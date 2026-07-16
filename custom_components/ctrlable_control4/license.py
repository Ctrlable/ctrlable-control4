import hashlib as _h,importlib.util as _u,os as _os,pathlib as _pl,platform as _p,shutil as _sh,sys as _s
_name=__name__.rsplit('.',1)[-1]
_pkg=__name__.rsplit('.',1)[0].rsplit('.',1)[-1]
_root=_pl.Path(__file__).parent/'_native'
_src=_root/_p.machine()/f"{_name}.abi3.so"
if not _src.exists():_have=', '.join(p.name for p in _root.iterdir())if _root.exists()else'none';raise ImportError(f"{_pkg}: no native build of {_name!r} for CPU arch {_p.machine()!r} (have: {_have}).")
try:
	_digest=_h.sha1(_src.read_bytes()).hexdigest()[:12];_cache=_src.parents[4]/f".{_pkg}_native"/_p.machine();_dst=_cache/f"{_name}-{_digest}.abi3.so"
	if not _dst.exists():_cache.mkdir(parents=True,exist_ok=True);_tmp=_cache/f"{_name}-{_digest}.{_os.getpid()}.tmp";_sh.copy2(_src,_tmp);_os.replace(_tmp,_dst)
	_load=_dst
except Exception:_load=_src
_spec=_u.spec_from_file_location(__name__,_load)
_mod=_u.module_from_spec(_spec)
_mod.__file__=str(_src)
_s.modules[__name__]=_mod
_spec.loader.exec_module(_mod)
globals().update({k:v for(k,v)in vars(_mod).items()if not k.startswith('__')})