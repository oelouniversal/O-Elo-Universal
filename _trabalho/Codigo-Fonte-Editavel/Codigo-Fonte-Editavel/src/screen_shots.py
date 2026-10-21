import sys, os
from playwright.sync_api import sync_playwright
HTML = "/home/claude/elo/build/book-screen.html"
OUT = "/home/claude/elo/build/shots"
exe = None
for root, d, files in os.walk("/opt/pw-browsers/chromium"):
    if "chrome" in files: exe = os.path.join(root, "chrome"); break
with sync_playwright() as p:
    br = p.chromium.launch(executable_path=exe)
    for name, (w, h, dpr) in {"phone": (390, 844, 2), "tablet": (820, 1180, 1), "desktop": (1280, 900, 1)}.items():
        ctx = br.new_context(viewport={"width": w, "height": h}, device_scale_factor=dpr)
        pg = ctx.new_page(); pg.goto("file://" + HTML); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(500)
        sw = pg.evaluate("document.documentElement.scrollWidth"); cw = pg.evaluate("document.documentElement.clientWidth")
        total = pg.evaluate("document.documentElement.scrollHeight")
        wide = pg.evaluate("""() => [...document.querySelectorAll('body *')].filter(e => e.getBoundingClientRect().right > document.documentElement.clientWidth + 1 && getComputedStyle(e).position !== 'fixed').slice(0,6).map(e => e.className || e.tagName)""")
        print(name, "scrollW", sw, "clientW", cw, "altura", total, "elementos largos:", wide)
        # capturas: capa, sumário, abertura cap.1, corpo cap.1, registro cap.1
        for key, sel in [("capa", "#capa"), ("sumario", "#sumario"), ("abertura", "#cap-1"), ("tradicao", "#cap-1-tradicao"), ("experimento", "#cap-1-experimento"), ("registro", "#cap-1-registro"), ("registro5", "#cap-5-registro"), ("porta", "#cap-1-porta")]:
            el = pg.query_selector(sel)
            el.scroll_into_view_if_needed(); 
            box = el.bounding_box()
            pg.screenshot(path=f"{OUT}/S-{name}-{key}.png", full_page=True, clip={"x": 0, "y": box["y"] + pg.evaluate("window.scrollY"), "width": w, "height": min(box["height"], 1800)})
        ctx.close()
    br.close()
