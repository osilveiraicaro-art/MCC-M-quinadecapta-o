-- Tabela de leads do diagnóstico (CRM)
create table if not exists public.leads (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  status text not null default 'novo'
    check (status in ('novo','em contato','reunião agendada','proposta enviada','fechado','perdido')),
  prioridade text check (prioridade in ('A','B','C')),
  nome text not null check (char_length(nome) between 1 and 120),
  whatsapp text check (char_length(whatsapp) <= 20),
  area text check (char_length(area) <= 60),
  cidade text check (char_length(cidade) <= 80),
  faturamento text check (char_length(faturamento) <= 60),
  nota int check (nota between 0 and 100),
  pontos_criticos text[],
  potencial_mensal numeric,
  potencial_anual numeric,
  quando_comecar text check (char_length(quando_comecar) <= 60),
  origem_clientes text check (char_length(origem_clientes) <= 60),
  aparece_google text check (char_length(aparece_google) <= 60),
  google_meu_negocio text check (char_length(google_meu_negocio) <= 60),
  pagina text check (char_length(pagina) <= 60),
  tempo_resposta text check (char_length(tempo_resposta) <= 60),
  acompanhamento text check (char_length(acompanhamento) <= 60),
  valor_cliente text check (char_length(valor_cliente) <= 60),
  clientes_desejados text check (char_length(clientes_desejados) <= 60),
  codigo text check (char_length(codigo) <= 20),
  utm_source text check (char_length(utm_source) <= 200),
  utm_medium text check (char_length(utm_medium) <= 200),
  utm_campaign text check (char_length(utm_campaign) <= 200),
  utm_term text check (char_length(utm_term) <= 200),
  gclid text check (char_length(gclid) <= 300),
  observacoes text,
  origem text check (char_length(origem) <= 30)
);

-- Para quem já criou a tabela antes:
alter table public.leads add column if not exists origem text check (char_length(origem) <= 30);

alter table public.leads enable row level security;

-- Visitantes da página só podem INSERIR (nunca ler, editar ou apagar).
drop policy if exists "pagina pode inserir lead" on public.leads;
create policy "pagina pode inserir lead" on public.leads
  for insert to anon
  with check (status = 'novo' and observacoes is null);

revoke all on public.leads from anon;
grant insert on public.leads to anon;

create index if not exists leads_created_at_idx on public.leads (created_at desc);
