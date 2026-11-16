import json
from copy import deepcopy
import pandas as pd
import streamlit as st
from echarts_studio.data import altair_catalog, load_altair, load_upload, profile, kind
from echarts_studio.schema import SECTIONS, AXIS, SERIES
from echarts_studio.options import set_path, prune, merge, sanitize_specials
from echarts_studio.ui import render_fields
from echarts_studio.export import json_text, python_text

st.set_page_config(page_title="ECharts Studio",page_icon="📊",layout="wide",initial_sidebar_state="expanded")
st.title("ECharts Studio")
st.caption("Dataset-aware visual option explorer for Streamlit's native Apache ECharts integration.")

@st.cache_data(show_spinner=False,ttl=3600)
def cached_altair(name): return load_altair(name)

with st.sidebar:
    st.header("Data")
    source=st.radio("Source",["Altair sample dataset","Upload file"],horizontal=False)
    df=None
    if source=="Altair sample dataset":
        try: catalog=altair_catalog()
        except Exception as e: catalog=[]; st.error(f"Could not read Altair dataset catalog: {e}")
        search=st.text_input("Filter sample datasets",placeholder="cars, stocks, barley…")
        matches=[n for n in catalog if search.lower() in n.lower()][:100]
        dataset=st.selectbox("Dataset",matches if matches else catalog, index=None, placeholder="Choose a dataset")
        if dataset:
            try: df=cached_altair(dataset)
            except Exception as e:
                st.error("That Altair dataset could not be downloaded in this environment. Choose another, upload a file, or run locally with internet access.")
                st.caption(str(e))
    else:
        upload=st.file_uploader("CSV, Excel, Parquet or JSON",type=["csv","xlsx","xls","parquet","json"])
        if upload:
            try: df=load_upload(upload)
            except Exception as e: st.error(str(e))
    if df is not None:
        st.dataframe(df.head(25),width="stretch",height=260)
        st.caption(f"{len(df):,} rows × {len(df.columns):,} columns")

if df is None:
    st.info("Choose an Altair sample dataset or upload your own data to start. The app does not ship with hardcoded demo data.")
    st.stop()

cols=list(df.columns); prof=profile(df); numeric=[p.name for p in prof if p.kind=="numeric"]; temporal=[p.name for p in prof if p.kind=="datetime"]; categorical=[p.name for p in prof if p.kind in ("categorical","boolean")]

config,live=st.columns([.95,1.35],gap="large")
with config:
    st.subheader("Build")
    chart_type=st.segmented_control("Series type",["line","bar","scatter"],default="line")
    st.markdown("##### Dataset & encoding")
    use_dataset=st.checkbox("Pass dataframe as dataset.source",True,help="Recommended. Streamlit serializes dataframe-like dataset sources for ECharts.")
    x_default=(temporal+categorical+numeric+cols)[0]
    x=st.selectbox("encode.x",cols,index=cols.index(x_default))
    y_choices=[c for c in numeric if c!=x]
    if chart_type=="scatter":
        y=st.selectbox("encode.y",y_choices,index=0 if y_choices else None)
        ys=[y] if y else []
    else: ys=st.multiselect("Y series",y_choices,default=y_choices[:2])
    tooltip_extra=st.multiselect("Extra tooltip dimensions",[c for c in cols if c not in [x,*ys]])
    size_col=None
    if chart_type=="scatter": size_col=st.selectbox("Optional size dimension",[None]+[c for c in numeric if c not in [x,*ys]])

    option={"dataset":{"source":df}} if use_dataset else {}
    st.markdown("##### Components")
    for sec in SECTIONS:
        with st.expander(sec.label,expanded=False):
            include=st.checkbox(f"Include {sec.label}",sec.default_on,key=f"include:{sec.key}")
            if include:
                obj=render_fields(sec.fields,f"component:{sec.key}")
                if sec.key=="animation": option.update(obj)
                else: option[sec.key]=obj

    for axis in ["xAxis","yAxis"]:
        with st.expander("X axis" if axis=="xAxis" else "Y axis"):
            include=st.checkbox(f"Include {axis}",True,key=f"include:{axis}")
            if include:
                if axis=="xAxis": inferred={"datetime":"time","numeric":"value","categorical":"category","boolean":"category"}[kind(df[x])]; overrides={"type":inferred,"name":str(x),"position":"bottom","boundaryGap":chart_type=="bar"}
                else: overrides={"type":"value","name":"Value","position":"left","boundaryGap":False}
                option[axis]=render_fields(AXIS,f"axis:{axis}",overrides)

    with st.expander("Series styling",expanded=True):
        common=render_fields(SERIES[chart_type],f"series:{chart_type}")
        common=sanitize_specials(prune(common))
        st.caption("Applied to each selected Y series. Data fields stay in encode, styling stays here.")
    with st.expander("Annotations"):
        mark_avg=st.checkbox("markLine: average",False); mark_min=st.checkbox("markPoint: minimum",False); mark_max=st.checkbox("markPoint: maximum",False)
    with st.expander("Data zoom"):
        if st.checkbox("Include dataZoom",False):
            ztypes=st.multiselect("Types",["inside","slider"],default=["inside","slider"]); z0,z1=st.slider("Window (%)",0,100,(0,100)); filter_mode=st.selectbox("filterMode",["filter","weakFilter","empty","none"])
            option["dataZoom"]=[{"type":z,"start":z0,"end":z1,"filterMode":filter_mode} for z in ztypes]
    with st.expander("Toolbox"):
        if st.checkbox("Include toolbox",False):
            feat={}
            if st.checkbox("saveAsImage",True): feat["saveAsImage"]={"name":"echarts-chart"}
            if st.checkbox("restore",True): feat["restore"]={}
            if st.checkbox("dataView",False): feat["dataView"]={"readOnly":True}
            if st.checkbox("magicType",chart_type in ("line","bar")): feat["magicType"]={"type":["line","bar"]}
            option["toolbox"]={"feature":feat}
    with st.expander("Visual map"):
        if st.checkbox("Include visualMap",False):
            vm_dim=st.selectbox("dimension",numeric); vm_type=st.selectbox("type",["continuous","piecewise"]); lo=float(df[vm_dim].min()); hi=float(df[vm_dim].max())
            option["visualMap"]={"type":vm_type,"dimension":vm_dim,"min":lo,"max":hi,"calculable":True,"inRange":{"color":["#313695","#74add1","#fdae61","#a50026"]}}
    with st.expander("Advanced JSON overlay"):
        st.caption("For any JSON-compatible ECharts option that does not yet have a widget. This is merged last.")
        raw=st.text_area("Overlay",'{\n  \n}',height=120)
        if raw.strip() not in ("","{}","{\n  \n}"):
            try: option=merge(option,json.loads(raw))
            except Exception as e: st.error(f"Invalid JSON: {e}")

