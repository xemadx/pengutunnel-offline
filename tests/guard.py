import os,sys,resource,ctypes,errno
os.chdir('/scratch')
os.environ.clear()
os.environ.update(PATH='/usr/sbin:/usr/bin:/sbin:/bin',HOME='/scratch/home',TMPDIR='/scratch/tmp',LANG='C.UTF-8',GOMAXPROCS='2',GOMEMLIMIT='256MiB',GOGC='40',PYTHONDONTWRITEBYTECODE='1')
for key,limit in [('CPU',35),('AS',2*1024**3),('NPROC',180),('FSIZE',64*1024**2),('NOFILE',512),('CORE',0),('STACK',16*1024**2)]:
 if '/package/tools/export_engine.py' in sys.argv:
  limit={'CPU':180,'FSIZE':128*1024**2}.get(key,limit)
 resource.setrlimit(getattr(resource,'RLIMIT_'+key),(limit,limit))
lib=ctypes.CDLL('libseccomp.so.2',use_errno=True)
lib.seccomp_init.restype=ctypes.c_void_p
lib.seccomp_rule_add.argtypes=[ctypes.c_void_p,ctypes.c_uint32,ctypes.c_int,ctypes.c_uint]
lib.seccomp_syscall_resolve_name.argtypes=[ctypes.c_char_p]
lib.seccomp_load.argtypes=[ctypes.c_void_p]
ctx=lib.seccomp_init(0x7fff0000)
class Cmp(ctypes.Structure):
 _fields_=[('arg',ctypes.c_uint),('op',ctypes.c_uint),('a',ctypes.c_uint64),('b',ctypes.c_uint64)]
lib.seccomp_rule_add_array.argtypes=[ctypes.c_void_p,ctypes.c_uint32,ctypes.c_int,ctypes.c_uint,ctypes.POINTER(Cmp)]
nr=lib.seccomp_syscall_resolve_name(b'socket')
for fam in range(65):
 if fam not in (1,2,10,16,17):
  cmp=Cmp(0,4,fam,0);assert lib.seccomp_rule_add_array(ctx,0x50000|errno.EPERM,nr,1,ctypes.byref(cmp))==0
cmp=Cmp(0,6,64,0);assert lib.seccomp_rule_add_array(ctx,0x50000|errno.EPERM,nr,1,ctypes.byref(cmp))==0
for name in ['ptrace','process_vm_readv','process_vm_writev','mount','umount2','pivot_root','chroot','unshare','setns','bpf','perf_event_open','keyctl','add_key','request_key','init_module','finit_module','delete_module','reboot','kexec_load','open_by_handle_at','io_uring_setup','userfaultfd']:
 nr=lib.seccomp_syscall_resolve_name(name.encode())
 if nr>=0: assert lib.seccomp_rule_add(ctx,0x50000|errno.EPERM,nr,0)==0,name
assert lib.seccomp_load(ctx)==0
os.execve(sys.argv[1],sys.argv[1:],dict(os.environ))
