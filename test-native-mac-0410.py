from pathlib import Path
import subprocess,json,platform,sys
assert sys.platform=='darwin'
root=Path.cwd();exe=root/'stage/GRIP BREAK.app/Contents/MacOS/GRIP BREAK';checks=root/'checks';checks.mkdir()
summary={'version':'0.4.10','platform':platform.platform(),'architecture':platform.machine(),'nativePhysicsPassed':False,'graphicsTested':False,'privateInternetJoinTested':False,'reports':[],'unresolvedChecks':[]}
def run(flag,folder,report,graphics=False):
    args=[str(exe)]
    if not graphics:args+=['-batchmode','-nographics']
    args+=['--'+flag,'--evidence',str(checks/folder),'-logFile',str(checks/(folder+'.log')),'-screen-width','1600','-screen-height','900','-screen-fullscreen','0']
    subprocess.run(args,check=True,timeout=120)
    data=json.loads((checks/folder/report).read_text())
    failed=[c for c in data['checks'] if not c['passed']]
    summary['reports'].append({'file':folder+'/'+report,'checks':len(data['checks']),'failed':len(failed),'issues':data['issues'],'graphics':data['graphics']})
    # Keep the actual failed benchmark result. A virtual GPU cannot establish
    # desktop hardware performance; it must not prevent menu capture.
    virtualBenchmark=folder=='gym' and data['graphics']=='Apple Paravirtual device' and len(failed)==1 and failed[0]['name']=='gym_performance'
    if virtualBenchmark:summary['unresolvedChecks'].extend(failed)
    assert data['build']=='0.4.10' and data['issues']==0 and (not failed or virtualBenchmark),(folder,failed,data['issues'])
    return data
try:
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
