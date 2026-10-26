import csv,collections,sys
from common import *
import numpy as np
CSV=sys.argv[1] if len(sys.argv)>1 else "experiments/raw/results_full_20260911.csv"
def make(outdir,csvpath=CSV):
    rows=list(csv.DictReader(open(csvpath,encoding="utf-8")))
    g=collections.OrderedDict()
    for r in rows:
        g.setdefault(float(r["T_pm"]),[]).append(r)
    ks=sorted(g); assert len(ks)==8 and all(len(g[k])==20 for k in ks)
    mk=[[float(r["makespan_s"])/1e6 for r in g[k]] for k in ks]
    av=[[float(r["availability_print_park"])*100 for r in g[k]] for k in ks]
    labels=[f"{int(k/1000)}k" for k in ks]
    fig,axs=plt.subplots(1,2,figsize=(13.5,4.9))
    def bx(ax,data):
        bp=ax.boxplot(data,positions=range(1,9),widths=0.5,patch_artist=True,showfliers=True,
            medianprops=dict(color="#2b2b2b",lw=2),whiskerprops=dict(color="#1f4e79",lw=1.4),capprops=dict(color="#1f4e79",lw=1.4),
            boxprops=dict(facecolor="#4f81ad",edgecolor="#1f4e79",lw=1.4,alpha=0.95),
            flierprops=dict(marker="o",markersize=3.5,markerfacecolor="#aaaaaa",markeredgecolor="#aaaaaa"))
        ax.scatter(range(1,9),[np.mean(d) for d in data],marker="D",s=42,color="#c0440c",zorder=5,label="mean")
        ax.set_xticks(range(1,9)); ax.set_xticklabels(labels)
        ax.set_xlabel("Preventive maintenance interval, T$_{pm}$ (s)",fontsize=11.5)
        ax.grid(axis="y",color="#dddddd",lw=1); ax.set_axisbelow(True)
        for s in ("top","right"): ax.spines[s].set_visible(False)
    bx(axs[0],mk); axs[0].set_ylabel("Makespan, ×10$^6$ s",fontsize=11.5)
    axs[0].set_title("(a) Batch completion time for 10 drones",fontsize=12.5)
    bx(axs[1],av); axs[1].set_ylabel("3D-printing-park availability, %",fontsize=11.5)
    axs[1].set_title("(b) 3D-printing-park availability",fontsize=12.5)
    from matplotlib.lines import Line2D
    h=[Line2D([0],[0],color="#2b2b2b",lw=2,label="median"),Line2D([0],[0],marker="D",color="w",markerfacecolor="#c0440c",markersize=8,label="mean")]
    fig.legend(handles=h,loc="lower center",ncol=2,frameon=False,fontsize=11,bbox_to_anchor=(0.5,-0.01))
    fig.tight_layout(rect=(0,0.06,1,1))
    save(fig,"fig4_tpm_study",outdir); plt.close(fig)
    print("medians makespan:",[round(float(np.median(d)),3) for d in mk]); print("mean avail %:",[round(float(np.mean(d)),2) for d in av])
if __name__=="__main__": make("out")
