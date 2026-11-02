import sys,os,json,subprocess,time,pathlib,hashlib,itertools,signal
BASE=pathlib.Path(sys.argv[1]);OUT=pathlib.Path(sys.argv[2]);SCR=BASE/'scratch';ROOT=BASE/'root'
RESULTS=[];PSK='AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA='
CORE_PATH=sys.argv[4] if len(sys.argv)>4 else '/package/pengutunnel.offline.elf'
def cmd(side,args,priv=False):
 caps='-all,+net_admin,+net_raw' if priv else '-all'
 return ['nsenter','--net=/run/netns/qa-'+side,'chroot',str(ROOT),'/usr/bin/setpriv','--reuid=65534','--regid=65534','--clear-groups','--bounding-set='+caps,'--inh-caps='+caps,'--ambient-caps='+caps,'--no-new-privs','/usr/bin/python3','-I','/input/guard.py',*args]
def execute(side,args,priv=False,timeout=12):
 try:
  p=subprocess.run(cmd(side,args,priv),capture_output=True,text=True,timeout=timeout)
  return {'exit':p.returncode,'stdout':p.stdout[:100000],'stderr':p.stderr[:8000]}
 except subprocess.TimeoutExpired as e:return {'timeout':True,'stdout':(e.stdout or b'').decode()[:100000]}
def peer(side,*args,timeout=12):
 r=execute(side,['/usr/bin/python3','-I','/input/peer.py',*map(str,args)],timeout=timeout)
 try:return json.loads(r['stdout'])
 except Exception:return r
def save(r):
 RESULTS.append(r)
 temporary=OUT/'results.json.new';temporary.write_text(json.dumps(RESULTS,indent=2));temporary.replace(OUT/'results.json')
 print(json.dumps({'case':r.get('case'),'pass':r.get('pass'),'unexpected':r.get('unexpected'),'count':len(RESULTS)}),flush=True)
def logread(path):
 try:
  fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
  try:return os.read(fd,120000).decode('utf8','replace')
  finally:os.close(fd)
 except OSError as e:return str(e)
def stop(p):
 if p.poll() is None:
  p.terminate()
  try:p.wait(timeout=2)
  except subprocess.TimeoutExpired:p.kill();p.wait(timeout=2)
def spawn(side,path,log,priv=False):
 f=open(log,'wb');p=subprocess.Popen(cmd(side,[CORE_PATH,'-config','/scratch/'+path.name],priv),stdout=f,stderr=subprocess.STDOUT);f.close();return p
def conf(kind,side,direction='reverse',cipher='aes-256-gcm',pool=1,extra='',tun=False,profile=None,psk=PSK,forward=True,pp=False,ipv6=False):
 ip='10.203.0.'+('1' if side=='a' else '2');other='10.203.0.'+('2' if side=='a' else '1')
 if tun:
  role='dualway' if direction=='dualway' else ('server' if (side=='a')==(direction=='reverse') else 'client')
 else:role='server' if side=='a' else 'client'
 listens=(side=='a')==(direction=='reverse')
 address=('listen = "0.0.0.0:24443"' if listens else 'remote = "'+other+':24443"')
 if ipv6: address=('listen = "[::]:24443"' if listens else 'remote = "[fd42:203::'+('2' if side=='a' else '1')+']:24443"')
 if tun and direction=='dualway':address='listen = "0.0.0.0:24443"\nremote = "'+other+':24443"'
 if profile:address=''
 t='[transport]\ntype = '+json.dumps(kind)+'\nmode = '+json.dumps(role)+'\n'+address+'\npool_connection = '+str(pool)+'\n'
 if not tun and direction=='direct':t+='l4_direction = "direct"\n'
 t+=extra+'\n'
 if profile:t+='[ipx]\nmode = '+json.dumps(role)+'\nprofile = '+json.dumps(profile)+'\nlisten_ip = '+json.dumps(ip)+'\ndst_ip = '+json.dumps(other)+'\ninterface = '+json.dumps('qa-v'+side)+'\n'+('icmp_type = '+str(0 if side=='a' else 8)+'\nicmp_code = 0\n' if profile=='icmp' else '')
 t+='[tun]\nhealth_port = 21234\n'
 if tun:t+='name = "qatu"\naddress = "10.204.0.'+('1' if side=='a' else '2')+'/24"\nmtu = 1380\n'
 t+='[security]\nenable_encryption = '+('false' if cipher=='none' else 'true')+'\nalgorithm = '+json.dumps(cipher)+'\npsk = '+json.dumps(psk)+'\n[health]\nheartbeat_interval = 1\nheartbeat_timeout = 4\n[tuning]\nauto_tuning = false\nworkers = 1\nstream_window = 2\n[logging]\nlevel = "debug"\n'
 if side=='a' and forward:t+='[forward]\nproxy_protocol = false\nports = ["24555=24556'+(' proxy_protocol=true' if pp else '')+'"'+(',"udp/24555=24556"' if tun and kind not in ('dns','ssh') else '')+']\n'
 return t
