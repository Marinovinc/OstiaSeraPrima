# -*- coding: utf-8 -*-
"""Scarica foto reali di esche da Wikimedia Commons (ricerca testuale + whitelist
di parole-chiave da pesca nel titolo, per scartare libri/incisioni). Manifest con
autore/licenza per attribuzione."""
import os, json, ssl, urllib.parse, urllib.request

OUT = "D:/claude_handoff/outbox/Roma_pesca_campionato_2026/esche_foto"
os.makedirs(OUT, exist_ok=True)
CTX = ssl.create_default_context(); CTX.check_hostname=False; CTX.verify_mode=ssl.CERT_NONE
UA = {"User-Agent":"IschiaFishing-research/1.0 (marino@unitec.it)"}

WL = ["lure","wobbler","koder","kunstkoder","bait","spinner","spoon","jig","crankbait",
      "rapala","plug","squid","skirt","teaser","popper","blinker","pilker","angeln",
      "leurre","esca","artificial","tackle","trolling lure","fishing"]
def ok_title(t):
    t=t.lower().replace("ö","o")
    if any(b in t for b in ("djvu",".pdf","garden","versailles","labyrinte","map","manuscript","engraving")): return False
    return any(w in t for w in WL)

FAM = {
 "minnow":  ["fishing wobbler","Rapala lure","crankbait lure","Kunstkoder wobbler"],
 "kona":    ["octopus skirt lure","trolling squid lure","marlin trolling lure","soft squid fishing lure"],
 "piumetta":["feather jig lure","tuna feather lure","saltwater feather lure fishing"],
 "teaser":  ["fishing teaser spreader bar","trolling teaser fishing","daisy chain fishing lure"],
}

def api(params):
    u="https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode(params)
    with urllib.request.urlopen(urllib.request.Request(u,headers=UA),context=CTX,timeout=30) as r:
        return json.load(r)

def search(term,n=12):
    d=api({"action":"query","format":"json","generator":"search","gsrsearch":term,
           "gsrnamespace":"6","gsrlimit":str(n),"prop":"imageinfo",
           "iiprop":"url|extmetadata|mime|size","iiurlwidth":"800"})
    out=[]
    for p in (d.get("query",{}).get("pages",{}) or {}).values():
        ii=(p.get("imageinfo") or [{}])[0]; mime=ii.get("mime","")
        if mime not in ("image/jpeg","image/png"): continue
        if not ok_title(p.get("title","")): continue
        em=ii.get("extmetadata",{})
        out.append({"title":p.get("title"),"thumb":ii.get("thumburl"),
                    "w":ii.get("thumbwidth"),"h":ii.get("thumbheight"),
                    "author":(em.get("Artist",{}) or {}).get("value","")[:120],
                    "lic":(em.get("LicenseShortName",{}) or {}).get("value",""),
                    "src":ii.get("descriptionurl")})
    return out

manifest=[]; seen=set()
for fam,terms in FAM.items():
    got=0
    for term in terms:
        if got>=5: break
        try: res=search(term)
        except Exception as e: print("ERR",term,e); continue
        for r in res:
            if got>=5 or r["title"] in seen or not r["thumb"]: continue
            seen.add(r["title"])
            ext=".jpg" if (".jpg" in r["thumb"].lower() or ".jpeg" in r["thumb"].lower()) else ".png"
            fn=f"{fam}_{got}{ext}"; fp=os.path.join(OUT,fn)
            try:
                with urllib.request.urlopen(urllib.request.Request(r["thumb"],headers=UA),context=CTX,timeout=40) as resp:
                    data=resp.read()
                if len(data)<3000: continue
                open(fp,"wb").write(data); r["file"]=fn; r["fam"]=fam; manifest.append(r); got+=1
                print(f"OK {fn:13s} {str(r['w'])+'x'+str(r['h']):10s} {r['title'][:50]}")
            except Exception as e: print("DLERR",fn,e)
    print(f"  [{fam}] {got} foto\n")
json.dump(manifest,open(os.path.join(OUT,"manifest.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=1)
print(f"TOT {len(manifest)} foto.")
