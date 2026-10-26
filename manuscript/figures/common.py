import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams.update({"font.family":"DejaVu Sans","mathtext.default":"regular","mathtext.fontset":"dejavusans"})

WARN=[]
def canvas(W,H,dpi_px=100):
    fig=plt.figure(figsize=(W/dpi_px,H/dpi_px))
    ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,W); ax.set_ylim(H,0); ax.axis("off")
    return fig,ax
def box(ax,x,y,w,h,fc="white",ec="#333",lw=1.6,ls="-",r=8,z=1):
    p=FancyBboxPatch((x,y),w,h,boxstyle=f"round,pad=0,rounding_size={r}",fc=fc,ec=ec,lw=lw,ls=ls,zorder=z)
    ax.add_patch(p); return p
def txt(ax,x,y,s,size=11,color="#222",weight="normal",style="normal",ha="center",va="center",z=5,ls=1.25,fit=None,name=""):
    t=ax.text(x,y,s,fontsize=size,color=color,fontweight=weight,fontstyle=style,ha=ha,va=va,zorder=z,linespacing=ls)
    if fit: WARN.append((t,fit,name or s[:30]))
    return t
def arrow(ax,pts,color="#333",lw=2.2,ls="-",head=True,style="-|>",ms=16,z=4):
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    if len(pts)>2 or not head:
        end=pts[-1]; prev=pts[-2]
        ax.plot(xs[:-1]+[end[0]] if not head else xs[:-1]+[prev[0]+(end[0]-prev[0])*0.001], ys[:-1]+[end[1]] if not head else ys[:-1]+[prev[1]+(end[1]-prev[1])*0.001],color=color,lw=lw,ls=ls,zorder=z,solid_capstyle="butt")
        if head:
            ax.add_patch(FancyArrowPatch(prev,end,arrowstyle=style,mutation_scale=ms,lw=lw,color=color,shrinkA=0,shrinkB=0,zorder=z,ls="-"))
    else:
        ax.add_patch(FancyArrowPatch(pts[0],pts[1],arrowstyle=style,mutation_scale=ms,lw=lw,color=color,shrinkA=0,shrinkB=0,zorder=z,ls=ls))
def check(fig,ax):
    fig.canvas.draw(); r=fig.canvas.get_renderer(); inv=ax.transData.inverted()
    bad=0
    for t,(x0,y0,x1,y1),name in WARN:
        bb=t.get_window_extent(r); (a,b),(c,d)=inv.transform((bb.x0,bb.y0)),inv.transform((bb.x1,bb.y1))
        xl,xr=min(a,c),max(a,c); yt,yb=min(b,d),max(b,d)
        if xl<x0-0.5 or xr>x1+0.5 or yt<y0-0.5 or yb>y1+0.5:
            bad+=1; print(f"  OVERFLOW {name!r}: text x[{xl:.0f},{xr:.0f}] y[{yt:.0f},{yb:.0f}] box x[{x0:.0f},{x1:.0f}] y[{y0:.0f},{y1:.0f}]")
    WARN.clear(); print("  fit check:",bad,"overflows")
def save(fig,name,outdir,dpi=600):
    import os; os.makedirs(outdir,exist_ok=True)
    fig.savefig(f"{outdir}/{name}.png",dpi=dpi,facecolor="white")
    fig.savefig(f"{outdir}/{name}.svg",facecolor="white")
    fig.savefig(f"{outdir}/{name}.pdf",facecolor="white")
