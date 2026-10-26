from common import *
W,H=1560,1080
LH=21; FS=10.2
BLUE=("#2f3d8a","#e8ebf7"); STUB=("#8a6a1c","#fbf3dc"); GRAY=("#555","#f0f0f0"); GREEN=("#3b6b38","#e6efe2")
def cls(ax,x,y,w,name,attrs,meths,col=BLUE,stereo=None):
    ec,fc=col
    hh=34+(14 if stereo else 0)
    ha=LH*len(attrs)+10 if attrs else 0
    hm=LH*len(meths)+10 if meths else 0
    h=hh+ha+hm
    box(ax,x,y,w,h,fc="white",ec=ec,lw=1.8,r=3)
    ax.add_patch(plt.Rectangle((x,y),w,hh,fc=fc,ec=ec,lw=1.8,zorder=2))
    if stereo:
        txt(ax,x+w/2,y+13,stereo,size=9.5,style="italic",color="#555",fit=(x,y,x+w,y+hh),name=name+" st")
        txt(ax,x+w/2,y+hh-14,name,size=12.5,weight="bold",color=ec,fit=(x,y,x+w,y+hh),name=name)
    else:
        txt(ax,x+w/2,y+hh/2,name,size=12.5,weight="bold",color=ec,fit=(x,y,x+w,y+hh),name=name)
    yy=y+hh
    for i,a in enumerate(attrs):
        txt(ax,x+9,yy+5+LH*(i+0.5),a,size=FS,ha="left",fit=(x,yy,x+w,yy+ha),name=name+": "+a)
    yy+=ha
    if attrs and meths: ax.plot([x,x+w],[yy,yy],color=ec,lw=1.4,zorder=3)
    for i,a in enumerate(meths):
        txt(ax,x+9,yy+5+LH*(i+0.5),a,size=FS,ha="left",fit=(x,yy,x+w,yy+hm),name=name+": "+a)
    return dict(x=x,y=y,w=w,h=h,r=x+w,b=y+h,cx=x+w/2,cy=y+h/2)
def line(ax,pts,ls="-",head=None,lw=1.5,color="#333"):
    if head: arrow(ax,pts,color=color,lw=lw,ls=ls,ms=14,style="-|>" if head=="filled" else "->")
    else: ax.plot([p[0] for p in pts],[p[1] for p in pts],color=color,lw=lw,ls=ls,zorder=3)
