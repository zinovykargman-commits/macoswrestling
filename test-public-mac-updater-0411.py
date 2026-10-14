from pathlib import Path
import hashlib,json,platform,subprocess,sys,urllib.request
assert sys.platform=='darwin'
root=Path.cwd();checks=root/'checks';checks.mkdir(exist_ok=True)
repository='zinovykargman-commits/macoswrestling'
def fetch(url):
    return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'GRIP-BREAK-Mac-Updater-Native-Public','Accept':'application/vnd.github+json' if url.startswith('https://api.github.com/') else 'application/octet-stream'}),timeout=60)
with fetch('https://api.github.com/repos/'+repository+'/releases/latest') as response:release=json.load(response)
assert release['tag_name']=='v0.4.11' and not release['draft'] and not release['prerelease'],'Actual stable0.4.11 public release required'
assets={a['name']:a for a in release['assets']};archive='GRIP_BREAK-macOS.zip';checksum='GRIP_BREAK-macOS-SHA256.txt'
for name in (archive,checksum):
    assert assets[name]['browser_download_url']=='https://github.com/'+repository+'/releases/download/v0.4.11/'+name
with fetch(assets[checksum]['browser_download_url']) as response:lines=response.read(16385).decode().splitlines()
expected=[line.split()[0] for line in lines if len(line.split())==2 and line.split()[1]==archive];assert len(expected)==1
incoming=root/'incoming';incoming.mkdir(exist_ok=True);download=incoming/archive
digest=hashlib.sha256()
with fetch(assets[archive]['browser_download_url']) as response,download.open('wb') as output:
    while True:
        chunk=response.read(1024*1024)
        if not chunk:break
        output.write(chunk);digest.update(chunk)
assert download.stat().st_size==assets[archive]['size'] and digest.hexdigest()==expected[0]
subprocess.run(['/usr/bin/ditto','-x','-k',str(download),str(root/'stage')],check=True,timeout=60)
app=root/'stage/GRIP BREAK.app';subprocess.run(['/usr/bin/codesign','--verify','--deep','--strict',str(app)],check=True,timeout=40)
exe=app/'Contents/MacOS/GRIP BREAK'
subprocess.run([str(exe),'-batchmode','-nographics','--mac-updater-public-test','--evidence',str(checks/'public'),'-logFile',str(checks/'public.log')],check=True,timeout=500)
data=json.loads((checks/'public/mac-updater-public.json').read_text());failed=[c for c in data['checks'] if not c['passed']]
summary={'version':'0.4.11','architecture':platform.machine(),'actualStableRelease':release['html_url'],'bootstrapArchiveHash':expected[0],'nativeChecks':len(data['checks']),'passedChecks':len(data['checks'])-len(failed),'issues':data['issues'],'failed':failed,'publicDownloadReplaceRestartPassed':data['build']=='0.4.11' and not failed and data['issues']==0,'scope':'Actual latestGitHub archive/checksum re-downloaded by game,strictZIP/CRC/signature verified,owneddisposable.app replaced,andnative firstframeack received; callerapp/preferences/outsidefiles unchanged; no DeveloperID/notarization claim'}
(checks/'public-updater-summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2));assert summary['publicDownloadReplaceRestartPassed'],failed
