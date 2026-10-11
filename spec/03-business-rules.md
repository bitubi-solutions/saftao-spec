# 03 — Regras de negócio

Regras que vão além do que o XSD valida. Cada regra tem um identificador (`R-nnn`), um estado de verificação e a fonte. O XSD garante tipos, tamanhos e valores permitidos; **estas** regras garantem coerência entre campos e com a legislação.

## Estados e fontes

| Estado | Significado |
|---|---|
| **verificado** | Consta de legislação publicada no Diário da República (fonte indicada) |
| **verificado (proposta)** | Consta da *Proposta de Decreto Executivo* do Ministério das Finanças, "Regras e requisitos para validação de sistemas de processamento electrónico de facturação dos contribuintes" (2018). Não confirmado que o texto final em vigor é idêntico |
| **por confirmar** | Sem fonte primária, ou com fontes em conflito |

Fontes: **DP 312/18** = Decreto Presidencial n.º 312/18, de 21 de Dezembro, e respectivo anexo "Estrutura de Dados"; **DE 317/20** = Decreto Executivo n.º 317/20, de 14 de Dezembro (anexo "Estrutura de dados", com notas técnicas por campo); **Proposta MinFin** = a proposta acima. Os números entre parênteses (por exemplo, 4.1.4.1) são os índices de campo do anexo.

## Formatos gerais

### R-030 — Datas e horas *(verificado: DP 312/18, anexo)*
Datas no formato `AAAA-MM-DD`; registos temporais no formato `AAAA-MM-DDThh:mm:ss`, **sem** fuso horário e **sem** milissegundos.

### R-031 — Sem valores negativos *(verificado: DP 312/18, anexo)*
Não são aceites valores negativos. Saldos contabilísticos ou transacções com valores negativos são representados a débito ou a crédito (ajustando a representação), e os restantes campos de montantes ou valores são exportados em **valor absoluto**.

### R-032 — Tipo de ficheiro (`TaxAccountingBasis`) *(verificado: DP 312/18, anexo)*
Códigos do tipo de ficheiro: `I` contabilidade integrada com facturação; `C` contabilidade; `F` facturação; `P` facturação parcial; `R` recibos; `S` autofacturação; `A` aquisição de bens e serviços; `Q` aquisição de bens e serviços integrada com a facturação.
O XSD 1.01_01 admite também `E`, que **não** consta do anexo do DP 312/18 *(por confirmar o significado)*.

### R-033 — Tabelas por tipo de ficheiro *(verificado: DP 312/18, anexo)*
| Tipo | Tabelas |
|---|---|
| `I` | Cabeçalho; mestras 2.1 a 2.5; 3 (movimentos contabilísticos); 4.1, 4.2, 4.3, 4.4 |
| `C` | Cabeçalho; 2.1, 2.2, 2.3, 2.5; 3 |
| `F` | Cabeçalho; 2.2, 2.4, 2.5; 4.1, 4.3, 4.4 |
| `R` | Cabeçalho; 2.2, 2.5; 4.4 |
| `S` | Cabeçalho; 2.2, 2.4, 2.5; 4.1 |
| `A` | Cabeçalho; 2.3, 2.5; documentos comerciais de fornecedores |
| `Q` | Cabeçalho; 2.2, 2.3, 2.4, 2.5; 4.1, 4.3, 4.4; documentos comerciais de fornecedores |
| `P` | O anexo define o código mas não lista as tabelas *(por confirmar)* |

Legenda: 2.1 contas, 2.2 clientes, 2.3 fornecedores, 2.4 produtos/serviços, 2.5 impostos; 4.1 documentos de venda (`SalesInvoices`), 4.2 movimentação de mercadorias (`MovementOfGoods`), 4.3 conferência (`WorkingDocuments`), 4.4 recibos (`Payments`).
**Por confirmar:** se a presença ou ausência de uma tabela fora desta lista invalida o ficheiro ou é só desvio de conteúdo; o XSD não o impõe.

### R-034 — Período do ficheiro *(verificado: DP 312/18, anexo)*
O SAF-T (AO) é gerado para um **período anual de tributação**, total ou parcial, desde o início desse período até ao seu termo ou à data da geração, se anterior. O SAF-T de contabilidade é **único** para o período a que respeita. O de facturação pode ser um por estabelecimento, se estes forem independentes do sistema central; se centralizado, é fornecido um único ficheiro.

### R-035 — Completude da exportação *(verificado (proposta))*
O ficheiro contém todos os elementos obrigatórios das tabelas aplicáveis ao tipo de ficheiro **e** todos os campos opcionais que tenham valor na base de dados. Os elementos indicados nas notas técnicas como únicos têm de ter valores únicos dentro da sua tabela.

## Contagens e somas de controlo

