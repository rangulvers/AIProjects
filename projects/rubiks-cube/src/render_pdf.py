"""Render the HTML guides to print-ready A4 PDFs (needs: pip install playwright && playwright install chromium)."""
import os, sys
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
GUIDES = os.path.join(HERE, '..', 'guides')
JOBS = {'schicht-fuer-schicht': 'Zauberwürfel lösen · Schicht für Schicht', 'cfop': 'CFOP lernen · Schneller lösen'}

with sync_playwright() as p:
    b = p.chromium.launch()
    for name, label in JOBS.items():
        pg = b.new_page()
        pg.goto('file://' + os.path.abspath(os.path.join(GUIDES, name + '.html')))
        pg.wait_for_timeout(300)
        footer = ('<div style="width:100%%;font-family:Inter,sans-serif;font-size:8px;color:#9ca3af;text-align:center;">'
                  '%s · Seite <span class="pageNumber"></span> von <span class="totalPages"></span></div>' % label)
        pg.pdf(path=os.path.join(GUIDES, name + '.pdf'), format='A4', print_background=True, prefer_css_page_size=True,
               display_header_footer=True, header_template='<div></div>', footer_template=footer)
        print('wrote', name + '.pdf')
    b.close()