def pair(name,kind='tcpfwd',direction='reverse',cipher='aes-256-gcm',pool=1,extra='',extra_b=None,tun=False,profile=None,negative=False,psk_b=PSK,cipher_b=None,lifecycle=False,ipv6=False,halfclose=False,parallel=1,mutate_a=None,mutate_b=None):
 r={'case':name,'transport':kind,'direction':direction,'cipher':cipher,'pool':pool,'tun':tun,'profile':profile,'expected':'reject' if negative else 'transfer','configs':{}}
 ps=[];logs=[];start=time.monotonic()
 try:
  for side in ('a','b'):
   text=conf(kind,side,direction,cipher_b if side=='b' and cipher_b else cipher,pool,extra_b if side=='b' and extra_b is not None else extra,tun,profile,psk_b if side=='b' else PSK,ipv6=ipv6)
   if side=='a' and mutate_a:text=mutate_a(text)
   if side=='b' and mutate_b:text=mutate_b(text)
   r['configs'][side]=text;p=SCR/(name+'-'+side+'.toml');p.write_text(text);p.chmod(0o644)
   logfile=SCR/(name+'-'+side+'.log');logs.append(logfile)
  processes={}
  for side in (('b','a') if direction=='direct' else ('a','b')):
   processes[side]=spawn(side,SCR/(name+'-'+side+'.toml'),SCR/(name+'-'+side+'.log'),tun or 'sni_spoof' in extra)
   time.sleep(.35)
  ps=[processes[s] for s in ('a','b')]
  deadline=time.monotonic()+(2.5 if negative else 10)
  health={}
  while time.monotonic()<deadline:
   health={s:peer(s,'health',timeout=2) for s in ('a','b')}
   if all(h.get('body',{}).get('alive') for h in health.values()):break
   if any(p.poll() is not None for p in ps):break
   time.sleep(.15)
  r['health']=health;r['exits_before_probe']=[p.poll() for p in ps]
  r['probe']=peer('a','probe','127.0.0.1',24555,'tcp',json.dumps([64] if negative else [1,64,65536,1048576]),parallel,int(halfclose),timeout=20)
  if tun and kind not in ('dns','ssh') and not negative:r['udp_probe']=peer('a','probe','127.0.0.1',24555,'udp',json.dumps([1,64,1200]),1,0)
  if lifecycle and r['probe'].get('ok'):
   stop(ps[1]);time.sleep(.7)
   r['after_peer_stop']=peer('a','health');ps[1]=spawn('b',SCR/(name+'-b.toml'),SCR/(name+'-b-restart.log'),tun)
   deadline=time.monotonic()+9
   while time.monotonic()<deadline:
    h=peer('a','health')
    if h.get('body',{}).get('alive'):break
    if ps[0].poll() is not None:break
    time.sleep(.2)
   r['surviving_process_exit']=ps[0].poll();r['recovery_health']=h
   r['recovery_probe']=peer('a','probe','127.0.0.1',24555,'tcp','[65536]',1,0)
  r['pass']=(bool(r['probe'].get('transfers')) and not r['probe'].get('ok',False)) if negative else (r['probe'].get('ok',False) and r.get('udp_probe',{'ok':True}).get('ok',False))
 except Exception as e:r['exception']=repr(e);r['pass']=False
 finally:
  for p in ps:stop(p)
  r['process_exits']=[p.returncode for p in ps];r['logs']={s:logread(p) for s,p in zip(('a','b'),logs)}
  r['seconds']=round(time.monotonic()-start,3)
  # Remove test-created TUN links to keep subsequent cases independent.
  for side in ('a','b'):subprocess.run(['ip','-n','qa-'+side,'link','del','qatu'],capture_output=True)
  save(r)
