#!/usr/bin/env python3
"""Apply manual fixes to the doi.org BibTeX and keep only keys cited in the .aux file.
  finalize_bib.py refs/refs_raw.bib sedps_acp_manuscript.aux sedps_refs.bib"""
import re, sys
raw, aux, out = sys.argv[1:4]
s = open(raw).read()
fix = {
    "bogenschutz2025": [("year={2025}", "year={2025},\n  pages={e2025MS005127}")],
    "stanford2026": [("publisher={Copernicus GmbH}", "journal={EGUsphere [preprint]},\n  publisher={Copernicus GmbH}"),
                     ("Muelmenstaedt, Johannes", "M{\\\"u}lmenst{\\\"a}dt, Johannes")],
    "beare2014": [("year={2013}", "year={2014}")],
}
entries = re.findall(r"(@\w+\{([^,]+),.*?\n\})", s, re.S)
cited = set()
if aux != "-":
    for m in re.findall(r"\\citation\{([^}]*)\}", open(aux).read()):
        cited.update(k.strip() for k in m.split(","))
keep = []
for body, key in entries:
    for a, b in fix.get(key, []):
        body = body.replace(a, b)
    if aux == "-" or key in cited:
        keep.append(body)
open(out, "w").write("\n\n".join(keep) + "\n")
print(len(entries), "entries;", len(keep), "kept;", "missing:", sorted(cited - {k for _, k in entries}))
