from pathlib import Path
import subprocess,json,platform,sys,plistlib,traceback,hashlib,os
assert sys.platform=='darwin'
root=Path.cwd();app=root/'stage/GRIP BREAK.app';exe=app/'Contents/MacOS/GRIP BREAK';checks=root/'checks';checks.mkdir()
info=plistlib.loads((app/'Contents/Info.plist').read_bytes());assert info['CFBundleShortVersionString']=='0.4.12' and info['CFBundleIdentifier']=='com.gripbreak.macoswrestling' and info['CFBundleExecutable']=='GRIP BREAK'
subprocess.run(['/usr/bin/codesign','--verify','--deep','--strict',str(app)],check=True,timeout=40)
summary={'version':'0.4.12','platform':platform.platform(),'architecture':platform.machine(),'nativePhysicsPassed':False,'graphicsTested':False,'privateInternetJoinTested':False,'nativeUpdaterLocalTested':False,'unchangedUpdaterBaseline':'0.4.11 local27/27 each; Intel actual-public5/5; ARM actual-public incomplete/hosted quota','currentUpdaterBundleVersionSignatureChecked':True,'sessionLifetimeTested':False,'sessionBaseline':'0.4.11 unchanged protocol12 lifecycle37 checks per architecture','reports':[],'unresolvedChecks':[]}
scope=os.environ.get('GRIP_NATIVE_SCOPE','full');assert scope in ('full','momentum');summary['scope']=scope
def run(flag,folder,report,graphics=False,timeout=110):
    args=[str(exe)]+([] if graphics else ['-batchmode','-nographics'])+['--'+flag,'--evidence',str(checks/folder),'-logFile',str(checks/(folder+'.log')),'-screen-width','1600','-screen-height','900','-screen-fullscreen','0']
    subprocess.run(args,check=True,timeout=timeout)
    data=json.loads((checks/folder/report).read_text());failed=[c for c in data['checks'] if not c['passed']]
    summary['reports'].append({'file':folder+'/'+report,'checks':len(data['checks']),'failed':len(failed),'issues':data['issues'],'graphics':data['graphics']})
    virtual=folder=='gym' and data['graphics']=='Apple Paravirtual device' and len(failed)==1 and failed[0]['name']=='gym_performance'
    if virtual:summary['unresolvedChecks'].extend(failed)
    assert data['build']=='0.4.12' and data['issues']==0 and (not failed or virtual),(folder,failed,data['issues'])
    return data
failures=[]
def attempt(name,operation):
    try:return True,operation()
    except Exception as error:failures.append({'category':name,'type':type(error).__name__,'message':str(error)});traceback.print_exc();return False,None
try:
    physics=[]
    plans=(
        ('physics-snapshot-test','physics-snapshot','physics-snapshots.json',False),
        ('momentum-test','momentum','momentum.json',False),
        ('stamina-test','stamina','stamina.json',False),
        ('ground-recovery-test','ground-recovery','ground-recovery.json',False),
        ('scramble-test','scramble','scramble.json',False),
        ('camera-obstruction-test','camera-obstruction','camera-obstruction.json',True),
        ('hand-contact-test','hand-contact','hand-contact.json',True))
    if scope=='momentum':plans=(('momentum-test','momentum','momentum.json',False),)
    for flag,folder,report,graphics in plans:
        ok,_=attempt(folder,lambda flag=flag,folder=folder,report=report,graphics=graphics:run(flag,folder,report,graphics));physics.append(ok)
    summary['nativePhysicsPassed']=all(physics)
    cpuPath=checks/'physics-snapshot/physics-snapshot-cpu.json'
    if cpuPath.exists():summary['snapshotCpuEvidence']=json.loads(cpuPath.read_text())
    def menu():
        data=run('menu-shot','ui','ui.json',True);assert (checks/'ui/menu.png').exists() and any(n in data['graphics'] for n in ('Metal','Apple','Intel','AMD'));return data
    if scope=='full':
        ok,_=attempt('ui',menu);summary['graphicsTested']=ok
    assert not failures,failures
finally:
    summary['functionalFailures']=failures;summary['nativeChecks']=sum(r['checks'] for r in summary['reports']);summary['passedChecks']=sum(r['checks']-r['failed'] for r in summary['reports'])
    (checks/'native-summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
