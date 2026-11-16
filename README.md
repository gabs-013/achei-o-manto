---
schema_version: 1
project_id: achei-o-manto
audience: ai_agents
updated_at: 2026-11-13
---

# Achei o Manto — entrada para IA

Base independente. Não importar a paleta, o público ou os ativos de outra marca.

Leitura inicial: [MEMORIA.md](MEMORIA.md). Carregar depois somente os módulos relevantes:

| Necessidade | Documento |
|---|---|
| Contexto rápido | [MEMORIA.md](MEMORIA.md) |
| Logo, paleta e direção visual | [IDENTIDADE.md](IDENTIDADE.md) |
| Voz, SEO, copy e playbook | [CONTEUDO-E-OPERACAO.md](CONTEUDO-E-OPERACAO.md) |
| Entregas e pendências | [ESTADO.md](ESTADO.md) |
| Teste de substituição de camisa no vídeo | [EXPERIMENTO-VIDEO.md](EXPERIMENTO-VIDEO.md) |
| Decisões e precedência | [DECISOES.jsonl](DECISOES.jsonl) |
| Inventário de materiais | [ATIVOS.json](ATIVOS.json) |
| Proveniência | [FONTES.json](FONTES.json) |
| Como atualizar | [MANUTENCAO.md](MANUTENCAO.md) |

`referencias/logo.png` é cópia do logo explicitamente indicado pelo usuário. `fontes/` é arquivo histórico; prompts antigos e preferências do assistente não substituem a última referência do usuário. Binários além do logo permanecem nos locais registrados.

Precedência: pedido atual → decisão explícita mais recente no mesmo escopo → referência indicada pelo usuário → artefato compatível → proposta histórica. Não inferir aprovação de produção ou publicação pela presença de um arquivo.
