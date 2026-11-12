#!/bin/bash
# Verify each DOI against Crossref and print first author, year, title, journal.
while read key doi; do
  j=$(curl -s -m 30 -A "bib-check/1.0" "https://api.crossref.org/works/$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1],safe='/'))" "$doi")")
  echo "$j" | python3 -c "
import json,sys
k='$key'
try:
  m=json.load(sys.stdin)['message']
  a=m.get('author',[{}]); fa=a[0].get('family','?') if a else m.get('editor',[{}])[0].get('family','?')
  y=(m.get('issued',{}).get('date-parts',[[None]])[0][0])
  print(f\"OK  {k:20s} {fa} ({len(a)} au) {y} | {m.get('title',[''])[0][:90]} | {(m.get('container-title') or [''])[0][:40]}\")
except Exception as e:
  print(f'BAD {k:20s} $doi')
"
done < "$1"