Em todas as tabelas de documentos, os documentos anulados (`Status = A`) **contam** para o número de registos mas **não** entram nas somas de controlo.

### R-001 — Documentos de venda: contagem *(verificado: DE 317/20)*
`SalesInvoices/NumberOfEntries` (4.1.1) = número total de documentos, **incluindo** os com `InvoiceStatus = A`.

### R-002 / R-003 — Documentos de venda: somas *(verificado: DE 317/20)*
`SalesInvoices/TotalDebit` (4.1.2) = soma de `DebitAmount` (4.1.4.19.13) das linhas; `TotalCredit` (4.1.3) = soma de `CreditAmount` (4.1.4.19.14). Ambas **excluem** os documentos com `InvoiceStatus = A`.

### R-004 — Razão *(verificado: DE 317/20)*
`GeneralLedgerEntries/TotalDebit` (3.2) = soma de todos os `DebitAmount` das linhas dos movimentos do período; `TotalCredit` (3.3) = soma de todos os `CreditAmount`. `NumberOfEntries` (3.1) = número de movimentos.

### R-005 — Estrutura de um movimento *(verificado: DE 317/20)*
Cada movimento (`Transaction`) tem, em `Lines`, **pelo menos uma linha a débito e uma a crédito**, sem ordem imposta (3.4.3.11).

### R-006 — Movimentos de mercadorias *(verificado: DE 317/20)*
`MovementOfGoods/NumberOfMovementLines` (4.2.1) = número total de linhas com relevância fiscal do período, **incluindo** as de documentos com `MovementStatus = A`.
`TotalQuantityIssued` (4.2.2) = soma de `Quantity` (4.2.3.21.5) das linhas, **excluindo** as de documentos com `MovementStatus = A`.

### R-007 — Documentos de conferência *(verificado: DE 317/20)*
`WorkingDocuments/NumberOfEntries` (4.3.1) conta todos os documentos, incluindo `WorkStatus = A`. `TotalDebit` (4.3.2) e `TotalCredit` (4.3.3) somam `DebitAmount` (4.3.4.14.13) e `CreditAmount` (4.3.4.14.14), excluindo os documentos com `WorkStatus = A`.

### R-008 — Recibos *(verificado: DE 317/20)*
`Payments/NumberOfEntries` (4.4.1) conta todos os recibos, incluindo `PaymentStatus = A`. `TotalDebit` (4.4.2) e `TotalCredit` (4.4.3) somam `DebitAmount` (4.4.4.14.4) e `CreditAmount` (4.4.4.14.5), excluindo os recibos com `PaymentStatus = A`.

### R-009 — Compras *(verificado: DE 317/20)*
`PurchaseInvoices/NumberOfEntries` (4.5.1) = número total de documentos incluídos.

## Identificação de documentos

### R-010 — Formato de identificação única *(verificado: DE 317/20; verificado (proposta))*
`InvoiceNo` (4.1.4.1), `DocumentNumber` (4.2.3.1, 4.3.4.1) e `PaymentRefNo` (4.4.4.1) são texto até 60 caracteres compostos por: tipo de documento (`InvoiceType`, `MovementType`, `WorkType` ou `PaymentType`), um espaço, o código interno do tipo de documento atribuído pela aplicação com o identificador da série, uma barra `/` e o número sequencial dentro da série.
A proposta MinFin descreve a forma `<código interno> <série>/<sequência>` com o padrão `([a-zA-Z0-9./_-])+ ([a-zA-Z0-9]*/[0-9]+)`; exemplo da proposta: `FAC 001/9`. *Os dois textos diferem na redacção (o primeiro inclui o tipo de documento no início); a forma exacta de compor o início está **por confirmar**. O padrão da proposta é o que os vectores de assinatura usam.*

### R-011 — Unicidade *(verificado: DE 317/20)*
Não podem existir registos com a mesma identificação. O mesmo código interno de tipo de documento **não** pode ser usado para tipos de documento diferentes.

### R-012 — Documentos de compra *(verificado: DE 317/20)*
O `InvoiceNo` de um documento de compra (4.5.2.1) é o **número original** do documento do fornecedor.

### R-013 — Referências em notas de crédito de compra *(verificado: DE 317/20)*
`References` (4.5.2.2) é **obrigatório** quando o tipo de documento de compra é `NC` (nota de crédito). Cada `Reference` identifica a factura referida, com a numeração do sistema de origem.

## Totais de um documento

### R-020 — `NetTotal` *(verificado: DE 317/20)*
`DocumentTotals/NetTotal` (4.1.4.20.2) é o total **sem** os impostos da `TaxTable`.

### R-021 — `GrossTotal` *(verificado: DE 317/20)*
`DocumentTotals/GrossTotal` (4.1.4.20.3) é o total **com** impostos e **não** reflecte retenções na fonte (`WithholdingTax`, 4.1.4.21).

