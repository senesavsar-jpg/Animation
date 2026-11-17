import numpy as np, wave, json
sr=48000; T=35.0; n=int(sr*T); t=np.arange(n)/sr
bpm=96; beat=60/bpm
rng=np.random.default_rng(7)
def note(m): return 440*2**((m-69)/12)
mix=np.zeros((n,2))
# chords Am F C G (2 bars each = 8 beats? use 4 beats per chord)
prog=[[57,60,64,69],[53,57,60,65],[48,55,60,64],[55,59,62,67]]
chord_len=4*beat
for k in range(int(T/chord_len)+1):
    c=prog[k%4]; s=int(k*chord_len*sr); e=min(n,int((k+1)*chord_len*sr)+int(0.3*sr))
    if s>=n: break
    tt=np.arange(e-s)/sr
    env=np.minimum(1,tt/0.6)*np.exp(-np.maximum(0,tt-chord_len)/0.25)
    pad=sum(np.sin(2*np.pi*note(m)*tt+0.3*np.sin(2*np.pi*0.3*tt))+0.3*np.sin(2*np.pi*note(m)*2.003*tt) for m in c)
    pad*=env*0.045
    mix[s:e,0]+=pad*(1+0.2*np.sin(2*np.pi*0.2*tt)); mix[s:e,1]+=pad*(1-0.2*np.sin(2*np.pi*0.2*tt))
    # bass
    tb=tt; b=np.sin(2*np.pi*note(c[0]-12)*tb)*np.exp(-tb/1.2)*0.16
    mix[s:e,:]+=b[:,None]
    # arp plucks 8ths
    for j in range(8):
        ps=s+int(j*beat/2*sr); 
        if ps>=n: break
        L=min(int(0.35*sr),n-ps); tp=np.arange(L)/sr
        m=c[[0,2,1,3,2,1,3,2][j]]+12
        pl=(np.sin(2*np.pi*note(m)*tp)*np.exp(-tp/0.12))*0.05
        pan=0.5+0.35*np.sin(j)
        mix[ps:ps+L,0]+=pl*(1-pan); mix[ps:ps+L,1]+=pl*pan
# drums start after hook at 3.0s
nb=int(T/beat)
for b in range(nb):
    bt=b*beat
    if bt<3.05 or bt>33.6: continue
    s=int(bt*sr)
    if b%2==0:  # kick
        L=min(int(0.4*sr),n-s); tk=np.arange(L)/sr
        f=50+90*np.exp(-tk/0.04); ph=2*np.pi*np.cumsum(f)/sr
        mix[s:s+L,:]+=(np.sin(ph)*np.exp(-tk/0.18)*0.42)[:,None]
    else:  # soft clap/snare
        L=min(int(0.25*sr),n-s); tk=np.arange(L)/sr
        sn=rng.standard_normal(L)*np.exp(-tk/0.06)*0.10
        mix[s:s+L,:]+=sn[:,None]
    for h in (0,0.5):  # hats
        hs=int((bt+h*beat+beat*0.25)*sr)
        if hs>=n: continue
        L=min(int(0.05*sr),n-hs); th=np.arange(L)/sr
        hn=np.diff(rng.standard_normal(L+1))*np.exp(-th/0.012)*0.035
        mix[hs:hs+L,0]+=hn*0.7; mix[hs:hs+L,1]+=hn
# fade out
mix*=np.clip((T-t)/1.2,0,1)[:,None]
def save(name,x):
    x=x/max(1e-9,np.abs(x).max())*0.89
    with wave.open(name,'wb') as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((x*32767).astype(np.int16).tobytes())
save('music.wav',mix)
# SFX track
sfx=np.zeros((n,2))
def whoosh(at,dur=0.45,g=0.5):
    s=int(at*sr); L=int(dur*sr); L=min(L,n-s); tt=np.arange(L)/sr
    no=rng.standard_normal(L)
    # simple swept lowpass via moving filter
    out=np.zeros(L); y=0
    for i in range(L):
        a=0.02+0.5*(tt[i]/dur)**1.5; y+=a*(no[i]-y); out[i]=y
    env=np.sin(np.pi*tt/dur)**2
    sfx[s:s+L,0]+=out*env*g; sfx[s:s+L,1]+=out*env*g*0.8
def pop(at,f=900,g=0.35):
    s=int(at*sr); L=min(int(0.12*sr),n-s); tt=np.arange(L)/sr
    fr=f*(1+1.5*np.exp(-tt/0.01)); ph=2*np.pi*np.cumsum(fr)/sr
    sfx[s:s+L,:]+=(np.sin(ph)*np.exp(-tt/0.03)*g)[:,None]
def ding(at,g=0.3):
    s=int(at*sr); L=min(int(1.2*sr),n-s); tt=np.arange(L)/sr
    d=(np.sin(2*np.pi*1318*tt)+0.5*np.sin(2*np.pi*1976*tt)+0.25*np.sin(2*np.pi*2637*tt))*np.exp(-tt/0.35)*g
    sfx[s:s+L,:]+=d[:,None]
def thud(at,g=0.6):
    s=int(at*sr); L=min(int(0.5*sr),n-s); tt=np.arange(L)/sr
    f=40+60*np.exp(-tt/0.05); ph=2*np.pi*np.cumsum(f)/sr
    sfx[s:s+L,:]+=(np.sin(ph)*np.exp(-tt/0.2)*g)[:,None]
def tick(at,g=0.25):
    s=int(at*sr); L=min(int(0.03*sr),n-s); tt=np.arange(L)/sr
    sfx[s:s+L,:]+=(np.sin(2*np.pi*2200*tt)*np.exp(-tt/0.006)*g)[:,None]
cues=json.load(open('cues.json'))
for c in cues:
    {'whoosh':whoosh,'pop':pop,'ding':ding,'thud':thud,'tick':tick}[c[0]](c[1])
save('sfx.wav',sfx)
print('ok')