def main():
 isolation={s:peer(s,'isolation') for s in ('a','b')}
 iso={'case':'isolation','pass':isolation['a'].get('netns')!=isolation['b'].get('netns'),'sides':isolation,'network':subprocess.check_output(['ip','-n','qa-a','route']).decode(),'limits':{'memory_bytes':1073741824,'swap':0,'pids':192,'cpu_cores':2,'scratch_bytes':536870912,'per_process_cpu_seconds':35,'per_file_bytes':12582912,'wall_seconds':2400}}
 save(iso)
 echo=peer_echo=[]
 try:
  for side in ('a','b'):
   logfile=open(SCR/('echo-'+side+'.log'),'wb');p=subprocess.Popen(cmd(side,['/usr/bin/python3','-I','/input/peer.py','echo']),stdout=logfile,stderr=logfile);logfile.close();echo.append(p)
  time.sleep(.3)
  save({'case':'veth-baseline','pass':peer('a','probe','10.203.0.2',24556,'tcp','[64,65536]',1,0).get('ok',False)})
  for tool,args in [('bootstrap',['/usr/bin/python3','-I','/package/tools/check_installer.py']),('installer-parity',['/usr/bin/python3','-I','/package/tools/check_parity_installer.py','/package/install-offline.sh']),('installer-regressions',['/usr/bin/python3','-I','/package/tools/check_regressions.py'])]:
   r=execute('a',args,timeout=45);save({'case':tool,'pass':r.get('exit')==0,'result':r})
  for flag in ('-version','-help'):
   r=execute('a',['/package/pengutunnel.offline.elf',flag]);save({'case':flag,'pass':r.get('exit')==0,'result':r})
  for kind,direction,cipher in itertools.product(['tcpfwd','tls','ws','wss','xhttp','xhttps'],['reverse','direct'],['aes-256-gcm','chacha20-poly1305','none']):
   pair('l4-'+kind+'-'+direction+'-'+cipher,kind,direction,cipher)
  for kind,cipher in itertools.product(('tcpfwd','tls','ws','wss','xhttp','xhttps'),('aes-256-gcm','chacha20-poly1305','none')):pair('wrong-psk-'+kind+'-'+cipher,kind,cipher=cipher,negative=True,psk_b='AQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQE=')
  for header in ('PGprotocol-NUM1','PGprotocol-NUM2','PGprotocol-NUM3'):pair('header-'+header,extra='l4_header = '+json.dumps(header))
  for kind in ('xhttp','xhttps'):
   for direction in ('reverse','direct'):pair('cdn-mode-'+kind+'-'+direction,kind,direction,extra='xhttp_cdn = true\nxhttp_path = "/qa"')
  for fp in ('chrome','firefox','safari','edge','ios'):pair('fingerprint-'+fp,'tls','direct',extra='sni = "qa.example.test"\ntls_fingerprint = '+json.dumps(fp))
  for kind in ('tcpfwd','tls','ws','xhttp'):pair('pool4-concurrent-'+kind,kind,pool=4,parallel=8)
  pair('tcp-halfclose',halfclose=True)
  pair('ipv6-tcpfwd',ipv6=True)
  pair('cipher-mismatch',negative=True,cipher_b='chacha20-poly1305')
  pair('header-autodetection',extra='l4_header = "PGprotocol-NUM1"',extra_b='l4_header = "PGprotocol-NUM2"')
  pair('ws-path-mismatch','ws',extra='ws_path = "/qa-a"',extra_b='ws_path = "/qa-b"',negative=True)
  for kind in ('tcp','udp','PGprotocol-NUM1','PGprotocol-NUM2','PGprotocol-NUM3','dns','ssh'):
   for direction,cipher in itertools.product(('reverse','direct'),('aes-256-gcm','chacha20-poly1305')):
    pair('tun-'+kind+'-'+direction+'-'+cipher,kind,direction,cipher,tun=True)
  for kind in ('tcp','udp'):pair('tun-'+kind+'-dualway',kind,'dualway',tun=True,pool=2)
  for profile,cipher in itertools.product(('icmp','ipip','ospf','gre','ah','esp'),('aes-256-gcm','chacha20-poly1305')):pair('ipx-'+profile+'-'+cipher,'ipx',cipher=cipher,tun=True,profile=profile)
  supplemental()
 finally:
  for p in echo:stop(p)
 print('FINISHED '+str(len(RESULTS)),flush=True)

