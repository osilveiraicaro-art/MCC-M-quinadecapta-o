"""Gera as páginas publicadas pela Vercel a partir de pagina.html:
  index.html              página de vendas completa (origem padrão: orgânico)
  diagnostico/index.html  só o diagnóstico, para prospecção ativa (origem padrão: prospecção)

Uso: python3 build.py <SUPABASE_URL> <SUPABASE_PUBLISHABLE_KEY>"""
import sys, pathlib

url, key = sys.argv[1], sys.argv[2]
src = pathlib.Path("pagina.html").read_text()
src = src.replace('var SUPABASE_URL = "";', f'var SUPABASE_URL = "{url}";', 1)
src = src.replace('var SUPABASE_KEY = "";', f'var SUPABASE_KEY = "{key}";', 1)
src = src.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')

style_end = src.index("</style>") + len("</style>")
head_part = src[:style_end]
body_part = src[style_end:]
script = body_part[body_part.index("<script>"):]


def section(html, marker):
    """Devolve a <section> que contém o marcador."""
    i = html.index(marker)
    start = html.rindex("<section", 0, i)
    end = html.index("</section>", i) + len("</section>")
    return html[start:end]


def page(head, body, extra_meta=""):
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#13286B">
{extra_meta}<style>body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
{head}
</head>
<body>{body}
</body>
</html>
"""


# Página de vendas
sales_meta = """<meta name="description" content="Sistema completo de captação para imobiliárias: landing page, Google Meu Negócio, Google Ads, CRM com funil por corretor e assistente de IA no WhatsApp. Pagamento único, em até 12x.">
<meta property="og:title" content="Máquina de Captação de Clientes">
<meta property="og:description" content="Clientes chegando direto para a sua imobiliária, atendidos na hora e acompanhados até o fechamento. Pagamento único, em até 12x, sem mensalidade.">
"""
pathlib.Path("index.html").write_text(page(head_part, body_part, sales_meta))

# Página só do diagnóstico
quiz = section(body_part, 'id="quiz"')
quiz_box = quiz[quiz.index('<div class="quiz" id="quiz">'):quiz.rindex("</div>\n  </div>\n</section>") + len("</div>")]
diag_css = """<style>
.dhero{background:radial-gradient(120% 90% at 85% 10%, #2447A8 0%, transparent 55%), linear-gradient(120deg, var(--navy-deep) 0%, var(--navy) 60%, #1A3488 100%);padding-block:clamp(40px,6vw,72px) clamp(90px,12vw,130px)}
.dhero .wrap{display:flex;flex-direction:column;gap:18px;max-width:820px}
.dhero h1{font-size:clamp(1.9rem,4.4vw,3rem)}
.dhero .pts{display:flex;flex-wrap:wrap;gap:8px 18px}
.dhero .pts span{font-family:var(--f-mono);font-size:.78rem;color:var(--muted);display:flex;align-items:center;gap:8px}
.dhero .pts span::before{content:"";width:7px;height:7px;border-radius:50%;background:var(--yellow)}
.dquiz{margin-top:clamp(-110px,-9vw,-70px);padding-bottom:clamp(48px,7vw,80px)}
.dquiz .wrap{max-width:820px}
.dfoot{border-top:1px solid var(--line);padding-block:26px}
.dfoot .wrap{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;align-items:center}
.dfoot a{font-weight:700;color:var(--navy)}
</style>"""
title_base = "Descubra em 2 minutos onde sua imobiliária está perdendo clientes"
diag_body = f"""

<header class="top">
  <div class="wrap">
    <div class="logo"><i aria-hidden="true"></i>Máquina de Captação de Clientes</div>
    <span class="fine">Diagnóstico gratuito · 2 minutos</span>
  </div>
</header>

<main>
<section class="dhero dark">
  <div class="wrap">
    <span class="eyebrow">Diagnóstico de captação</span>
    <h1 data-personal="{title_base}">{title_base}</h1>
    <p class="lede muted">Responda algumas perguntas rápidas. No final, você vê a nota de captação da imobiliária, os pontos que estão levando clientes para a concorrência e quanto isso representa em comissões.</p>
    <div class="pts"><span>Gratuito</span><span>Leva 2 minutos</span><span>Resultado na hora</span></div>
  </div>
</section>

<section class="dquiz">
  <div class="wrap">
    {quiz_box}
  </div>
</section>
</main>

<footer class="dfoot">
  <div class="wrap">
    <span class="fine">Máquina de Captação de Clientes · pagamento único, em até 12x</span>
    <a href="/">Conhecer a solução completa</a>
  </div>
</footer>

{script.replace('var PAGE_ORIGEM = "orgânico";', 'var PAGE_ORIGEM = "prospecção";', 1)}"""
diag_head = head_part.replace("<title>Máquina de Captação de Clientes</title>",
                              "<title>Diagnóstico de Captação</title>", 1) + "\n" + diag_css
diag_meta = '<meta name="robots" content="noindex">\n<meta property="og:title" content="Diagnóstico de captação de clientes">\n<meta property="og:description" content="Descubra em 2 minutos onde sua imobiliária está perdendo clientes.">\n'
pathlib.Path("diagnostico").mkdir(exist_ok=True)
pathlib.Path("diagnostico/index.html").write_text(page(diag_head, diag_body, diag_meta))
print("ok: index.html, diagnostico/index.html")
