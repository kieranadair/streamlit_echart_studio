from __future__ import annotations
import json

def jsonable_option(option):
    def conv(v):
        try:
            import pandas as pd
            if isinstance(v,pd.DataFrame): return v.to_dict(orient="records")
        except Exception: pass
        if isinstance(v,dict): return {k:conv(x) for k,x in v.items()}
        if isinstance(v,list): return [conv(x) for x in v]
        return v
    return conv(option)

def json_text(option): return json.dumps(jsonable_option(option),indent=2,default=str)
def python_text(option):
    display=dict(option)
    if "dataset" in display: display={**display,"dataset":{"source":"__DF__"}}
    txt=json.dumps(display,indent=2,default=str).replace('"__DF__"','df')
    return "option = "+txt+"\n\nst.echarts_chart(option, height=520)\n"
