# Máquina de Captação de Clientes

Landing page com diagnóstico gratuito. Os leads vão para a tabela `leads` do Supabase.

- `index.html`: página de vendas publicada pela Vercel (origem padrão dos leads: orgânico; com gclid ou utm_medium=cpc vira anúncio).
- `diagnostico/index.html`: só o diagnóstico, para prospecção ativa. Aceita `?nome=Ana&area=Odontologia&tel=48999999999` (origem: prospecção).
- `prospeccao/index.html`: ferramenta interna que gera o link personalizado e as mensagens de prospecção.
- `pagina.html`: fonte da página, sem as chaves do Supabase.
- `build.py`: gera `index.html` e `diagnostico/index.html` a partir de `pagina.html` com a URL e a chave publishable do Supabase.
- `supabase.sql`: cria a tabela `leads` e a regra que permite à página apenas inserir.
