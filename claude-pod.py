# Makes the claude-pod.png diagram
#
# rerun:
#   cp claude-pod.py d/
#   podman run --rm -it -v 'd:/x' --workdir=/x --entrypoint=/bin/zsh claude-pod
#   apk add  py3-pillow font-dejavu
#   python3 claude-pod.py


from PIL import Image, ImageDraw, ImageFont
S=2
W,H=1600,1100
img=Image.new("RGB",(W*S,H*S),(250,247,242))
d=ImageDraw.Draw(img)
F="/usr/share/fonts/truetype/dejavu/"
def f(n,b=False,m=False):
    name=("DejaVuSansMono" if m else "DejaVuSans")+("-Bold" if b else "")+".ttf"
    return ImageFont.truetype(F+name,n*S)
def R(x0,y0,x1,y1,fill,outline,w=3,r=18,dash=False):
    box=[x0*S,y0*S,x1*S,y1*S]
    d.rounded_rectangle(box,r*S,fill=fill,outline=None if dash else outline,width=w*S)
    if dash:
        L=14
        for x in range(x0+r,x1-r,L*2):
            d.line([x*S,y0*S,min(x+L,x1-r)*S,y0*S],fill=outline,width=w*S); d.line([x*S,y1*S,min(x+L,x1-r)*S,y1*S],fill=outline,width=w*S)
        for y in range(y0+r,y1-r,L*2):
            d.line([x0*S,y*S,x0*S,min(y+L,y1-r)*S],fill=outline,width=w*S); d.line([x1*S,y*S,x1*S,min(y+L,y1-r)*S],fill=outline,width=w*S)
def T(x,y,s,font,fill=(40,40,45),anchor="la"):
    d.text((x*S,y*S),s,font=font,fill=fill,anchor=anchor)
def arrow(x0,y0,x1,y1,col,w=4,label=None,lx=0,ly=0):
    d.line([x0*S,y0*S,x1*S,y1*S],fill=col,width=w*S)
    import math
    a=math.atan2(y1-y0,x1-x0); L=16
    p=[(x1,y1),(x1-L*math.cos(a-0.45),y1-L*math.sin(a-0.45)),(x1-L*math.cos(a+0.45),y1-L*math.sin(a+0.45))]
    d.polygon([(px*S,py*S) for px,py in p],fill=col)
    if label: T(lx,ly,label,f(17,m=True),col)

ORANGE=(217,119,87); ORL=(250,228,218)
BLUE=(70,110,190); BLL=(225,234,250)
GREEN=(60,150,100); GRL=(224,243,231)
RED=(200,70,70); REDL=(250,225,225)
GREY=(110,112,120); GRY=(236,234,230)
PURP=(130,100,190); PRL=(236,229,250)

T(60,40,"claude-pod: Running Claude in Podman containers",f(40,True))
T(60,95,"Problem: 100s of “allow python3 …?” prompts → fatigue → “FFS YES” → oops, on a personal Mac.",f(20),GREY)
def TC(x,y,parts,font):
    for s,c in parts:
        T(x,y,s,font,c); x+=d.textlength(s,font=font)/S
TC(60,125,[("Fix: keep the host Claude on a short leash in ",GREY),("edit",RED),(" or ",GREY),("ask",RED),(" mode, and give the busy work to a disposable container in ",GREY),("auto",RED),(" mode.",GREY)],f(20))

# Mac host
R(40,170,1560,1060,(255,255,255),GREY,3,24)
T(64,184,"🍎 personal Mac mini (host)".replace("🍎 ",""),f(24,True),GREY)

# VSCode claude
R(80,230,520,470,ORL,ORANGE)
T(100,245,"VSCode Claude",f(26,True),ORANGE)
T(100,285,"permission mode: ask",f(19,m=True))
T(100,313,"reads & writes code",f(19))
T(100,341,"shell work → claude-pod exec",f(19))
T(100,381,"can see: ~/.ssh, ~/.claude,",f(17),GREY)
T(100,405,"browser, keychain… (so it asks)",f(17),GREY)

# host-only secrets
R(80,810,520,1020,REDL,RED)
T(100,825,"never mounted in the pod",f(22,True),RED)
for i,s in enumerate(["~/.ssh keys","~/.claude (host Claude's brain)","rest of $HOME, photos, browser"]):
    T(110,868+i*42,"✗ "+s,f(19),RED)

# script
R(80,520,520,760,GRY,GREY)
T(100,535,"claude-pod (bash)",f(24,True))
for i,s in enumerate(["up / exec / down / ports / --build","one container per repo","recreates if image/spec changes","per-repo port digit N:","  container P → 127.0.0.1:N·10000+P"]):
    T(100,576+i*36,s,f(17,m=True))

# VM
R(600,230,1520,1020,PRL,PURP,3,24,dash=True)
T(624,244,"podman machine (Linux VM): only shared dirs are visible",f(22,True),PURP)

# container
R(650,300,1480,780,BLL,BLUE,4)
T(674,316,"claude-<repo>-N   (alpine, lives until reboot)",f(24,True),BLUE)
T(674,358,"claude --permission-mode auto",f(20,m=True))
T(674,388,"GNU coreutils/sed/grep · python3 · node · deno · hugo · caddy",f(17),GREY)
T(674,412,"HOME=/home/claude (throwaway) · CLAUDE_CONFIG_DIR=~/.claude-pod",f(17),GREY)

# mounts
T(674,452,"mounts (at real Mac paths)",f(20,True))
rows=[
    ("current repo","r/w",GREEN),
    ("repo/.git  .claude  .vscode","r/o  ← host executes these",ORANGE),
    ([("$CLAUDE_PODS",ORANGE),(" list of dirs, eg: \"$HOME/work/ $HOME/dev\"",(40,40,45))],"r/o",BLUE),
    ("~/.claude-pod (pod's own login/sessions)","r/w",GREEN)
]
for i,(a,b,c) in enumerate(rows):
    y=490+i*44
    R(674,y,1456,y+36,(255,255,255),c,2,8)
    TC(688,y+8,a if isinstance(a,list) else [(a,(40,40,45))],f(18,m=True))
    T(1440,y+8,b,f(18,True),c,anchor="ra");
T(674,672,"servers bind 0.0.0.0 inside → published on localhost only",f(17),GREY)
T(674,700,".git r/o by default (CLAUDE_POD_GIT_RW=1 to open)",f(17),GREY)
T(674,728,"no tty needed, so host Claude's Bash tool can drive it",f(17),GREY)

# internet
R(1100,850,1480,990,GRL,GREEN)
T(1120,866,"internet egress",f(22,True),GREEN)
T(1120,912,"https only",f(20))
arrow(1290,780,1290,848,GREEN)

# arrows
arrow(300,470,300,518,ORANGE,4,"claude-pod exec 'cmd'",312,482)
arrow(520,640,648,640,GREY,4)
T(532,610,"podman",f(16,m=True),GREY)

# caveat
R(650,830,1060,1000,(255,249,225),(200,150,40))
T(668,846,"remaining gap",f(20,True),(170,120,20))
for i,s in enumerate(["pod can write repo files the","host runs later: .envrc, Makefile,",".venv/bin/python, eslint config"]):
    T(668,880+i*32,s,f(17))

img=img.resize((W,H),Image.LANCZOS)
img.save("claude-pod.png")
