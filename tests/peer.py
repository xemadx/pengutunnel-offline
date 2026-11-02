import sys,socket,threading,json,hashlib,time,http.client,concurrent.futures,os
mode=sys.argv[1]
if mode=='proxy-echo':
 def exact(s,n):
  out=bytearray()
  while len(out)<n:
   b=s.recv(n-len(out))
   if not b:raise OSError('short PROXY header')
   out.extend(b)
  return bytes(out)
 def handle(s):
  with s:
   s.settimeout(4)
   try:
    header=exact(s,16)
    if header[:12]!=b'\r\n\r\n\x00\r\nQUIT\n' or header[12]!=0x21:raise OSError('invalid PROXY v2 header')
    length=int.from_bytes(header[14:16],'big')
    if length>512:raise OSError('PROXY header limit')
    exact(s,length)
    while True:
     b=s.recv(65536)
     if not b:break
     s.sendall(b)
   except OSError:pass
 server=socket.socket();server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1);server.bind(('0.0.0.0',24756));server.listen(32)
 while True:
  s,_=server.accept();threading.Thread(target=handle,args=(s,),daemon=True).start()
if mode=='echo':
 def tcp_client(s):
  with s:
   s.settimeout(4)
   try:
    while True:
     b=s.recv(65536)
     if not b:break
     s.sendall(b)
   except OSError: pass
 def tcp():
  s=socket.socket();s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1);s.bind(('0.0.0.0',24556));s.listen(64)
  while True:
   c,_=s.accept();threading.Thread(target=tcp_client,args=(c,),daemon=True).start()
 def udp():
  s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM);s.bind(('0.0.0.0',24556))
  while True:
   b,a=s.recvfrom(65536);s.sendto(b,a)
 threading.Thread(target=tcp,daemon=True).start();threading.Thread(target=udp,daemon=True).start()
 print('READY',flush=True);time.sleep(2300)
elif mode=='health':
 try:
  c=http.client.HTTPConnection('127.0.0.1',21234,timeout=.35);c.request('GET','/health');r=c.getresponse();print(json.dumps({'status':r.status,'body':json.loads(r.read(32768))}));c.close()
 except Exception as e: print(json.dumps({'error':str(e)}))
elif mode=='probe':
 host=sys.argv[2];port=int(sys.argv[3]);proto=sys.argv[4];sizes=json.loads(sys.argv[5]);parallel=int(sys.argv[6]);halfclose=sys.argv[7]=='1';read_timeout=float(sys.argv[8]) if len(sys.argv)>8 else 3
 def transfer(i):
  results=[]
  for n in sizes:
   data=bytes(((j*17+i)%251 for j in range(n)));got=bytearray();started=time.monotonic()
   try:
    if proto=='udp':
     with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
      s.settimeout(2);s.sendto(data,(host,port));got.extend(s.recvfrom(65536)[0])
    else:
     with socket.create_connection((host,port),timeout=1.5) as s:
      s.settimeout(read_timeout)
      if halfclose:
       s.sendall(data);s.shutdown(socket.SHUT_WR)
       while len(got)<n:
        b=s.recv(n-len(got))
        if not b:break
        got.extend(b)
      else:
       for off in range(0,n,16384):
        part=data[off:off+16384];s.sendall(part);end=len(got)+len(part)
        while len(got)<end:
         b=s.recv(end-len(got))
         if not b:raise RuntimeError('unexpected EOF')
         got.extend(b)
    results.append({'bytes':n,'ok':bytes(got)==data,'received':len(got),'sha256':hashlib.sha256(got).hexdigest(),'seconds':round(time.monotonic()-started,4)})
   except Exception as e:results.append({'bytes':n,'ok':False,'error':str(e)});break
  return results
 with concurrent.futures.ThreadPoolExecutor(max_workers=parallel) as pool: rows=list(pool.map(transfer,range(parallel)))
 print(json.dumps({'ok':all(len(r)==len(sizes) and all(x['ok'] for x in r) for r in rows),'transfers':rows}))
elif mode=='isolation':
 print(json.dumps({'uid':os.getuid(),'host_mount_visible':os.path.exists('/mnt/c'),'host_key_visible':os.path.exists('/root/.ssh'),'netns':os.readlink('/proc/self/ns/net'),'environment':dict(os.environ)}))
elif mode=='rawrequest':
 with socket.create_connection((sys.argv[2],int(sys.argv[3])),timeout=1) as s:
  s.settimeout(1);s.sendall(bytes.fromhex(sys.argv[4]))
  try: print(repr(s.recv(2048)))
  except OSError as e:print(str(e))
elif mode=='capture':
 s=socket.socket(socket.AF_PACKET,socket.SOCK_RAW,socket.htons(3));s.bind((sys.argv[2],0));s.settimeout(.3);end=time.monotonic()+7;rows=[]
 while time.monotonic()<end and len(rows)<150:
  try:b=s.recv(65535)
  except socket.timeout:continue
  if len(b)>42 and b[12:14]==b'\x08\x00' and b[23]==17:
   off=14+(b[14]&15)*4;payload=b[off+8:]
   rows.append({'src':socket.inet_ntoa(b[26:30]),'dst':socket.inet_ntoa(b[30:34]),'sport':int.from_bytes(b[off:off+2],'big'),'dport':int.from_bytes(b[off+2:off+4],'big'),'bytes':len(payload),'payload_prefix':payload[:80].hex()})
 print(json.dumps(rows))
