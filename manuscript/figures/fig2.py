from common import *
import sys
W,H=1610,960
# Last note (agreed 2026-10-26): GNN output goes to Task2 (action space, Table 5 row 6) and Task7 (topological state input, Table 5 row 7; rho(Task2)=rho(Task7)={GNN})
LAST_NOTE=sys.argv[1] if len(sys.argv)>1 else "Task$_2$ and the\nstate input of Task$_7$"
def make(outdir,last=LAST_NOTE,name="fig2_closed_loop"):
    fig,ax=canvas(W,H)
    R=("#8a3326","#f6e1df"); B=("#232d73","#e1e5f6"); G=("#3b6b38","#e3ecdf"); A=("#7d5e14","#f3ecd7")
    d=40  # shift of the middle block
    cx=785+d
    # M1
    box(ax,36,40,372,215,fc=R[1],ec=R[0],lw=2.2)
    txt(ax,222,92,"Mechanism 1\nGenetic Algorithm (GA)",size=16.5,weight="bold",color=R[0],fit=(36,40,408,255),name="M1 title")
    txt(ax,222,168,"structural & behavioral\nnode design (Task$_1$)",size=13.5,fit=(36,40,408,255),name="M1 body")
    txt(ax,222,224,"distributions of reliability and\nefficiency parameters of nodes",size=11.5,style="italic",fit=(36,40,408,255),name="M1 note")
    txt(ax,36,330,"statistical distributions of E, T and\nreliability parameters initialize the\nrandom-event generators of the\ndigital twin",size=11.5,ha="left",fit=(36,270,470,400),name="M1 side")
    # M3
    x3=480+d
    box(ax,x3,40,610,345,fc=B[1],ec=B[0],lw=2.2)
    txt(ax,cx,72,"Mechanism 3 — DQN agent",size=17.5,weight="bold",color="#1d2766",fit=(x3,40,x3+610,385),name="M3 title")
    txt(ax,cx,116,"seven operational tasks: Task$_2$–Task$_5$, Task$_7$–Task$_9$",size=13.5,fit=(x3,40,x3+610,385),name="M3 sub")
    box(ax,x3+30,145,548,95,fc="white",ec=B[0],lw=2,ls=(0,(4,3)),r=6)
    txt(ax,cx-1,168,"Digital twin (training environment)",size=14,weight="bold",fit=(x3+30,145,x3+578,240),name="DT title")
    txt(ax,cx-1,208,"stochastic simulation: node topology, material and\ninformation flows, reliability distributions",size=11.5,fit=(x3+30,145,x3+578,240),name="DT body")
    box(ax,x3+30,252,258,84,fc="white",ec=B[0],lw=2,r=6)
    txt(ax,x3+159,294,"Q-network +\ntarget network",size=13.5,weight="bold",fit=(x3+30,252,x3+288,336),name="Q")
    box(ax,x3+320,252,258,84,fc="white",ec=B[0],lw=2,r=6)
    txt(ax,x3+449,294,"Replay buffer\nexperience (s, a, r, s′)",size=13,weight="bold",fit=(x3+320,252,x3+578,336),name="RB")
    txt(ax,cx,362,"Integral reward R = Σ w$_i$·r$_i$ aggregates the partial effects of all seven tasks",size=11.5,style="italic",fit=(x3,342,x3+610,385),name="reward")
    # M4
    x4=1280
    box(ax,x4,40,310,215,fc=G[1],ec=G[0],lw=2.2)
    txt(ax,x4+155,92,"Mechanism 4\nGraph Neural Network",size=15.5,weight="bold",color=G[0],fit=(x4,40,x4+310,255),name="M4 title")
    txt(ax,x4+155,168,"topology-aware scaling\n(Task$_6$)",size=13.5,fit=(x4,40,x4+310,255),name="M4 body")
    txt(ax,x4+155,224,"graph model of the line,\nload-redistribution recommendations",size=11,style="italic",fit=(x4,40,x4+310,255),name="M4 note")
    txt(ax,x4,336,"node loads and topology from solved\nTask$_2$/Task$_7$ instances form the\nGNN training set",size=11.5,ha="left",fit=(x4,280,W,390),name="M4 side1")
    txt(ax,x4,432,"scaling recommendations return to the\naction space of "+last,size=11.5,ha="left",fit=(x4,400,W,470),name="M4 side2")
    # arrows GA->DQN, DQN<->GNN (labels sit above/below the arrows inside the gaps)
    arrow(ax,[(408,145),(x3-2,145)],lw=3,ms=20); txt(ax,(408+x3)/2,120,"GA → DQN",size=11.5,weight="bold",fit=(408,100,x3,140),name="GA->DQN")
    xe=x3+610
    arrow(ax,[(xe+2,105),(x4-2,105)],lw=3,ms=20); txt(ax,(xe+x4)/2,82,"DQN → GNN",size=11,weight="bold",color="#111",fit=(xe,60,x4,100),name="DQN->GNN")
    arrow(ax,[(x4-2,180),(xe+2,180)],lw=3,ms=20,color=G[0]); txt(ax,(xe+x4)/2,203,"GNN → DQN",size=11,weight="bold",color=G[0],fit=(xe,185,x4,225),name="GNN->DQN")
    # closed cycle
    box(ax,36,495,372,160,fc="white",ec="#888",lw=2,ls=(0,(4,3)),r=8)
    txt(ax,222,535,"Closed optimization cycle",size=14.5,weight="bold",fit=(36,495,408,655),name="cycle t")
    txt(ax,222,598,"GA → digital twin → DQN ↔ AIC → GNN\nwith GNN recommendations returned\nto the DQN action space",size=11.5,fit=(36,495,408,655),name="cycle b")
    # AIC
    box(ax,x3,540,610,160,fc=A[1],ec=A[0],lw=2.2)
    txt(ax,cx,572,"Mechanism 2 — Artificial Intelligence Complex (AIC)",size=14,weight="bold",color=A[0],fit=(x3+12,540,x3+598,700),name="AIC title")
    txt(ax,cx,635,"edge devices: CNN (spectral features), RNN/LSTM (time series);\nindirect reliability assessment (Task$_{10}$); master–slave modules",size=12,fit=(x3,540,x3+610,700),name="AIC body")
    # DQN <-> AIC arrows
    ax1,ax2=cx-50,cx+45
    arrow(ax,[(ax1,538),(ax1,387)],lw=3.2,ms=20); arrow(ax,[(ax2,387),(ax2,538)],lw=3.2,ms=20)
    txt(ax,ax1-14,438,"AIC → DQN",size=12,weight="bold",ha="right")
    txt(ax,ax1-14,486,"real-time state vector $\\mathit{s}_t$\nsynchronizes the digital twin",size=11.5,ha="right")
    txt(ax,ax2+14,438,"DQN → AIC",size=12,weight="bold",ha="left")
    txt(ax,ax2+14,486,"control commands $\\mathit{a}_t$\nexecuted via slave modules",size=11.5,ha="left")
    # physical
    yp=800
    box(ax,x3,yp,610,125,fc="#eeeeee",ec="#666",lw=2.2)
    txt(ax,cx,yp+38,"Physical production line",size=16.5,weight="bold",fit=(x3,yp,x3+610,yp+125),name="phys t")
    txt(ax,cx,yp+88,"nodes, warehouse, material flows",size=13.5,fit=(x3,yp,x3+610,yp+125),name="phys b")
    s1,s2=cx-130,cx+130
    arrow(ax,[(s1,yp-2),(s1,702)],lw=3.2,ms=20); arrow(ax,[(s2,702),(s2,yp-2)],lw=3.2,ms=20)
    txt(ax,s1-14,751,"sensor signals",size=11.5,ha="right")
    txt(ax,s2+14,751,"actuation",size=11.5,ha="left")
    txt(ax,cx,751,"cyber-physical\ncontrol loop",size=11.5,style="italic",color="#333",fit=(s1+10,705,s2-10,798),name="loop")
    check(fig,ax); save(fig,name,outdir); plt.close(fig)
if __name__=="__main__": make("out")