def fault_case(kind):
 name='fault-recovery-'+kind;r={'case':name,'transport':kind,'expected':'recovery'};processes={};paths={};logs={}
 try:
  for side in ('a','b'):
   path=SCR/(name+'-'+side+'.toml');path.write_text(conf(kind,side,pool=2));path.chmod(0o644);paths[side]=path;logs[side]=SCR/(name+'-'+side+'.log')
   processes[side]=spawn(side,path,logs[side]);time.sleep(.4)
  time.sleep(1)
  r['initial']=peer('a','probe','127.0.0.1',24555,'tcp','[65536]',1,0)
  subprocess.run(['ip','-n','qa-a','link','set','qa-va','down'],check=True);time.sleep(.5)
  subprocess.run(['ip','-n','qa-a','link','set','qa-va','up'],check=True);time.sleep(1)
  r['link_flap_probe']=peer('a','probe','127.0.0.1',24555,'tcp','[65536]',1,0)
  # Forced peer exit does not send the graceful cross-peer restart signal.
  processes['b'].kill();processes['b'].wait();time.sleep(.5)
  processes['b']=spawn('b',paths['b'],SCR/(name+'-b-restart.log'))
  r['supervisor_restarts']=[];deadline=time.monotonic()+15
  while time.monotonic()<deadline:
   for side,p in list(processes.items()):
    if p.poll() is not None:
     r['supervisor_restarts'].append({'side':side,'exit':p.returncode});processes[side]=spawn(side,paths[side],SCR/(name+'-'+side+'-supervised.log'))
   h={s:peer(s,'health') for s in ('a','b')}
   if all(x.get('body',{}).get('alive') for x in h.values()):break
   time.sleep(.3)
  r['recovery_health']=h;r['recovery_probe']=peer('a','probe','127.0.0.1',24555,'tcp','[65536]',1,0)
  # An invalid opening on a separate connection must not break the live pair.
  r['invalid_opening']=peer('b','rawrequest','10.203.0.1',24443,b'INVALID-QA-OPENING\r\n'.hex())
  r['after_invalid_opening']=peer('a','probe','127.0.0.1',24555,'tcp','[65536]',1,0)
  r['pass']=all(r[x].get('ok',False) for x in ('initial','link_flap_probe','recovery_probe','after_invalid_opening'))
 except Exception as e:r['pass']=False;r['exception']=repr(e)
 finally:
  subprocess.run(['ip','-n','qa-a','link','set','qa-va','up'],capture_output=True)
  for p in processes.values():stop(p)
  r['logs']={s:logread(p) for s,p in logs.items()};save(r)


def supplemental():
 for side in ('a','b'):
  n='1' if side=='a' else '2';other='2' if side=='a' else '1'
  subprocess.run(['ip','-n','qa-'+side,'addr','add','10.205.0.'+n+'/32','dev','lo'],check=True)
  subprocess.run(['ip','-n','qa-'+side,'route','add','10.205.0.'+other+'/32','dev','qa-v'+side],check=True)
 for profile in ('icmp','ipip','ospf','gre','ah','esp'):
  pair('ipx-spoof-'+profile,'ipx',tun=True,profile=profile,
   mutate_a=lambda s:s.replace('[ipx]','[ipx]\nspoof_source = "10.205.0.1"\nspoof_peer = "10.205.0.2"'),
   mutate_b=lambda s:s.replace('[ipx]','[ipx]\nspoof_source = "10.205.0.2"\nspoof_peer = "10.205.0.1"'))
 for kind in ('tls','wss','xhttps'):
  pair('sni-spoof-'+kind,kind,'direct',extra='sni = "qa.example.test"\nsni_spoof = true\nsni_spoof_names = "fake.example.test"\nsni_spoof_strict = true')
 pair('custom-tun-addresses','tcp',tun=True,
  mutate_a=lambda s:s.replace('10.204.0.1/24','10.204.0.10/24').replace('24555=24556','24555=10.204.0.11:24556'),
  mutate_b=lambda s:s.replace('10.204.0.2/24','10.204.0.11/24'))
 for kind in ('tcpfwd','ws','xhttp'):fault_case(kind)

def proxy_cases():
 f=open(SCR/'proxy-backend.log','wb');backend=subprocess.Popen(cmd('b',['/usr/bin/python3','-I','/input/peer.py','proxy-echo']),stdout=f,stderr=f);f.close();time.sleep(.3)
 echo=subprocess.Popen(cmd('b',['/usr/bin/python3','-I','/input/peer.py','echo']),stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(.2)
 try:
  pair('proxy-v2-l4',mutate_a=lambda s:s.replace('24555=24556','24555=24756 proxy_protocol=true'))
  pair('proxy-v2-tun','tcp',tun=True,mutate_a=lambda s:s.replace('"24555=24556"','"24555=24756 proxy_protocol=true"'))
 finally:stop(backend);stop(echo)

if __name__=='__main__':
 mode=sys.argv[3] if len(sys.argv)>3 else 'all'
 if mode=='all':main()
 if mode in ('all','proxy'):proxy_cases()
 import importlib.util
 if mode=='export':
  spec=importlib.util.spec_from_file_location('export_artifacts',pathlib.Path(__file__).resolve().parent/'export_artifacts.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
  observation=module.export(globals());save({'case':'complete-machine-code-export','pass':True,'observation':observation});sys.exit(0)
 spec=importlib.util.spec_from_file_location('bootstrap_cli',pathlib.Path(__file__).resolve().parent/'bootstrap_cli.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 try:
  observation=module.check_bootstrap_cli(BASE,ROOT);save({'case':'persistent-bootstrap-cli','pass':True,'observation':observation})
 except Exception as error:save({'case':'persistent-bootstrap-cli','pass':False,'error':str(error)})
 failures=[r['case'] for r in RESULTS if r.get('pass') is not True]
 print(json.dumps({'cases':len(RESULTS),'failures':failures}),flush=True)
 sys.exit(bool(failures))
