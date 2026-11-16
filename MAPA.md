---
project_id: achei-o-manto
purpose: mapa_de_caminhos
updated_at: 2026-11-16
---

# Mapa de caminhos

Os documentos usam caminhos **relativos ao workspace original** (`output/...`, `Posts Feed/...`). Este repositório guarda uma parte desse conteúdo em outros lugares. Use esta tabela para traduzir.

## Regra de tradução

| Caminho nos documentos | Onde está no repositório |
|---|---|
| `output/achei-o-manto/<pasta>/<arquivo>` (texto, JSON) | `fontes/textos/workspace/output/achei-o-manto/<pasta>/<arquivo>` |
| `output/santos-video-test/<arquivo>` (texto, JSON, script) | `fontes/textos/workspace/output/santos-video-test/<arquivo>` |
| `referencias/logo.png` | `referencias/logo.png` (mesmo caminho) |
| `fontes/...` | `fontes/...` (mesmo caminho) |
| `Posts Feed/...` | `Posts Feed/...` (mesmo caminho, fora do inventário; ver abaixo) |
| Imagens, vídeos e zips em `output/` | **Não estão no repositório.** Ficam no computador de origem e são listados em `ATIVOS.json` |

Os caminhos `/Users/g.martins/...` em `ATIVOS.json`, `FONTES.json` e `EXPERIMENTO-VIDEO.md` são referências do computador de origem. Não existem neste ambiente.

## Estado da cobertura

- `ATIVOS.json`: 69 ativos. 20 têm cópia textual neste repositório (`knowledge_copy`). Os 49 restantes são binários ou externos, e só o registro existe aqui.
- `FONTES.json`: 26 fontes. Todas as cópias locais referenciadas existem.
- `DECISOES.jsonl`: 12 decisões, todas em JSON válido.
- `Posts Feed/`: 6 imagens PNG e 7 arquivos de texto ou JSON. **Não estão no inventário `ATIVOS.json`** e não possuem hash registrado. Para incluí-los, siga o procedimento de `MANUTENCAO.md`.

## Onde encontrar cada tipo de coisa

| Pergunta | Arquivo |
|---|---|
| Qual é a direção atual? | `MEMORIA.md`, depois `DECISOES.jsonl` |
| Qual logo e cores valem? | `IDENTIDADE.md`, `referencias/logo.png` |
| Qual o estado de cada entrega? | `ESTADO.md` |
| Qual foi a última apresentação? | `post-minimalista/` (três páginas, direção vigente). As de quatro páginas são histórico |
| Qual o status do teste de vídeo? | `EXPERIMENTO-VIDEO.md` (experimental, não é vídeo final) |
| De onde veio cada afirmação? | `FONTES.json` e `fontes/` |
| O que mudou e quando? | `CHANGELOG.md` |
