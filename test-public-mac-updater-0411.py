from pathlib import Path
import hashlib,json,platform,subprocess,sys,urllib.request,urllib.error,shutil,tempfile,re,os
assert sys.platform=='darwin'
root=Path.cwd();checks=root/'checks';checks.mkdir(exist_ok=True)
repository='zinovykargman-commits/macoswrestling'
def fetch(url):
    headers={'User-Agent':'GRIP-BREAK-Mac-Updater-Native-Public','Accept':'application/vnd.github+json' if url.startswith('https://api.github.com/') else 'application/octet-stream'}
    if url.startswith('https://api.github.com/') and os.environ.get('GRIP_BOOTSTRAP_GH_TOKEN'):headers['Authorization']='Bearer '+os.environ['GRIP_BOOTSTRAP_GH_TOKEN']
    return urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=60)
latest='https://api.github.com/repos/'+repository+'/releases/latest'
preflight={'url':latest,'authenticated':False,'architecture':platform.machine(),'system':platform.platform()}
try:
    with urllib.request.urlopen(urllib.request.Request(latest,headers={'User-Agent':'GRIP-BREAK-Mac-Updater-Native-Public','Accept':'application/vnd.github+json'}),timeout=30) as response:
        preflight.update(status=response.status,remaining=response.headers.get('X-RateLimit-Remaining'),reset=response.headers.get('X-RateLimit-Reset'));json.load(response)
except urllib.error.HTTPError as error:
    preflight.update(status=error.code,remaining=error.headers.get('X-RateLimit-Remaining'),reset=error.headers.get('X-RateLimit-Reset'),body=error.read(4096).decode(errors='replace'))
(checks/'anonymous-api-preflight.json').write_text(json.dumps(preflight,indent=2));print(json.dumps(preflight,indent=2),flush=True)
assert preflight['status']==200,'Anonymous production-game API route unavailable: see anonymous-api-preflight.json; no native game attempt made'
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
def owned_roots():
    roots=[];temporary=Path(tempfile.gettempdir()).resolve()
    for candidate in temporary.glob('GRIP_BREAK-MacUpdaterAudit-*'):
        if candidate.is_symlink() or not candidate.is_dir() or not re.fullmatch(r'GRIP_BREAK-MacUpdaterAudit-[0-9a-f]{32}',candidate.name):continue
        marker=candidate/'disposable-owned.txt'
        if marker.is_symlink() or not marker.is_file() or marker.stat().st_size>128 or marker.read_text().strip()!=candidate.name:continue
        candidate.resolve().relative_to(temporary);roots.append(candidate.resolve())
    return set(roots)
beforeRoots=owned_roots();gameEnvironment={key:value for key,value in os.environ.items() if key not in ('GRIP_BOOTSTRAP_GH_TOKEN','GITHUB_TOKEN','GH_TOKEN')}
gameFailure=None
try:subprocess.run([str(exe),'-batchmode','-nographics','--mac-updater-public-test','--evidence',str(checks/'public'),'-logFile',str(checks/'public.log')],check=True,timeout=500,env=gameEnvironment)
except (subprocess.CalledProcessError,subprocess.TimeoutExpired) as error:gameFailure=str(error)
newRoots=owned_roots()-beforeRoots
assert len(newRoots)<=2,'Unexpected number of new marked fixture roots'
fixture=checks/'public/mac-public-clone-root.txt';successful=Path(fixture.read_text().strip()).resolve() if fixture.exists() else None
if successful is not None:assert successful in newRoots,'Success marker does not refer to this test-created owned clone'
for owned in sorted(newRoots):
    exported=checks/'public'/('actual-update' if owned==successful else 'early-child-'+owned.name);exported.mkdir(parents=True,exist_ok=True)
    for folder in ('public-evidence','restart-evidence'):
        source=owned/folder
        if source.exists() and not source.is_symlink():
            for item in source.glob('*'):
                if item.is_file() and not item.is_symlink() and item.suffix in ('.json','.txt') and item.stat().st_size<=8*1024*1024:shutil.copy2(item,exported/item.name)
    for job in owned.glob('.GRIP_BREAK-update-*'):
        assert not job.is_symlink() and re.fullmatch(r'\.GRIP_BREAK-update-[0-9a-f]{32}',job.name)
        for name in ('install.log','update-job.json','result','restart-started','restart-ok'):
            source=job/name
            if source.is_file() and not source.is_symlink() and source.stat().st_size<=8*1024*1024:shutil.copy2(source,exported/name)
    for report in exported.glob('*.json'):
        if 'failed' in report.name:print('Actual child failure '+report.name+': '+report.read_text(),flush=True)
if gameFailure:(checks/'game-process-failure.json').write_text(json.dumps({'error':gameFailure,'exportedNewOwnedClones':len(newRoots)},indent=2))
data=json.loads((checks/'public/mac-updater-public.json').read_text());failed=[c for c in data['checks'] if not c['passed']]
summary={'version':'0.4.11','architecture':platform.machine(),'system':platform.platform(),'actualStableRelease':release['html_url'],'bootstrapArchiveHash':expected[0],'bootstrapApiAuthenticated':bool(os.environ.get('GRIP_BOOTSTRAP_GH_TOKEN')),'gameUpdaterAuthenticated':False,'nativeChecks':len(data['checks']),'passedChecks':len(data['checks'])-len(failed),'issues':data['issues'],'failed':failed,'publicDownloadReplaceRestartPassed':data['build']=='0.4.11' and not failed and data['issues']==0 and not gameFailure,'scope':'Attempt actual anonymous latestGitHub download/checksum/ZIP/signature/ownedapp replace/native firstframe acknowledgement; achieved behavior is recorded by individual checks and receipts; no DeveloperID/notarization claim'}
(checks/'public-updater-summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2));assert summary['publicDownloadReplaceRestartPassed'],failed