### R-022 — Moeda estrangeira *(verificado: DE 317/20; verificado (proposta))*
`Currency` **não** é gerado quando o documento é emitido em AOA. Quando existe: `CurrencyCode` segue a ISO 4217, `CurrencyAmount` é o `GrossTotal` na moeda original e `ExchangeRate` é a taxa usada na conversão para AOA. Para efeitos de assinatura e de exportação, o valor do documento é o **contravalor em AOA**.

### R-023 — Arredondamento do `GrossTotal` *(verificado (proposta))*
O `GrossTotal` exportado é o mesmo valor considerado na assinatura: **arredondado a duas casas decimais**.

### R-024 — Franquias, garantias e retenções *(verificado (proposta))*
Franquias, valores de garantia e retenções na fonte constam de campos próprios, **depois** do apuramento do total com impostos (`GrossTotal`), e **não** influenciam os totais do documento. Não se criam produtos ou serviços para este fim.

## Estados e origem dos documentos

### R-040 — Estados *(verificado: DE 317/20)*
| Campo | Valores e significado |
|---|---|
| `InvoiceStatus` (4.1.4.3.1) | `N` normal; `S` autofacturação; `A` documento anulado; `R` documento de resumo de outros criados noutras aplicações e gerado nesta |
| `MovementStatus` (4.2.3.3.1) | `N` normal; `T` por conta de terceiros; `A` anulado; `F` facturado, ainda que parcialmente; `R` resumo de outros documentos |
| `WorkStatus` (4.3.4.3.1) | `N` normal; `A` anulado; `F` facturado, ainda que parcialmente |
| `PaymentStatus` (4.4.4.9.1) | `N` recibo normal e vigente; `A` recibo anulado |
| `TransactionType` (3.4.3.7) | `N` normal; `R` regularizações do período de tributação; `A` apuramento de resultados; `J` movimentos de ajustamento |

### R-041 — Origem (`SourceBilling` / `SourcePayment`) *(verificado: DE 317/20)*
`P` documento produzido na aplicação; `I` documento integrado, produzido noutra aplicação; `M` documento proveniente de recuperação ou de emissão manual.

### R-042 — Integração de documentos de outros sistemas *(verificado (proposta))*
- O sistema integrador **não recalcula nem modifica** os documentos integrados, incluindo a sua identificação única.
- Os documentos integrados ficam em séries/tipos **distintos e autónomos** dos da emissão própria, como cópias do original, e uma série **não mistura** origens.
- `Hash` igual ao do sistema emissor; `SourceBilling = I`; `HashControl` conforme `04-signature.md`.

### R-045 — Origem consistente numa série *(verificado (proposta); corroborado na prática)*
Uma série/tipo de documento não mistura documentos de origens diferentes (por exemplo, `SourceBilling = P` e `I` na mesma série). Registo prático (não normativo): o validador do portal da AGT rejeitou uma cadeia de hash em que um documento `I` estava no meio de uma série de documentos `P`.

### R-043 — Recuperação de documentos manuais e de duplicados *(verificado (proposta))*
Documentos recuperados de impressos manuais ou de duplicados (após falha do sistema) entram em **série específica**, de periodicidade anual ou superior, com numeração sequencial própria **iniciada em 1**, e `SourceBilling = M`. A data do documento é a do documento original. Documentos que referenciem um documento recuperado usam a série e o número **originais**. Após uma falha com reposição de cópia de segurança, as séries em uso são encerradas e criam-se novas.

### R-044 — Documentos rectificativos *(verificado (proposta), aplicação a impressão)*
Os documentos não contêm valores negativos; correcções fazem-se com notas de débito e de crédito. Excepção: valores negativos em anulações de registos que já integram o documento ou em acertos de estimativas de prestações continuadas, nunca superiores ao valor positivo da mesma rubrica.

## Assinatura

As regras de assinatura, `Hash` e `HashControl` estão em [`04-signature.md`](04-signature.md).

## Ainda por especificar ou confirmar

- **Relação aritmética** entre `NetTotal`, `TaxPayable` e `GrossTotal`, e a tolerância de arredondamento: o anexo não a impõe no trecho lido. *(por confirmar)*
- **Equilíbrio** entre `TotalDebit` e `TotalCredit` no razão: não afirmado no trecho lido. *(por confirmar)*
- **Regras de linha** (cálculo de impostos, descontos, isenções e respectivos códigos `M..`) e das tabelas de impostos e produtos. *(por transcrever do DE 317/20)*
- **`Payments`**: regras de `PaymentMechanism`, `WithholdingTax` e relação com documentos pagos. *(por transcrever)*
- **Datas dentro do período**: relação entre `StartDate`/`EndDate` e as datas dos documentos e movimentos (`Period`). *(por transcrever)*
- Texto final em vigor das regras marcadas **(proposta)**.
