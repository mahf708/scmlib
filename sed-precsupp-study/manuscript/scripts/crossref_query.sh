#!/bin/bash
# Search Crossref bibliographic metadata: crossref_query.sh "free text"
q=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$1")
curl -s -m 30 -A "bib-check/1.0" "https://api.crossref.org/works?query.bibliographic=$q&rows=${2:-3}" | python3 -c "
import json,sys
for m in json.load(sys.stdin)['message']['items']:
  a=m.get('author',[{}]); fa=a[0].get('family','?') if a else '?'
  y=(m.get('issued',{}).get('date-parts',[[None]])[0][0])
  print(f\"   {m['DOI']} | {fa} ({len(a)}) {y} | {m.get('title',[''])[0][:95]} | {(m.get('container-title') or [''])[0][:35]}\")
"
