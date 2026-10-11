# Testes de conformidade

Casos partilhados por todas as bibliotecas `saftao-*`.

## Dois tipos de casos

### 1. Validação de ficheiros (`cases/`)

Cada caso é um par:

- `<nome>.xml`: o ficheiro SAF-T a validar.
- `<nome>.expected.json`: `{"valid": true|false, "level": "schema"|"business-rule", "rules": [...], "reason": "..."}`.

Uma biblioteca **passa** um caso se o seu resultado (`válido`/`inválido`) coincidir com `valid`. As mensagens de erro podem diferir entre linguagens e **não** são comparadas.

| `level` | Significado |
|---|---|
| `schema` | O ficheiro viola o XSD (ou não é XML) |
| `business-rule` | O ficheiro **passa** o XSD mas viola uma ou mais regras de `spec/03-business-rules.md`, listadas em `rules` |

Uma biblioteca que só valide o XSD passa os casos `schema` e falha os `business-rule`; é um nível de conformidade parcial e legítimo, mas tem de o declarar.

| Caso | Esperado | Nível | O que testa |
|---|---|---|---|
| `valid-purchase-invoices` | válido | schema | Ficheiro de referência de facturas de compra |
| `invalid-version` | inválido | schema | `AuditFileVersion` diferente de `1.01_01` |
| `invalid-missing-company-name` | inválido | schema | `CompanyName` em falta no `Header` |
| `invalid-currency` | inválido | schema | `CurrencyCode` fora de `AOA`/`USD` |
| `invalid-accounting-basis` | inválido | schema | `TaxAccountingBasis` fora dos valores permitidos |
| `invalid-company-country` | inválido | schema | `Country` do endereço da empresa diferente de `AO` |
| `invalid-not-xml` | inválido | schema | XML mal formado |
| `rule-purchase-count-mismatch` | inválido | business-rule (R-009) | `NumberOfEntries` ≠ número de documentos de compra |
| `rule-credit-note-without-reference` | inválido | business-rule (R-013) | Nota de crédito de compra sem `References` |

Os casos `schema` foram confirmados com o validador de referência (`tools/validate.py`, lxml/libxml2). Os `business-rule` foram confirmados como **válidos no XSD** pelo mesmo validador; a violação da regra decorre do texto da especificação.

### 2. Construção da mensagem de assinatura (`signature/`)

`signature/message-construction.json` contém vectores para duas funções que qualquer biblioteca tem de ter:

- `messageConstruction`: dados os campos do documento e o `Hash` anterior, a mensagem a assinar (campos separados por `;`).
- `grossTotalFormat`: formatação do `GrossTotal` (duas casas, ponto decimal, sem separador de milhares, arredondado a duas casas).

Cada vector tem `status` (`verificado (proposta)` ou `por confirmar`); ver `spec/04-signature.md`. **Não há vectores da assinatura em si**: o digest está por confirmar.

## Próximos casos

- Um ou mais casos por regra restante de `03-business-rules.md` (R-001 a R-008, R-010 a R-011, R-020 a R-024), com ficheiros de venda, movimento, conferência e recibos.
- Vectores de assinatura (chave de teste), depois de o digest ser confirmado.

## Origem e licença

O caso `valid-purchase-invoices` deriva do exemplo `SAF-T AO (PurchaseInvoices).xml` do repositório [assoft-portugal/SAF-T-AO](https://github.com/assoft-portugal/SAF-T-AO) (licença MIT). Os restantes ficheiros são mutações deste. Ver `NOTICE`.
