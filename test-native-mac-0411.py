from pathlib import Path
import subprocess,json,platform,sys,socket,time
assert sys.platform=='darwin'
root=Path.cwd();exe=root/'stage/GRIP BREAK.app/Contents/MacOS/GRIP BREAK';checks=root/'checks';checks.mkdir()
summary={'version':'0.4.11','platform':platform.platform(),'architecture':platform.machine(),'nativePhysicsPassed':False,'graphicsTested':False,'privateInternetJoinTested':False,'nativeUpdaterLocalTested':False,'sessionLifetimeTested':False,'reports':[],'unresolvedChecks':[]}
def run(flag,folder,report,graphics=False,timeout=120):
    args=[str(exe)]
    if not graphics:args+=['-batchmode','-nographics']
    if flag=='mac-updater-test':args+=['--mac-updater-archive',str(root/'incoming/GRIP_BREAK-macOS.zip')]
    args+=['--'+flag,'--evidence',str(checks/folder),'-logFile',str(checks/(folder+'.log')),'-screen-width','1600','-screen-height','900','-screen-fullscreen','0']
    subprocess.run(args,check=True,timeout=timeout)
    data=json.loads((checks/folder/report).read_text())
    failed=[c for c in data['checks'] if not c['passed']]
    summary['reports'].append({'file':folder+'/'+report,'checks':len(data['checks']),'failed':len(failed),'issues':data['issues'],'graphics':data['graphics']})
    # Keep the actual failed benchmark result. A virtual GPU cannot establish
    # desktop hardware performance; it must not prevent menu capture.
    virtualBenchmark=folder=='gym' and data['graphics']=='Apple Paravirtual device' and len(failed)==1 and failed[0]['name']=='gym_performance'
    if virtualBenchmark:summary['unresolvedChecks'].extend(failed)
    assert data['build']=='0.4.11' and data['issues']==0 and (not failed or virtualBenchmark),(folder,failed,data['issues'])
    return data
def session():
    listener=socket.socket();listener.bind(('127.0.0.1',0));port=listener.getsockname()[1];listener.close()
    children=[];logs=[];base=checks/'session';base.mkdir()
    try:
        for peer in ('host','client'):
            evidence=base/peer;evidence.mkdir();log=(base/(peer+'.log')).open('w');logs.append(log)
            args=[str(exe),'-batchmode','-nographics','--session-'+peer+'-test','--port',str(port),'--address','127.0.0.1','--evidence',str(evidence),'-logFile',str(base/(peer+'-unity.log'))]
            child=subprocess.Popen(args,stdout=log,stderr=subprocess.STDOUT);children.append(child)
            if peer=='host':
                end=time.monotonic()+30
                while not (evidence/'session-listening.txt').exists() and child.poll() is None and time.monotonic()<end:time.sleep(.1)
                assert (evidence/'session-listening.txt').exists(),'native session host did not listen'
        end=time.monotonic()+150
        for child in children:assert child.wait(timeout=max(1,end-time.monotonic()))==0,'native session child failed'
        for peer in ('host','client'):
            data=json.loads((base/peer/('session-'+peer+'.json')).read_text());failed=[c for c in data['checks'] if not c['passed']]
            summary['reports'].append({'file':'session/'+peer+'/session-'+peer+'.json','checks':len(data['checks']),'failed':len(failed),'issues':data['issues'],'graphics':data['graphics']})
            assert data['build']=='0.4.11' and data['issues']==0 and not failed,(peer,failed,data['issues'])
        summary['sessionLifetimeTested']=True
        summary['sessionScope']='two native loopback TCP peers; staged RoundWin result events; real manual aim input; three rounds, rematch,25s result/lobby idles,client/host coordinated lobby, intentional leave; not physically earned pins or internet tunnel hosting'
    finally:
        for child in children:
            if child.poll() is None:child.terminate()
        for child in children:
            try:child.wait(timeout=5)
            except subprocess.TimeoutExpired:child.kill();child.wait(timeout=5)
        for log in logs:log.close()
try:
    run('mac-updater-test','mac-updater','mac-updater.json',timeout=180)
    summary['nativeUpdaterLocalTested']=True
    session()
    run('ground-recovery-test','ground-recovery','ground-recovery.json')
    run('stamina-test','stamina','stamina.json')
    run('scramble-test','scramble','scramble.json')
    # Stance includes rendered live movement plus a nested prepared-grip
    # fixture. Match the actual interactive Windows check rather than running
    # this mixed visual/contact sequence with no render/interpolation frames.
    run('stance-test','stance','stance.json',True)
    run('corner-test','corner','corner.json')
    run('top-control-test','top-control','top-control.json')
    run('hand-contact-test','hand-contact','hand-contact.json',True)
    summary['nativePhysicsPassed']=True
    run('appearance-test','appearance','appearance.json',True)
    run('gym-test','gym','gym.json',True)
    ui=run('menu-shot','ui','ui.json',True)
    assert (checks/'ui/menu.png').exists()
    assert any(n in ui['graphics'] for n in ('Metal','Apple','Intel','AMD')),ui['graphics']
    summary['graphicsTested']=True;summary['graphicsDevice']=ui['graphics']
finally:
    summary['nativeChecks']=sum(r['checks'] for r in summary['reports'])
    summary['passedChecks']=sum(r['checks']-r['failed'] for r in summary['reports'])
    (checks/'native-summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
