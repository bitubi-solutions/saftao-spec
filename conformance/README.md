# Testes de conformidade

Casos partilhados por todas as bibliotecas `saftao-*`.

## Formato

Cada caso é um par em `cases/`:

- `<nome>.xml`: o ficheiro SAF-T a validar.
- `<nome>.expected.json`: `{"valid": true|false, "reason": "..."}`.

Uma biblioteca **passa** um caso se o seu resultado de validação (`valido`/`inválido`) coincidir com `valid`. As mensagens de erro podem diferir entre linguagens e **não** são comparadas.

## Casos actuais

| Caso | Esperado | O que testa |
|---|---|---|
| `valid-purchase-invoices` | válido | Ficheiro de referência de facturas de compra |
| `invalid-version` | inválido | `AuditFileVersion` diferente de `1.01_01` |
| `invalid-missing-company-name` | inválido | `CompanyName` em falta no `Header` |
| `invalid-currency` | inválido | `CurrencyCode` fora de `AOA`/`USD` |
| `invalid-accounting-basis` | inválido | `TaxAccountingBasis` fora dos valores permitidos |
| `invalid-company-country` | inválido | `Country` do endereço da empresa diferente de `AO` |
| `invalid-not-xml` | inválido | XML mal formado |

Todos os casos foram confirmados com o validador de referência (`tools/validate.py`, baseado em libxml2 através de lxml).

## Próximos casos

- Regras de `03-business-rules.md` (R-001 a R-022), um ou mais casos por regra.
- Vectores de assinatura (`signature/`), **só** depois de o algoritmo estar verificado (ver `spec/04-signature.md`).

## Origem e licença

O caso `valid-purchase-invoices` deriva do exemplo `SAF-T AO (PurchaseInvoices).xml` do repositório [assoft-portugal/SAF-T-AO](https://github.com/assoft-portugal/SAF-T-AO) (licença MIT). Os restantes casos inválidos são mutações deste ficheiro. Ver `NOTICE`.
