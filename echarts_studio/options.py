from __future__ import annotations
from copy import deepcopy

def set_path(root,path,value):
    cur=root; bits=path.split(".")
    for b in bits[:-1]: cur=cur.setdefault(b,{})
    cur[bits[-1]]=value

def prune(v):
    if isinstance(v,dict): return {k:prune(x) for k,x in v.items() if x is not None}
    if isinstance(v,list): return [prune(x) for x in v if x is not None]
    return v

def merge(a,b):
    out=deepcopy(a)
    for k,v in b.items():
        if isinstance(v,dict) and isinstance(out.get(k),dict): out[k]=merge(out[k],v)
        else: out[k]=deepcopy(v)
    return out

def sanitize_specials(s):
    if s.get("step")=="off": s["step"]=False
    if s.get("sampling")=="off": s.pop("sampling",None)
    if s.get("stack")=="": s.pop("stack",None)
    if s.get("barMaxWidth")==0: s.pop("barMaxWidth",None)
    return s
