# 03 — Regras de negócio

Regras que vão além do que o XSD valida. Cada regra tem um identificador (`R-nnn`), o estado de verificação e a fonte. O XSD garante tipos, tamanhos e valores permitidos; **estas** regras garantem coerência entre campos.

Fonte principal: Decreto Executivo n.º 317/20, de 14 de Dezembro, anexo "Estrutura de dados" (ver `sources.md`). Números de campo entre parênteses referem-se ao anexo.

## Contagens e somas de controlo

### R-001 — Contagem de documentos de venda *(verificado)*
`SalesInvoices/NumberOfEntries` (4.1.1) é o número total de documentos, **incluindo** os que têm `InvoiceStatus = A` (anulado).

### R-002 — Total a débito de vendas *(verificado)*
`SalesInvoices/TotalDebit` (4.1.2) é a soma de `DebitAmount` (4.1.4.19.13) das linhas, **excluindo** os documentos com `InvoiceStatus = A`.

### R-003 — Total a crédito de vendas *(verificado)*
`SalesInvoices/TotalCredit` (4.1.3) é a soma de `CreditAmount` (4.1.4.19.14) das linhas, **excluindo** os documentos com `InvoiceStatus = A`.

### R-004 — Totais do razão *(verificado)*
`GeneralLedgerEntries/TotalDebit` (3.2) e `TotalCredit` (3.3) são a soma, respectivamente, de todos os `DebitAmount` e `CreditAmount` dos movimentos do período. `NumberOfEntries` (3.1) é o número de movimentos.

### R-005 — Estrutura mínima de um movimento *(verificado)*
Cada movimento contabilístico (`Transaction`) tem de ter, em `Lines`, **pelo menos uma linha a débito e uma a crédito**, sem imposição de ordem (3.4.3.11).

> Os anexos equivalentes para `WorkingDocuments` e `MovementOfGoods` (4.2, 4.3) têm contagens análogas. Ainda por transcrever nesta versão da spec.

## Identificação de documentos

### R-010 — Formato de `InvoiceNo` *(verificado)*
`InvoiceNo` (4.1.4.1, texto até 60 caracteres) é composto, por esta ordem: tipo do documento (`InvoiceType`), um espaço, o **código interno do tipo de documento** atribuído pela aplicação, o identificador da série, uma barra `/` e o número sequencial dentro da série.
Exemplo da forma: `FT FT2026/1` (tipo `FT`, código interno `FT`, série `2026`, sequência `1`) *(exemplo ilustrativo, não oficial)*.

### R-011 — Unicidade *(verificado)*
Não podem existir dois registos com a mesma identificação. O mesmo código interno de tipo de documento **não** pode ser usado para tipos de documento diferentes.

## Totais de um documento

### R-020 — `NetTotal` *(verificado)*
`DocumentTotals/NetTotal` (4.1.4.20.2) é o total do documento **sem** os impostos da `TaxTable`.

### R-021 — `GrossTotal` *(verificado)*
`DocumentTotals/GrossTotal` (4.1.4.20.3) é o total **com** impostos, e **não** reflecte retenções na fonte (`WithholdingTax`, 4.1.4.21).

### R-022 — Moeda estrangeira *(verificado)*
O elemento `Currency` **não** deve ser gerado quando o documento é emitido em AOA. Quando existe: `CurrencyCode` segue a ISO 4217; `CurrencyAmount` é o `GrossTotal` na moeda original; `ExchangeRate` é a taxa usada na conversão para AOA.

## Regras ainda por transcrever ou confirmar

- Relação aritmética entre `NetTotal`, `TaxPayable` e `GrossTotal` (R-0xx): **por confirmar** se o anexo a impõe como igualdade exacta, e com que tolerância de arredondamento.
- Regras de `InvoiceStatus` (`N`, `A`, `S`, `R`, etc.) e transições: **por transcrever**.
- Regras específicas de `Payments`, `PurchaseInvoices`, `MovementOfGoods` e `WorkingDocuments`: **por transcrever**.
- Equilíbrio entre total a débito e a crédito no razão: o anexo não o afirma no trecho lido; **por confirmar**.

Quando uma regra passar a **verificada** e tiver caso de teste, é acrescentada aqui e em `conformance/`.
