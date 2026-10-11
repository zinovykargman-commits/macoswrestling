from pathlib import Path
import json,os,urllib.request
repository=os.environ['GITHUB_REPOSITORY'];token=os.environ['GH_TOKEN']
headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','User-Agent':'GripBreak-Mac-Native-Check'}
with urllib.request.urlopen(urllib.request.Request('https://api.github.com/repos/'+repository+'/releases',headers=headers),timeout=30) as r:releases=json.load(r)
release=next(r for r in releases if r['tag_name']=='v0.4.4')
asset=next(a for a in release['assets'] if a['name']=='GRIP_BREAK-macOS.zip')
headers['Accept']='application/octet-stream'
class Redirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        new=super().redirect_request(req,fp,code,msg,headers,newurl)
        if new:new.remove_header('Authorization')
        return new
opener=urllib.request.build_opener(Redirect());p=Path('incoming/GRIP_BREAK-macOS.zip');p.parent.mkdir(exist_ok=True)
with opener.open(urllib.request.Request(asset['url'],headers=headers),timeout=60) as r:p.write_bytes(r.read())
print('Fetched staged archive',p.stat().st_size,'bytes')
