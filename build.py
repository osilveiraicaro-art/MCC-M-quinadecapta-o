"""Gera index.html a partir de pagina.html, preenchendo a conexão com o Supabase.
Uso: python3 build.py <SUPABASE_URL> <SUPABASE_PUBLISHABLE_KEY>"""
import sys, re, pathlib
url, key = sys.argv[1], sys.argv[2]
src = pathlib.Path("pagina.html").read_text()
src = src.replace('var SUPABASE_URL = "";', f'var SUPABASE_URL = "{url}";', 1)
src = src.replace('var SUPABASE_KEY = "";', f'var SUPABASE_KEY = "{key}";', 1)
src = src.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
head_end = src.index("</style>") + len("</style>")
head, body = src[:head_end], src[head_end:]
doc = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="Implementação completa para profissionais autônomos: landing page, Google Meu Negócio, Google Ads, CRM e assistente de IA no WhatsApp. Pagamento único, em até 12x.">
<meta property="og:title" content="Máquina de Captação de Clientes">
<meta property="og:description" content="Seja encontrado no Google, atenda com IA e acompanhe cada cliente. Pagamento único, em até 12x, sem mensalidade.">
<meta name="theme-color" content="#13286B">
<style>body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
{head}
</head>
<body>{body}
</body>
</html>
"""
pathlib.Path("index.html").write_text(doc)
print("ok", len(doc))
