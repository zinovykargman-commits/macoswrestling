from pathlib import Path
import subprocess,json,platform,sys,time
assert sys.platform=='darwin'
root=Path.cwd();exe=root/'stage/GRIP BREAK.app/Contents/MacOS/GRIP BREAK';checks=root/'checks';checks.mkdir()
command=[str(exe),'-batchmode','-nographics','--stamina-test','--evidence',str(checks/'stamina'),'-logFile',str(checks/'stamina.log')]
subprocess.run(command,check=True,timeout=120)
report=json.loads((checks/'stamina/stamina.json').read_text());assert report['issues']==0 and all(c['passed'] for c in report['checks'])
summary={'platform':platform.platform(),'architecture':platform.machine(),'nativeStaminaChecks':len(report['checks']),'nativePhysicsPassed':True,'graphicsTested':False,'privateInternetJoinTested':False}
# The hosted Mac may lack a usable desktop/Metal device. Keep graphical
# observations separate from the required headless physics/startup checks.
try:
    subprocess.run([str(exe),'--menu-shot','--evidence',str(checks/'ui'),'-logFile',str(checks/'ui.log'),'-screen-width','1600','-screen-height','900','-screen-fullscreen','0'],check=True,timeout=90)
    ui=json.loads((checks/'ui/ui.json').read_text());summary['uiChecks']=len(ui['checks']);summary['graphicsTested']=ui['issues']==0 and all(c['passed'] for c in ui['checks']) and (checks/'ui/menu.png').exists();summary['graphicsDevice']=ui['graphics']
except Exception as e:summary['graphicsLimitation']=str(e)
(checks/'native-summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
