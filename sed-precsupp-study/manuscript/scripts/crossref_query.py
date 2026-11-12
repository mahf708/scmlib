#!/usr/bin/env python3
"""Search Crossref: crossref_query.py "free text" ["free text" ...] (retries on rate limits)."""
import json, sys, time, urllib.parse, urllib.request

def get(url):
    for i in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "bib-check/1.0"})
            return json.load(urllib.request.urlopen(req, timeout=40))
        except Exception:
            time.sleep(3 * (i + 1))
    return None

for q in sys.argv[1:]:
    print("Q:", q)
    r = get("https://api.crossref.org/works?rows=3&query.bibliographic=" + urllib.parse.quote(q))
    if not r:
        print("   FAILED"); continue
    for m in r["message"]["items"]:
        a = m.get("author", [{}]); fa = a[0].get("family", "?") if a else "?"
        y = m.get("issued", {}).get("date-parts", [[None]])[0][0]
        print(f"   {m['DOI']} | {fa} ({len(a)}) {y} | {m.get('title', [''])[0][:95]} | {(m.get('container-title') or [''])[0][:35]}")
    time.sleep(1)
