# -*- coding: utf-8 -*-
"""Builds _artifact/page.html: index.html with the outer document tags stripped,
so it can be published as an Artifact preview (the Artifact platform supplies
its own <!doctype>/<head>/<body> skeleton). Preview only, never deployed."""
import io, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = io.open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()

head = s[s.index("<head>"):s.index("</head>")]
body = s[s.index("<body>") + len("<body>"):s.index("</body>")]

keep = re.findall(r'<link [^>]*>', head)
out = (u'<title>SEO Website Layout</title>\n'
       + "\n".join(keep) + "\n"
       + body.strip() + "\n")
d = os.path.join(ROOT, "_artifact")
if not os.path.isdir(d):
    os.makedirs(d)
io.open(os.path.join(d, "page.html"), "w", encoding="utf-8").write(out)
print("wrote _artifact/page.html (%d bytes)" % len(out))
