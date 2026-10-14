from pathlib import Path
import subprocess,json,platform,sys,socket,time,shutil,tempfile,re,traceback
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
failures=[]
def attempt(name,operation):
    try:return True,operation()
    except Exception as error:
        failures.append({'category':name,'type':type(error).__name__,'message':str(error)});traceback.print_exc();return False,None
try:
    ok,_=attempt('mac-updater',lambda:run('mac-updater-test','mac-updater','mac-updater.json',timeout=180));summary['nativeUpdaterLocalTested']=ok
    attempt('session-lifetime',session)
    physics=[]
    for flag,folder,report,graphics in (
        ('ground-recovery-test','ground-recovery','ground-recovery.json',False),
        ('stamina-test','stamina','stamina.json',False),
        ('scramble-test','scramble','scramble.json',False),
        ('stance-test','stance','stance.json',True),
        ('corner-test','corner','corner.json',False),
        ('top-control-test','top-control','top-control.json',False),
        ('hand-contact-test','hand-contact','hand-contact.json',True)):
        ok,_=attempt(folder,lambda flag=flag,folder=folder,report=report,graphics=graphics:run(flag,folder,report,graphics));physics.append(ok)
    summary['nativePhysicsPassed']=all(physics)
    attempt('appearance',lambda:run('appearance-test','appearance','appearance.json',True))
    attempt('gym',lambda:run('gym-test','gym','gym.json',True))
    def menus():
        ui=run('menu-shot','ui','ui.json',True)
        assert (checks/'ui/menu.png').exists() and any(n in ui['graphics'] for n in ('Metal','Apple','Intel','AMD')),ui['graphics']
        summary['graphicsDevice']=ui['graphics'];return ui
    ok,_=attempt('ui',menus);summary['graphicsTested']=ok
    assert not failures,failures

finally:
    fixture=checks/'mac-updater/mac-updater-fixture-root.txt'
    if fixture.exists():
        owned=Path(fixture.read_text().strip()).resolve();owned.relative_to(Path(tempfile.gettempdir()).resolve())
        assert re.fullmatch(r'GRIP_BREAK-MacUpdaterAudit-[0-9a-f]{32}',owned.name) and (owned/'disposable-owned.txt').read_text().strip()==owned.name
        for job in owned.glob('.GRIP_BREAK-update-*'):
            assert not job.is_symlink() and re.fullmatch(r'\.GRIP_BREAK-update-[0-9a-f]{32}',job.name)
            dest=checks/'mac-updater/jobs'/job.name;dest.mkdir(parents=True,exist_ok=True)
            for name in ('install.log','update-job.json','result','restart-started','restart-ok','install.sh'):
                source=job/name
                if source.is_file() and not source.is_symlink():shutil.copy2(source,dest/name)
    summary['functionalFailures']=failures
    summary['nativeChecks']=sum(r['checks'] for r in summary['reports'])
    summary['passedChecks']=sum(r['checks']-r['failed'] for r in summary['reports'])
    (checks/'native-summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
