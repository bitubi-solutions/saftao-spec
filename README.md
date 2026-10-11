# saftao-spec

Especificação e testes de conformidade partilhados das bibliotecas `saftao-*`, que geram, lêem e validam o ficheiro SAF-T (AO), por Bitubi Solutions.

Este repo é a fonte de verdade das regras e dos casos de teste. Cada biblioteca (`saftao-java`, `saftao-python`, `saftao-csharp`, `saftao-php`, e depois `saftao-rust` e `saftao-c`) implementa a especificação de forma nativa e tem de passar os mesmos testes.

## Estado

**v0.1, rascunho.** Cobre a versão **1.01_01** do SAF-T (AO). Parte do conteúdo está marcada como *não verificado* ou *por confirmar*; ver [`spec/00-overview.md`](spec/00-overview.md) e [`spec/sources.md`](spec/sources.md). Em particular, **a assinatura dos documentos ainda não está especificada** (algoritmo por confirmar).

## Conteúdo

| Pasta | O que tem |
|---|---|
| [`spec/`](spec/) | A especificação: visão geral, estrutura, referência de campos (gerada do XSD), regras de negócio, assinatura, fontes |
| [`schema/`](schema/) | O XSD SAF-T (AO) 1.01_01, sem alterações (ver [`NOTICE`](NOTICE)) |
| [`conformance/`](conformance/) | Casos de teste partilhados (`.xml` + `.expected.json`) |
| [`tools/`](tools/) | `xsd_to_md.py` (gera `spec/02-fields.md`) e `validate.py` (validador de referência) |

## Ferramentas

```bash
# regenerar a referência de campos a partir do XSD (apenas biblioteca padrão)
python3 -I tools/xsd_to_md.py schema/SAFTAO1.01_01.xsd > spec/02-fields.md

# validar um ficheiro com o validador de referência (requer lxml)
python3 tools/validate.py schema/SAFTAO1.01_01.xsd ficheiro.xml
```

## Contribuir

Correcções às fontes, regras verificadas com referência a legislação e novos casos de conformidade são bem-vindos. Regras sem fonte citada são marcadas como *não verificadas*.

## Licença

Apache-2.0 para o conteúdo original (ver [LICENSE](LICENSE)). O XSD e os exemplos de origem têm atribuição em [NOTICE](NOTICE).
