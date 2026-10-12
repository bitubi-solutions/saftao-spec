# saftao-spec

Especificação e testes de conformidade partilhados das bibliotecas `saftao-*`, que geram, lêem e validam o ficheiro SAF-T (AO), por Bitubi Solutions.

Este repo é a fonte de verdade das regras e dos casos de teste. Cada biblioteca (`saftao-java`, `saftao-python`, `saftao-csharp`, `saftao-php`, e depois `saftao-rust` e `saftao-c`) implementa a especificação de forma nativa e tem de passar os mesmos testes.

> **Aviso.** Este projecto **não é um programa de facturação certificado** e **não foi avaliado, aprovado nem endossado pela AGT** (Administração Geral Tributária). Quem o integrar num software que emite documentos fiscais é responsável por cumprir os requisitos legais aplicáveis, incluindo a certificação do software e o registo como produtor. A assinatura incluída serve para teste e interoperabilidade. Fornecido "tal como está", sem garantias (ver licença).

## Estado

**v0.2, rascunho.** Cobre a versão **1.01_01** do SAF-T (AO). Cada afirmação indica o seu estado de verificação; ver [`spec/00-overview.md`](spec/00-overview.md) e [`spec/sources.md`](spec/sources.md).

- **Estrutura, campos e regras de negócio:** especificadas, a partir do XSD e da legislação.
- **Assinatura dos documentos:** especificada (RSA 1024 bits, SHA-1, PKCS#1 v1.5, base64 de 172 caracteres) com vectores de teste. **A fonte é uma proposta oficial de 2018**; confirmar a vigência antes de produção. Ver [`spec/04-signature.md`](spec/04-signature.md).
- Parte das regras vem de uma *proposta* de decreto executivo do Ministério das Finanças (2018), não do texto final.

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

## Aviso sobre validadores de terceiros

Testámos o validador gratuito [saft.ao](https://saft.ao) com 20 ficheiros sintéticos: **valida só o esquema XSD**. Aceitou ficheiros com hash adulterado, numeração com salto e totais incoerentes. **Passar no saft.ao não prova que o ficheiro passa o validador da AGT.** Detalhes em [`conformance/oracle/results/`](conformance/oracle/results/saft.ao-2026-10-12.md).

## Contribuir

Correcções às fontes, regras verificadas com referência a legislação e novos casos de conformidade são bem-vindos. Regras sem fonte citada são marcadas como *não verificadas*.

## Licença

Apache-2.0 para o conteúdo original (ver [LICENSE](LICENSE)). O XSD e os exemplos de origem têm atribuição em [NOTICE](NOTICE).
