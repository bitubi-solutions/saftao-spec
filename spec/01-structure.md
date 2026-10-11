# 01 — Estrutura do ficheiro

Namespace: `urn:OECD:StandardAuditFile-Tax:AO_1.01_01`. Elemento raiz: `AuditFile`. Versão (`AuditFileVersion`): `1.01_01`. *(verificado: XSD)*

```
AuditFile
├── Header                 metadados do ficheiro e da empresa
├── MasterFiles            dados mestre
│   ├── GeneralLedgerAccounts   plano de contas (opcional)
│   ├── Customer                clientes (opcional, vários)
│   ├── Supplier                fornecedores (opcional, vários)
│   ├── Product                 produtos e serviços (opcional, vários)
│   └── TaxTable                tabela de impostos (opcional)
├── GeneralLedgerEntries   movimentos contabilísticos (opcional)
└── SourceDocuments        documentos de origem (opcional)
    ├── SalesInvoices      facturas de venda e equivalentes
    ├── MovementOfGoods    documentos de transporte/movimento de mercadorias
    ├── WorkingDocuments   documentos de trabalho (pró-formas, orçamentos, ...)
    ├── Payments           recibos e pagamentos
    └── PurchaseInvoices   facturas de compra
```

A ordem dos elementos é a do XSD (`xs:sequence`); o ficheiro tem de a respeitar. O detalhe de cada elemento, obrigatoriedade e restrições está em [`02-fields.md`](02-fields.md).

## Notas *(verificado: XSD)*

- Na versão 1.01_01 os cinco grupos de `SourceDocuments` são opcionais; um ficheiro pode conter só um deles (por exemplo, só `PurchaseInvoices`, como no exemplo de referência).
- O `Header` identifica também o software produtor: `SoftwareValidationNumber` (formato `<número>/AGT/<ano>`, ou `0` para software não validado), `ProductID` (`<produto>/<empresa>`), `ProductVersion` e `ProductCompanyTaxID`.
- `CurrencyCode` do `Header` admite `AOA` ou `USD`.
- `Country` do endereço da empresa é fixo `AO`; nos clientes e fornecedores admite códigos de país ISO ou `Desconhecido`.
- Valores monetários usam o tipo `SAFmonetaryType` (decimal); datas usam o tipo `SAFAODateSpan` (intervalo 2000-01-01 a 9999-12-31).
- O próprio XSD indica `Status: Development` para esta versão.
