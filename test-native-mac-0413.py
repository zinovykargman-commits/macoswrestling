from pathlib import Path
import subprocess,json,platform,sys,plistlib,traceback
assert sys.platform=='darwin'
root=Path.cwd();app=root/'stage/GRIP BREAK.app';exe=app/'Contents/MacOS/GRIP BREAK';checks=root/'checks';checks.mkdir()
info=plistlib.loads((app/'Contents/Info.plist').read_bytes());assert info['CFBundleShortVersionString']=='0.4.13' and info['CFBundleIdentifier']=='com.gripbreak.macoswrestling' and info['CFBundleExecutable']=='GRIP BREAK'
subprocess.run(['/usr/bin/codesign','--verify','--deep','--strict',str(app)],check=True,timeout=40)
summary={'version':'0.4.13','platform':platform.platform(),'architecture':platform.machine(),'currentGPUVisualsPassed':False,'graphicsTested':False,'nativePhysicsPassed':False,'physicsBaseline':'0.4.12 corrected momentum23/23 each; literal productionGBWrestler source retained','privateInternetJoinTested':False,'nativeUpdaterLocalTested':False,'unchangedUpdaterBaseline':'0.4.11 local27/27 each; Intel actual-public5/5; ARM actual-public incomplete/hosted quota','currentUpdaterBundleVersionSignatureChecked':True,'sessionLifetimeTested':False,'sessionBaseline':'0.4.11 unchanged protocol12 lifecycle37 checks per architecture','reports':[],'unresolvedChecks':[],'wholeGameMacFPSTested':False}
failures=[]
def run(flag,folder,report):
    args=[str(exe),'--'+flag,'--graphics-quality','high','--evidence',str(checks/folder),'-logFile',str(checks/(folder+'.log')),'-screen-width','1600','-screen-height','900','-screen-fullscreen','0']
    subprocess.run(args,check=True,timeout=180)
    data=json.loads((checks/folder/report).read_text());failed=[c for c in data['checks'] if not c['passed']]
    summary['reports'].append({'file':folder+'/'+report,'checks':len(data['checks']),'failed':len(failed),'issues':data['issues'],'graphics':data['graphics']})
    assert data['build']=='0.4.13' and data['issues']==0 and not failed,(folder,failed,data['issues'])
    return data
def attempt(name,operation):
    try:return True,operation()
    except Exception as error:failures.append({'category':name,'type':type(error).__name__,'message':str(error)});traceback.print_exc();return False,None
try:
    results=[]
    for flag,folder,report in (('render-optimization-test','render-optimization','render-optimization.json'),('camera-obstruction-test','camera-obstruction','camera-obstruction.json'),('hand-contact-test','hand-contact','hand-contact.json')):
        ok,_=attempt(folder,lambda flag=flag,folder=folder,report=report:run(flag,folder,report));results.append(ok)
    summary['currentGPUVisualsPassed']=all(results)
    def menu():
        data=run('menu-shot','ui','ui.json');assert (checks/'ui/menu.png').exists() and any(n in data['graphics'] for n in ('Metal','Apple','Intel','AMD'));return data
    ok,_=attempt('ui',menu);summary['graphicsTested']=ok
    assert not failures,failures
finally:
    summary['functionalFailures']=failures;summary['nativeChecks']=sum(r['checks'] for r in summary['reports']);summary['passedChecks']=sum(r['checks']-r['failed'] for r in summary['reports'])
    (checks/'native-summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
