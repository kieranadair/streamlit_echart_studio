import pandas as pd
from echarts_studio.data import kind, profile
from echarts_studio.options import set_path, merge, sanitize_specials

def test_kinds():
    assert kind(pd.Series([1,2]))=="numeric"
    assert kind(pd.Series(["a","b"]))=="categorical"
def test_set_path():
    d={}; set_path(d,"label.fontSize",12); assert d=={"label":{"fontSize":12}}
def test_merge(): assert merge({"a":{"b":1}},{"a":{"c":2}})=={"a":{"b":1,"c":2}}
def test_specials():
    d=sanitize_specials({"step":"off","sampling":"off","stack":"","barMaxWidth":0}); assert d=={"step":False}
def test_profile(): assert profile(pd.DataFrame({"x":[1,None]}))[0].nulls==1
