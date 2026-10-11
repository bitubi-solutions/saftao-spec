# 00 — Visão geral

## Âmbito

Esta especificação descreve o ficheiro **SAF-T (AO)**, versão **1.01_01**: o ficheiro XML normalizado de auditoria tributária de Angola. Serve de referência comum às bibliotecas `saftao-*` (Java, Python, C#, PHP, e depois Rust e C), que a implementam de forma nativa e têm de passar os mesmos testes de conformidade (`conformance/`).

**Dentro do âmbito**
- Estrutura e campos do ficheiro (derivados do XSD).
- Regras de negócio verificáveis (totais, numeração, estados).
- Assinatura e encadeamento dos documentos (`Hash`, `HashControl`).

**Fora do âmbito (por agora)**
- A API de facturação electrónica da AGT (JSON, assinatura RS256, certificados). É um mecanismo diferente e ainda em evolução; terá a sua própria especificação.
- Submissão do ficheiro à AGT, interface do contribuinte, e regras fiscais materiais (taxas, isenções).

## Níveis de normatividade

Cada afirmação desta especificação tem um estado:

| Estado | Significado |
|---|---|
| **verificado** | Confirmado numa fonte primária (XSD ou legislação) citada em `sources.md` |
| **não verificado** | Vem de fonte secundária ou de inferência; **não** deve ser implementado como obrigatório antes de confirmação |
| **por confirmar** | Ponto aberto conhecido, à espera de fonte |

Implementadores devem tratar apenas o que está **verificado** como normativo.

## Ordem de leitura

1. [`01-structure.md`](01-structure.md): visão geral da estrutura.
2. [`02-fields.md`](02-fields.md): referência de campos (gerada do XSD).
3. [`03-business-rules.md`](03-business-rules.md): regras de negócio.
4. [`04-signature.md`](04-signature.md): assinatura e encadeamento.
5. [`sources.md`](sources.md): fontes e o que está verificado.

## Como implementar uma biblioteca

1. Gerar (ou escrever) o modelo a partir de `schema/SAFTAO1.01_01.xsd`.
2. Implementar a validação contra o XSD.
3. Implementar as regras de `03-business-rules.md` marcadas como verificadas.
4. Passar todos os casos de `conformance/` (o campo `valid` de cada `.expected.json`). As mensagens de erro podem variar entre linguagens; só o resultado conta.
