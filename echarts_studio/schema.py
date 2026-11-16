from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class Field:
    path: str; widget: str; default: Any=None; options: tuple=(); minimum: float|int|None=None; maximum: float|int|None=None; step: float|int|None=None; help: str=""; charts: tuple=()
@dataclass(frozen=True)
class Section:
    key: str; label: str; fields: tuple[Field,...]; default_on: bool=True

def F(path,w,default=None,options=(),minimum=None,maximum=None,step=None,help="",charts=()): return Field(path,w,default,tuple(options),minimum,maximum,step,help,tuple(charts))

TEXT_STYLES=(F("color","color","#333333"),F("fontStyle","select","normal",["normal","italic","oblique"]),F("fontWeight","select","normal",["normal","bold","bolder","lighter"]),F("fontFamily","select","sans-serif",["sans-serif","serif","monospace"]),F("fontSize","int",12,minimum=6,maximum=48))
SECTIONS=(
 Section("title","Title",(F("text","text","ECharts Studio"),F("subtext","text",""),F("left","select","left",["auto","left","center","right"]),F("top","text","auto"),F("textStyle.color","color","#333333"),F("textStyle.fontSize","int",18,minimum=8,maximum=48),F("textStyle.fontWeight","select","bolder",["normal","bold","bolder","lighter"]))),
 Section("tooltip","Tooltip",(F("show","bool",True),F("trigger","select","axis",["item","axis","none"]),F("axisPointer.type","select","line",["line","shadow","cross","none"]),F("confine","bool",True),F("enterable","bool",False),F("formatter","text","{b}<br/>{a}: {c}",help="String-template formatters work; JS callbacks do not."))),
 Section("legend","Legend",(F("show","bool",True),F("type","select","plain",["plain","scroll"]),F("orient","select","horizontal",["horizontal","vertical"]),F("left","select","center",["auto","left","center","right"]),F("top","text","8%"),F("align","select","auto",["auto","left","right"]),F("itemGap","int",10,minimum=0,maximum=100))),
 Section("grid","Grid",(F("show","bool",False),F("left","text","3%"),F("right","text","4%"),F("top","text","18%"),F("bottom","text","12%"),F("containLabel","bool",True),F("borderWidth","int",1,minimum=0,maximum=10),F("borderColor","color","#cccccc"))),
 Section("animation","Animation",(F("animation","bool",True),F("animationDuration","int",700,minimum=0,maximum=5000,step=100),F("animationEasing","select","cubicOut",["linear","quadraticIn","quadraticOut","cubicIn","cubicOut","cubicInOut","sinusoidalInOut","elasticOut","bounceOut"]),F("animationDelay","int",0,minimum=0,maximum=3000,step=100))),
 Section("aria","Accessibility / ARIA",(F("enabled","bool",True),),False),
)
AXIS=(F("show","bool",True),F("type","select","category",["category","value","time","log"]),F("position","select","bottom",["top","bottom","left","right"]),F("name","text",""),F("nameLocation","select","end",["start","middle","end"]),F("nameGap","int",15,minimum=0,maximum=100),F("inverse","bool",False),F("boundaryGap","bool",True),F("axisLine.show","bool",True),F("axisLine.symbol","select","none",["none","arrow"]),F("axisLine.lineStyle.color","color","#6e7079"),F("axisLine.lineStyle.width","int",1,minimum=0,maximum=10),F("axisLine.lineStyle.type","select","solid",["solid","dashed","dotted"]),F("axisTick.show","bool",True),F("axisTick.inside","bool",False),F("axisLabel.show","bool",True),F("axisLabel.inside","bool",False),F("axisLabel.rotate","int",0,minimum=-90,maximum=90),F("axisLabel.margin","int",8,minimum=0,maximum=50),F("axisLabel.color","color","#6e7079"),F("axisLabel.fontSize","int",12,minimum=6,maximum=32),F("axisLabel.formatter","text","{value}"),F("splitLine.show","bool",True),F("splitLine.lineStyle.type","select","solid",["solid","dashed","dotted"]),F("splitArea.show","bool",False),F("minorTick.show","bool",False),F("minorSplitLine.show","bool",False))
SERIES_COMMON=(F("silent","bool",False),F("clip","bool",True),F("label.show","bool",False),F("label.position","select","top",["top","left","right","bottom","inside","insideTop","insideBottom"]),F("label.rotate","int",0,minimum=-90,maximum=90),F("label.fontSize","int",12,minimum=6,maximum=32),F("label.color","color","#333333"),F("label.formatter","text","{c}"),F("emphasis.focus","select","series",["none","self","series"]),F("emphasis.disabled","bool",False),F("itemStyle.opacity","float",1.0,minimum=0.0,maximum=1.0,step=.05),F("itemStyle.borderWidth","int",0,minimum=0,maximum=10))
SERIES={
 "line": SERIES_COMMON+(F("smooth","float",0.0,minimum=0,maximum=1,step=.05),F("step","select","off",["off","start","middle","end"]),F("connectNulls","bool",False),F("showSymbol","bool",True),F("symbol","select","emptyCircle",["emptyCircle","circle","rect","roundRect","triangle","diamond","pin","arrow","none"]),F("symbolSize","int",6,minimum=0,maximum=40),F("lineStyle.width","int",2,minimum=0,maximum=10),F("lineStyle.type","select","solid",["solid","dashed","dotted"]),F("areaStyle.opacity","float",0.0,minimum=0,maximum=1,step=.05),F("endLabel.show","bool",False),F("sampling","select","off",["off","lttb","average","min","max","minmax","sum"])),
 "bar": SERIES_COMMON+(F("stack","text",""),F("barWidth","text","60%"),F("barMaxWidth","int",0,minimum=0,maximum=300),F("barMinHeight","int",0,minimum=0,maximum=100),F("barGap","text","30%"),F("barCategoryGap","text","20%"),F("showBackground","bool",False),F("backgroundStyle.color","color","#eeeeee"),F("realtimeSort","bool",False),F("itemStyle.borderRadius","int",0,minimum=0,maximum=50)),
 "scatter": SERIES_COMMON+(F("symbol","select","circle",["circle","rect","roundRect","triangle","diamond","pin","arrow"]),F("symbolSize","int",10,minimum=1,maximum=80),F("large","bool",False),F("largeThreshold","int",2000,minimum=100,maximum=10000)),
}
