from common import *
W,H=1389,1023
def make(outdir):
    fig,ax=canvas(W,H)
    for x,s in [(155,"HIERARCHY LEVEL"),(706,"AI MECHANISM"),(1225,"TASKS OWNED, μ(t)")]:
        txt(ax,x,36,s,size=15,weight="bold",color="#333")
    cols={"gnn":("#3b6b38","#e3ecdf"),"dqn":("#2f3d8a","#e1e5f6"),"aic":("#8a6a1c","#f3ecd7"),"ga":("#8a3326","#f6e1df")}
    rows=[
     ("gnn",70,190,"Production network","strategic level:\nscaling decisions",
      "Mechanism 4 — Graph Neural Network (GNN)",
      "Topology-aware scaling of production:\ngraph model of the line, load-redistribution recommendations",
      "trained on digital-twin data with known balancing outcomes","Task$_6$","|T$_{GNN}$| = 1"),
     ("dqn",301,207,"Production line","operational level:\nreal-time control",
      "Mechanism 3 — Deep Q-Network (DQN) agent",
      "Single multi-task agent trained in the digital-twin environment;\njointly solves seven interdependent operational tasks",
      "integral reward R = Σ w·r aggregates the partial effects of all tasks;\ndigital twin: stochastic simulation of topology, flows and reliability distributions",
      "Task$_2$–Task$_5$,\nTask$_7$–Task$_9$","|T$_{DQN}$| = 7"),
     ("aic",549,190,"Node condition","sensing level:\nedge devices",
      "Mechanism 2 — Artificial Intelligence Complex (AIC)",
      "Edge-level signal analysis: CNN for spectral features, RNN/LSTM for time series;\nindirect reliability assessment of nodes without taking them out of service",
      "master–slave architecture; executes agent commands via slave modules","Task$_{10}$","|T$_{AIC}$| = 1"),
     ("ga",780,190,"Node","design level",
      "Mechanism 1 — Genetic Algorithm (GA)",
      "Structural and behavioral design of the node: chromosome\nencodes design and behavioral genes; multi-objective fitness F(x)\nunder constraints g$_i$(x) ≤ 0",
      None,"Task$_1$","|T$_{GA}$| = 1"),
    ]
    for key,y,h,lvl,lvl2,title,body,note,task,card in rows:
        ec,fc=cols[key]
        box(ax,36,y,237,h,fc="#f2f2f2",ec="#999",lw=1.6)
        txt(ax,154,y+h*0.30,lvl,size=15,weight="bold",color="#111",fit=(36,y,273,y+h),name=lvl)
        txt(ax,154,y+h*0.66,lvl2,size=12.5,color="#444",fit=(36,y,273,y+h))
        box(ax,315,y,783,h,fc=fc,ec=ec,lw=2.2)
        if note is None:
            ty,by=y+h*0.20,y+h*0.60
        else:
            ty,by,ny=y+h*0.18,y+h*0.47,y+h*0.80
            txt(ax,706,ny,note,size=11,style="italic",color="#333",fit=(315,y,1098,y+h),name=title+" note")
        txt(ax,706,ty,title,size=16.5,weight="bold",color=ec,fit=(315,y,1098,y+h),name=title)
        txt(ax,706,by,body,size=13,color="#1a1a1a",fit=(315,y,1098,y+h),name=title+" body")
        box(ax,1117,y,226,h,fc="white",ec=ec,lw=2.2)
        tl=task.count("\n")
        txt(ax,1230,y+h*(0.36 if tl==0 else 0.33),task,size=16.5,weight="bold",fit=(1117,y,1343,y+h),name=task)
        txt(ax,1230,y+h*0.72,card,size=14,color="#444",fit=(1117,y,1343,y+h))
    # arrows between rows
    labs=[(260,301,"learned topological model, node loads (Task$_2$/Task$_7$)"),
          (508,549,"real-time state vector $\\mathit{s}_t$ synchronizes the digital twin"),
          (739,780,"distributions of efficiency and reliability parameters")]
    for y0,y1,l in labs:
        arrow(ax,[(706,y1-2),(706,y0+2)],lw=3.2,ms=22)
        txt(ax,771,(y0+y1)/2,l,size=12.5,style="italic",ha="left",color="#222")
    check(fig,ax); save(fig,"fig1_hierarchy",outdir); plt.close(fig)
if __name__=="__main__": make("out")