series=[]
for y in ys:
    s={"name":str(y),"type":chart_type,**deepcopy(common)}
    if use_dataset:
        enc={"x":x,"y":y,"tooltip":[x,y,*tooltip_extra]}
        if size_col: enc["itemName"]=tooltip_extra[0] if tooltip_extra else x
        s["encode"]=enc
    else:
        xv=df[x].dt.strftime("%Y-%m-%dT%H:%M:%S").tolist() if kind(df[x])=="datetime" else df[x].tolist()
        s["data"]=[[a,b] for a,b in zip(xv,df[y].tolist())]
    if mark_avg: s["markLine"]={"data":[{"type":"average","name":"Average"}]}
    pts=[]
    if mark_min: pts.append({"type":"min","name":"Minimum"})
    if mark_max: pts.append({"type":"max","name":"Maximum"})
    if pts: s["markPoint"]={"data":pts}
    series.append(prune(s))
if series: option["series"]=series
option=prune(option)

with live:
    st.subheader("Live preview")
    c1,c2,c3=st.columns(3)
    height=c1.select_slider("Height",[320,400,480,520,600,720],value=520)
    renderer=c2.radio("Renderer",["canvas","svg"],horizontal=True)
    theme=c3.radio("Theme",["streamlit",None],format_func=lambda v:"streamlit" if v else "None",horizontal=True)
    if not ys: st.warning("Select at least one numeric Y field.")
    else:
        try: st.echarts_chart(option,height=height,renderer=renderer,theme=theme,alt=f"{chart_type} chart showing {', '.join(ys)} by {x}")
        except Exception as e: st.error(f"Chart configuration error: {e}")
    tabs=st.tabs(["Option tree","Python","JSON","Data dictionary","Learning notes"])
    display=deepcopy(option)
    if "dataset" in display: display["dataset"]={"source":"<dataframe>"}
    with tabs[0]: st.json(display,expanded=2)
    with tabs[1]:
        st.code(python_text(option),language="python",line_numbers=True)
        st.download_button("Download option.py",python_text(option),"echarts_option.py","text/x-python")
    with tabs[2]:
        j=json_text(option); st.code(j,language="json",line_numbers=True); st.download_button("Download option.json",j,"echarts_option.json","application/json")
    with tabs[3]:
        dd=pd.DataFrame([p.__dict__ for p in prof]); st.dataframe(dd,width="stretch",hide_index=True)
    with tabs[4]:
        st.markdown("""
**How to read this chart**
- `dataset.source` owns the dataframe; `series.encode` maps its named dimensions into visual channels.
- Axes define scales and presentation; series define marks and mark-specific styling.
- Component checkboxes remove whole option branches, making ECharts defaults visible.
- `dataZoom` explores a window over an axis. `visualMap` maps another data dimension into visual properties such as colour.
- Native Streamlit options must remain JSON-compatible. JavaScript callbacks, custom `renderItem`, map registration and ECharts GL are outside this app's native-mode scope.
        """)

st.divider()
with st.expander("Dataset transform lab"):
    st.caption("Use pandas for deterministic preparation, while the chart remains dataset/encode-driven.")
    group=st.selectbox("Group by",[None]+categorical+temporal,key="transform_group")
    measure=st.selectbox("Measure",numeric,key="transform_measure")
    agg=st.selectbox("Aggregation",["sum","mean","median","min","max","count"],key="transform_agg")
    if group:
        transformed=df.groupby(group,dropna=False)[measure].agg(agg).reset_index()
        st.dataframe(transformed.head(50),width="stretch",hide_index=True)
        st.caption("This lab is intentionally separate: it teaches the boundary between dataframe preparation and ECharts presentation.")
