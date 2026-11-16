from __future__ import annotations
import streamlit as st
from .options import set_path

def render_field(f,key,override=None):
    d=f.default if override is None else override; h=f.help or None; label=f.path
    if f.widget=="bool": return st.checkbox(label,value=bool(d),key=key,help=h)
    if f.widget=="text": return st.text_input(label,value=str(d),key=key,help=h)
    if f.widget=="color": return st.color_picker(label,value=str(d),key=key,help=h)
    if f.widget=="select":
        d=d if d in f.options else f.options[0]; return st.selectbox(label,f.options,index=f.options.index(d),key=key,help=h)
    if f.widget=="int": return st.slider(label,int(f.minimum),int(f.maximum),int(d),int(f.step or 1),key=key,help=h)
    if f.widget=="float": return st.slider(label,float(f.minimum),float(f.maximum),float(d),float(f.step or .1),key=key,help=h)
    raise ValueError(f.widget)

def render_fields(fields,key_prefix,overrides=None):
    obj={}; overrides=overrides or {}
    for f in fields: set_path(obj,f.path,render_field(f,f"{key_prefix}:{f.path}",overrides.get(f.path)))
    return obj
