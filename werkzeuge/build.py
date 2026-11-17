import json
w=json.load(open('words.json'))
out=[]
for x in w:
    if x['w'].startswith('-') and out:
        out[-1]['w']+=x['w']; out[-1]['e']=x['e']; continue
    out.append(dict(x))
fix={'fang':'Fang','dich,':'dich:','Gehirns,':'Gehirns:','Psycho-Tricks.':'Psycho-Tricks!'}
for x in out: x['w']=fix.get(x['w'],x['w'])
res=[]
for x in out:
    if res and res[-1]['w']=='20er': res[-1]['w']='Zwanzigern'; res[-1]['e']=x['e']; continue
    res.append(x)
for x in res:
    if x['w']=='Dein' and x['s']>28: x['s']=28.85
open('../short/index.html','w').write(open('template.html').read().replace('__WORDS__',json.dumps(res,ensure_ascii=False)))
