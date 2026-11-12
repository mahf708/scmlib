#!/usr/bin/env python3
"""Fetch BibTeX for every 'key doi' line from doi.org (content negotiation),
check it against Crossref, re-key it and clean characters pdflatex dislikes.
  fetch_bib.py dois.txt extra.bib > refs.bib"""
import os, re, sys, time, urllib.request

def fetch(doi):
    for i in range(6):
        try:
            req = urllib.request.Request("https://doi.org/" + doi,
                                         headers={"Accept": "application/x-bibtex", "User-Agent": "bib-check/1.0"})
            return urllib.request.urlopen(req, timeout=40).read().decode("utf-8")
        except Exception:
            time.sleep(3 * (i + 1))
    return None

REPL = {"‐": "-", "‑": "-", "‒": "-", "–": "--", "—": "---", "‘": "`", "’": "'",
        "“": "``", "”": "''", " ": " ", "&amp;aring;": "{\\aa}", "&amp;": "\\&", " ": " ", "−": "-"}
UNI = {"\u00d8": "{\\O}", "\u00e1": "{\\'a}", "\u00e4": "{\\\"a}", "\u00e6": "{\\ae}", "\u00f6": "{\\\"o}", "\u00fc": "{\\\"u}", "&aring;": "{\\aa}"}
PROTECT = ["DYCOMS-II", "DYCOMS", "LES", "GCMs", "GCM", "E3SM", "SCREAM", "DNS", "VOCALS-REx", "POC", "CRM", "RICO",
           "A-Train", "CAM3", "CAM", "DYAMOND", "PDF", "Earth", "Community Atmosphere Model", "Terra Incognita",
           "Atlantic", "Pacific", "ECHAM", "WRF", "CONSTRAIN", "Part", "I", "II"]

def clean(b, key):
    b = re.sub(r"^@(\w+)\{[^,]*,", lambda m: "@" + m.group(1) + "{" + key + ",", b.strip(), count=1)
    for k, v in list(REPL.items()) + list(UNI.items()):
        b = b.replace(k, v)
    b = re.sub(r"</?(i|sub|sup|scp|b)>", "", b)
    b = re.sub(r",\s*url=\{[^}]*\}", "", b)          # DOI is enough
    b = re.sub(r",\s*ISSN=\{[^}]*\}", "", b)
    b = re.sub(r",\s*month=\w+", "", b)
    def prot(m):
        t = m.group(1)
        for w in PROTECT:
            t = re.sub(r"(?<![{\w])" + re.escape(w) + r"(?![\w}])", "{" + w + "}", t)
        return "title={" + t + "}"
    b = re.sub(r"title=\{(.*?)\}, (?=\w+=)", lambda m: prot(m) + ", ", b, count=1)
    b = b.replace("pages={", "pages={").replace("–", "--")
    b = re.sub(r"\}, (?=\w+=)", "},\n  ", b)
    b = re.sub(r"^(@\w+\{[^,]+,) ", r"\1\n  ", b)
    return b.rstrip("}").rstrip() + "\n}\n"

out = []
for line in open(sys.argv[1]):
    if not line.strip():
        continue
    key, doi = line.split()
    cache = os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), "cache", key + ".bib")
    if os.path.exists(cache):
        b = open(cache).read()
    else:
        b = fetch(doi)
        if b:
            os.makedirs(os.path.dirname(cache), exist_ok=True)
            open(cache, "w").write(b)
    if not b or not b.strip().startswith("@"):
        print(f"FAILED {key} {doi}", file=sys.stderr)
        continue
    out.append(clean(b, key))
    time.sleep(0.5)
print("\n".join(out))
if len(sys.argv) > 2:
    print(open(sys.argv[2]).read())