def make(outdir):
    fig,ax=canvas(W,H)
    DASH=(0,(5,3))
    sim=cls(ax,20,15,260,"SimulationLine",["line : AgroDroneLine","timer : TimeManager"],["tick(elapsed_time)"])
    tm=cls(ax,380,15,330,"TimeManager",["acceleration_factor = 10⁴","tick_interval = 0.01 s (100 Hz)","current_time : float"],["start() / stop()","tick(): Δt = base × accel"],stereo="«thread»")
    fsm=cls(ax,1010,15,500,"FSM states",["NodeState: IDLE | WAITING_FOR_RES | WORKING |","    MAINT | REPAIR | FAILURE","OperationState: IDLE | WAITING | EXECUTING |","    LETUP | BLOCKED"],[],col=GRAY,stereo="«enumerations»")
    y2=250
    adl=cls(ax,20,y2,340,"AgroDroneLine",["units : List[ProductionNode] {26}","res_manager : ResourceManager","planner : ProductionPlanner","lim_drones_made : int","memory_points : List[float]"],["initialize_units() / init_resources()","getResourcesForOneDrone() // BOM","tick(t) / plot_history()"])
    pp=cls(ax,430,y2,320,"ProductionPlanner",["resource_limits : dict // BOM","limit_drones : int","get_state / get_reserved : delegates"],["process_request(req) : bool"])
    rm=cls(ax,900,y2,330,"ResourceManager",["resources : dict[str, ResourcePool]","requests : List[RequestRes]","agent : ResourceAgent | None"],["add_resource() / add_requests()","tick() // aging-priority dispatch"])
    ra=cls(ax,1330,y2,215,"ResourceAgent",[],["dispatch_requests()","get_resource()"],col=STUB,stereo="«stub · DQN hook»")
    y3=520
    pn=cls(ax,20,y3,355,"ProductionNode",["id, description","reliability : Reliability","status : NodeState // FSM","operations : List[ProductionOperation]","state_durations : dict[NodeState, s]","produced / defects / reserved : dict","agentNode : NodeAgent | None","memory : List[dict]"],["tick(t, is_point) // FSM logic","evaluate_efficiency() / _reliability()"])
    na=cls(ax,500,y3,235,"NodeAgent",[],["tick(t) / evaluate()","init/complete_operation()"],col=STUB,stereo="«stub · DQN hook»")
    po=cls(ax,830,y3,340,"ProductionOperation",["name : str // output resource type","input_resources : dict[str, int]","duration / duration_letup : s","efficiency : Efficiency","state : OperationState // FSM","time_work : float","memory : List[dict]"],["create_resource(node_id)","callback(resources)"])
    rs=cls(ax,1250,y3-30,295,"Resources",["BaseResource (name, id)","   – PurchasedResource","   – ManufacturedResource","(source_resources genealogy,","    node_id)","ResourcePool: bulk float | List","RequestRes: input_resources,","    wait_ticks, callback"],[],col=GREEN)
    y4=880
    rel=cls(ax,20,y4,370,"Reliability",["design: repairability, longevity, …","failure_frequency : TD-Exponential","maintenance_interval : TD-LogNormal","reliability : TD-Exponential","emergency_response : Constant"],["get(time_work) : dict // sample"])
    eff=cls(ax,470,y4,420,"Efficiency",["design: productivity, utilization_rate, …","schedule_accuracy ~ N(m, s)","defect_rate ~ N(m, s); stability ~ U(a, b)","power_usage ↑, maintenance_cost ↑,","profitability ↓, reconfiguration_speed ↓, …"],["get(time_work) : dict // sample"])
    dw=cls(ax,975,y4,340,"Distribution wrappers",["Normal / Uniform / LogNormal / Expon","TimeDependentExponential:","λ(t) = λ₀(1 + αt) // ageing","TimeDependentLogNormal: μ(t) = μ₀ − αt","Increasing / Decreasing / Constant"],["sample(time_work) : float"])
    # ── relations ──
    def lab(x,y,s,ha="center",**k): txt(ax,x,y,s,size=10,style="italic",color="#333",ha=ha,**k)
    # SimulationLine — TimeManager
    line(ax,[(sim["r"],60),(tm["x"],60)]); lab((sim["r"]+tm["x"])/2,46,"1")
    # SimulationLine — AgroDroneLine
    line(ax,[(sim["cx"],sim["b"]),(sim["cx"],adl["y"])]); lab(sim["cx"]+12,(sim["b"]+adl["y"])/2,"1",ha="left")
    # AgroDroneLine — ProductionPlanner
    yl=y2+70
    line(ax,[(adl["r"],yl),(pp["x"],yl)]); lab((adl["r"]+pp["x"])/2,yl-13,"1")
    # AgroDroneLine — ResourceManager (route above planner)
    yr=y2-22
    line(ax,[(adl["x"]+270,adl["y"]),(adl["x"]+270,yr),(rm["x"]+60,yr),(rm["x"]+60,rm["y"])]); lab(rm["x"]+72,yr+12,"1",ha="left")
    # Planner ⇢ ResourceManager
    yp=y2+130
    line(ax,[(pp["r"],yp),(rm["x"],yp)],ls=DASH,head="open"); lab((pp["r"]+rm["x"])/2,yp-13,"add_requests")
    # ResourceAgent hook
    yh=y2+60
    line(ax,[(ra["x"],yh),(rm["r"],yh)],ls=DASH,head="open"); lab((ra["x"]+rm["r"])/2,yh-13,"hook")
    # AgroDroneLine — ProductionNode
    line(ax,[(adl["cx"],adl["b"]),(adl["cx"],pn["y"])]); lab(adl["cx"]+12,(adl["b"]+pn["y"])/2,"1..26",ha="left")
    # NodeAgent hook
    yh2=y3+75
    line(ax,[(na["x"],yh2),(pn["r"],yh2)],ls=DASH,head="open"); lab((na["x"]+pn["r"])/2,yh2-13,"hook")
    # ProductionNode — ProductionOperation (passes under NodeAgent)
    ypo=na["b"]+40
    line(ax,[(pn["r"],ypo),(po["x"],ypo)]); lab((pn["r"]+po["x"])/2+60,ypo-13,"1..*")
    # RM ⇢ ProductionOperation create_resource()
    xc=rm["x"]+70
    line(ax,[(xc,rm["b"]),(xc,po["y"])],ls=DASH,head="open"); lab(xc+10,(rm["b"]+po["y"])/2,"create_resource()",ha="left")
    # RM → Resources (route right of RM below the stub)
    yq=rm["b"]-18
    line(ax,[(rm["r"],yq),(rs["cx"],yq),(rs["cx"],rs["y"])],head="filled",lw=2)
    # ProductionNode → Reliability
    line(ax,[(pn["x"]+60,pn["b"]),(pn["x"]+60,rel["y"])],head="filled"); lab(pn["x"]+72,(pn["b"]+rel["y"])/2,"1",ha="left")
    # ProductionOperation → Efficiency
    xo=860
    line(ax,[(xo,po["b"]),(xo,eff["y"])],head="filled"); lab(xo+10,(po["b"]+eff["y"])/2,"1",ha="left")
    # Reliability ⇢ Efficiency, Efficiency ⇢ Distribution wrappers (use)
    yd=y4+60
    line(ax,[(rel["r"],yd),(eff["x"],yd)],ls=DASH,head="open")
    line(ax,[(eff["r"],yd),(dw["x"],yd)],ls=DASH,head="open"); lab((eff["r"]+dw["x"])/2,yd-13,"use")
    check(fig,ax)
    print("bottom of lowest box:",max(rel["b"],eff["b"],dw["b"]),"canvas H",H)
    save(fig,"fig3_class_diagram",outdir); plt.close(fig)
if __name__=="__main__": make("out")
