# Máquina de Captação de Clientes

Landing page com diagnóstico gratuito. Os leads vão para a tabela `leads` do Supabase.

- `index.html`: página publicada pela Vercel.
- `pagina.html`: fonte da página, sem as chaves do Supabase.
- `build.py`: gera `index.html` a partir de `pagina.html` com a URL e a chave publishable do Supabase.
- `supabase.sql`: cria a tabela `leads` e a regra que permite à página apenas inserir.
