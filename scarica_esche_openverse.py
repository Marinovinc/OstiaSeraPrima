# -*- coding: utf-8 -*-
"""Scarica foto reali a licenza libera (CC) di esche da altura via Openverse API.
Per kona/octopus, piumetta/feather, teaser/spreader-bar. Salva manifest con
autore/licenza/fonte per attribuzione onesta."""
import os, json, ssl, urllib.parse, urllib.request

OUT = "D:/claude_handoff/outbox/Roma_pesca_campionato_2026/esche_foto"
os.makedirs(OUT, exist_ok=True)
CTX = ssl.create_default_context(); CTX.check_hostname=False; CTX.verify_mode=ssl.CERT_NONE
UA = {"User-Agent":"IschiaFishing-research/1.0 (marino@unitec.it)"}

FAM = {
 "kona":     ["trolling lure skirt", "marlin trolling lure", "kona lure", "skirted game lure"],
 "piumetta": ["tuna feather lure", "feather jig fishing", "saltwater feather lure"],
 "teaser":   ["spreader bar fishing", "daisy chain teaser fishing", "trolling teaser lure"],
}
WL = ["lure","fishing","bait","jig","teaser","trolling","tuna","marlin","skirt","tackle","game fish","spreader"]
def ok(t):
    t=(t or "").lower()
    if any(b in t for b in ("book","map","logo","poster","stamp","coin")): return False
    return any(w in t for w in WL)

def api(q):
    u="https://api.openverse.org/v1/images/?"+urllib.parse.urlencode(
        {"q":q,"page_size":"12","license_type":"all-cc","mature":"false"})
    with urllib.request.urlopen(urllib.request.Request(u,headers=UA),context=CTX,timeout=30) as r:
        return json.load(r)

manifest=[]
for fam,queries in FAM.items():
    got=0
    for q in queries:
        if got>=4: break
        try: data=api(q)
        except Exception as e: print("ERR",q,str(e)[:80]); continue
        for it in data.get("results",[]):
            if got>=4: break
            if not ok(it.get("title","")): continue
            thumb=it.get("thumbnail") or it.get("url")
            if not thumb: continue
            fn=f"{fam}_ov_{got}.jpg"; fp=os.path.join(OUT,fn)
            try:
                with urllib.request.urlopen(urllib.request.Request(thumb,headers=UA),context=CTX,timeout=40) as resp:
                    d=resp.read()
                if len(d)<3000: continue
                open(fp,"wb").write(d)
                manifest.append({"file":fn,"fam":fam,"title":it.get("title"),
                    "creator":it.get("creator"),"license":(it.get("license","")+" "+str(it.get("license_version",""))).strip(),
                    "source":it.get("foreign_landing_url")})
                got+=1
                print(f"OK {fn:14s} [{it.get('license')}] {str(it.get('title'))[:45]}")
            except Exception as e: print("DLERR",fn,str(e)[:60])
    print(f"  [{fam}] {got}\n")
json.dump(manifest,open(os.path.join(OUT,"manifest_openverse.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("TOT", len(manifest))
