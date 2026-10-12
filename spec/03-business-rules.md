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
Códigos do tipo de ficheiro: `I` contabilidade integrada com facturação; `C` contabilidade; `F` facturação; `P` facturação parcial; `R` recibos; `S` autofacturação; `A` aquisição de bens e serviços; `Q` aquisição de bens e serviços integrada com a facturação; `E` **facturação para o Estado** (este último acrescentado pelo DE 317/20 *(verificado: DE 317/20)*; não consta do DP 312/18).
O tipo `R`, `S` e outros só se indicam se o programa emite *apenas* esse tipo de documento; caso contrário usa-se `C` ou `F` *(verificado: DE 317/20, nota (a) ao campo 1.4)*.

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

## Ficheiro, cabeçalho e tabelas auxiliares

### R-036 — Obrigatoriedade *(verificado: DE 317/20)*
Na coluna "Obrigatório" do anexo: `*` campo de preenchimento obrigatório; `#` campo de escolha alternativa ou dependente de condições; **em branco**, campo opcional que **deve** ser preenchido sempre que a informação exista no repositório de dados da aplicação, mediante prova documental.

### R-037 — Autofacturação *(verificado: DE 317/20)*
A geração do ficheiro de autofacturação é da responsabilidade do **efectivo emitente** (o cliente que se autofactura), que o disponibiliza sempre que ao fornecedor seja exigido o SAF-T. O ficheiro contém: `Header` com os campos 1.2 a 1.8 com os dados do **fornecedor** e `TaxAccountingBasis = S`; `Customer` com os dados do **emitente**; `Product` com os produtos dos documentos; e `SalesInvoices` com os documentos do fornecedor em que `InvoiceStatus = S`.

### R-038 — Exportação de vários meses *(verificado: DE 317/20)*
Ao exportar vários meses, aceita-se, em casos justificados, que as tabelas 2.2 a 2.5 (e, em aplicações integradas, também 2.1 e 3) sejam exportadas **uma só vez**, no último período extraído.

### R-039 — Ficheiros independentes *(verificado: DE 317/20)*
Se a contabilidade e a facturação geram ficheiros independentes, ambos contêm as tabelas **comuns** (Header, Customer, TaxTable e Payments, quando existam) e cada um a sua informação específica: contabilidade (2.1 contas, 2.3 fornecedores, 3 movimentos); facturação (2.3 fornecedores, 2.4 produtos, 4.1 vendas, 4.3 conferência).

### R-050 — Cabeçalho: identificação *(verificado: DE 317/20)*
- `TaxRegistrationNumber` (1.3): NIF angolano, **sem espaços e sem prefixo de país**.
- `FiscalYear` (1.8): aplicam-se as regras do Código do Imposto Industrial quando o período contabilístico coincide com o ano civil.
- `CurrencyCode` (1.11): moeda padrão dos campos monetários; **"AOA"**. O XSD admite também `USD`; o DE 317/20 manda preencher `AOA`.
- `DateCreated` (1.12): data de criação do ficheiro XML.
- `TaxEntity` (1.13): no ficheiro de **facturação**, o estabelecimento (posto de venda) a que respeita o ficheiro, ou `Global`; nos ficheiros de **contabilidade ou integrados**, `Sede`.
- `ProductCompanyTaxID` (1.14): NIF da entidade produtora do software.
- `SoftwareValidationNumber` (1.15): `NNN/AGT/AAAA`; `0` se não aplicável.
- `ProductID` (1.16): `Nome da aplicação/Nome da empresa produtora do software`.
- `ProductVersion` (1.17): versão da aplicação que produz o ficheiro.

### R-060 — Plano de contas (`GeneralLedgerAccounts`) *(verificado: DE 317/20)*
- Exporta-se o plano previsto no sistema de normalização contabilística e disposições do respectivo sector. **Não** se exportam registos das **classes** de contas.
- Constam **todas** as contas, incluindo as integradoras, **até às contas do Razão**.
- Em contas agregadoras com subcontas devedoras e credoras, evidenciam-se na agregadora os saldos devedores **e** credores.
- `OpeningDebitBalance`/`OpeningCreditBalance`: saldos do **início** do período de tributação. `ClosingDebitBalance`/`ClosingCreditBalance`: saldos do **fim** do período ou da data de geração, se anterior.
- `GroupingCategory`: `GR` conta de 1.º grau da contabilidade geral; `GA` agregadora/integradora geral; `GM` de movimento geral; `AR`, `AA`, `AM` os equivalentes da contabilidade analítica.
- Excepto contas de 1.º grau, indica-se a conta agregadora (`GroupingCode`) do grau imediatamente superior, **com a mesma estrutura** do `AccountID`.

### R-061 — Clientes (`Customer`) *(verificado: DE 317/20)*
- Contém todos os registos movimentados no período e os **implícitos** nos movimentos que não constem do ficheiro de clientes da aplicação (por exemplo, uma factura só com o nome e NIF do cliente: exporta-se como cliente).
- **Unicidade:** não pode haver mais de um registo com o mesmo `CustomerID`.
- Um cliente já existente, com documentos emitidos e **sem NIF**, **não pode ter o nome alterado**; a limitação cessa quando se averba o NIF.
- **Consumidor final:** cria-se um cliente genérico com a designação `Consumidor final` e NIF `999999999`.
- `AccountID`: conta-corrente do cliente no plano de contas, se definida; senão `Desconhecido`.
- Morada: campos preenchidos com `Desconhecido` em sistemas não integrados quando a informação não é conhecida, e nas operações com consumidor final. `Country` segue a ISO 3166-1 alpha-2.
- `SelfBillingIndicator`: `1` se há acordo de autofacturação entre cliente e fornecedor, `0` caso contrário.

### R-062 — Fornecedores (`Supplier`) *(verificado: DE 317/20)*
Contém todos os registos movimentados no período. **Unicidade** do `SupplierID`. `AccountID`: conta-corrente do fornecedor no plano de contas, se definida; senão `Desconhecido`. O NIF não leva prefixo de país.

### R-063 — Produtos e serviços (`Product`) *(verificado: DE 317/20)*
- Catálogo de produtos e tipos de serviço movimentados, mais os registos **implícitos** nos movimentos que não existam na tabela da aplicação (por exemplo, uma linha de portes: exporta-se como produto).
- Incluem-se também impostos, taxas, ecotaxas e encargos parafiscais mencionados no documento, que contribuam ou não para a base tributável do IVA ou do IS, **excepto IVA e IS**, que vão para a `TaxTable`.
- O programa **não pode permitir alterar** a descrição de um produto já com documentos emitidos.
- `ProductType`: `P` produtos; `S` serviços; `O` outros (portes debitados, adiantamentos recebidos, alienação de activos); `E` impostos especiais de consumo (IEC); `I` impostos, taxas e encargos parafiscais, excepto IVA, IS e IEC.
- `ProductNumberCode`: o código EAN (código de barras); se não existir, o valor de `ProductCode`.
- `ProductDescription`: denominação usual do bem ou serviço, com os elementos necessários para determinar a taxa de imposto aplicável.

### R-070 — Tabela de impostos (`TaxTable`) *(verificado: DE 317/20)*
- `TaxType`: `IVA`, `IS` (imposto do selo) ou `NS` (não sujeição a IVA ou IS).
- `TaxCode`: se `IVA`: `NOR` taxa normal, `ISE` isenta, `OUT` outros (regimes especiais). Se `IS`: o código da verba, ou `ISE`. Se não sujeição: `NS`. Em recibos emitidos sem imposto discriminado: `NA`.
- `TaxCountryRegion`: ISO 3166-1 alpha-2; para Cabinda, `AO-CAB` (espaço fiscal da região de Cabinda).
- `TaxExpirationDate`: última data legal de aplicação da taxa, se esta mudar durante o período.
- `TaxPercentage`: obrigatório se o imposto é uma percentagem. `TaxAmount`: obrigatório se é uma verba fixa de imposto do selo. Em isenção ou não sujeição, o valor é `0`.

## Razão (movimentos contabilísticos)

### R-080 — Movimentos *(verificado: DE 317/20)*
- Registam-se os movimentos do período de exportação. **Não** se exportam movimentos de **abertura**: estão reflectidos nos saldos de abertura do plano de contas (R-060).
- `TransactionID` (3.4.3.1): único e correspondente ao número de documento contabilístico, formado por **data do documento, identificador do diário e número de arquivo do documento**, separados por espaços (`TransactionDate`, `JournalID`, `DocArchivalNumber`).
- `Period` (3.4.3.3): número do mês do período de tributação, de `1` a `12`, contado desde o início do período; `13` a `16` para movimentos do último mês relacionados com o apuramento do resultado (inventários, depreciações, ajustamentos, apuramento de resultados).
- `TransactionDate`: data impressa no documento de suporte. `GLPostingDate`: data relevante para efeitos contabilísticos. `DocArchivalNumber`: número do documento dentro do diário, que permita aceder ao documento de origem.
- `CustomerID` é **obrigatório** se o cliente é não residente ou a transacção é uma venda que deva figurar no anexo/declaração anual ou no anexo I da declaração periódica de IVA. `SupplierID` é obrigatório se o fornecedor é não residente ou a compra deve figurar no anexo/declaração anual. Cada um indica a chave do registo em `Customer`/`Supplier`.
- Em cada linha: `RecordID` (chave única da linha no documento) e `SourceDocumentID` (tipo e número do documento comercial relacionado; em aplicações integradas, a numeração do campo de origem).

## Documentos comerciais: regras comuns

### R-090 — Tabelas de documentos *(verificado: DE 317/20)*
- **Não se exportam linhas sem relevância fiscal** (descrições técnicas, instruções de montagem, condições de garantia).
- O **código interno do tipo de documento** não pode ser usado em tipos de documento diferentes, qualquer que seja a tabela.
- Cada série tem numeração **pelo menos anual**.
- **Linhas** exportadas **pela mesma ordem** que no documento original.
- `Reason` (nos estados): razão da alteração de estado do documento.
- `Hash` e `HashControl`: ver `04-signature.md`. `Hash` fica `0` quando **não há obrigatoriedade de validação**; `HashControl` fica `0` se o documento foi gerado por **programa não validado**.
- `TransactionID` no documento comercial: **obrigatório** em sistemas integrados de contabilidade e facturação (mesmo que o tipo de ficheiro não contenha as tabelas contabilísticas), quando o documento dá origem a registo contabilístico.

### R-091 — Linhas e totais (comum a vendas, movimento, conferência e recibos) *(verificado: DE 317/20)*
- `DebitAmount`: valor da linha **sem imposto**, dos documentos a lançar a **débito** na conta de vendas, **deduzido** de descontos de linha e de cabeçalho. `CreditAmount`: o equivalente a **crédito**.
- `UnitPrice`: preço unitário sem imposto, **deduzido** de descontos; `0.00` quando não valorizado na base de dados.
- `TaxBase`: valor tributável unitário que **não concorre** para o `NetTotal`; é a base de cálculo dos impostos da linha. O sinal com que o imposto concorre para o `TaxPayable` resulta de a linha ter `DebitAmount` ou `CreditAmount`. Se há obrigatoriedade de preencher `TaxBase`, `UnitPrice` fica `0.00`.
- `SettlementAmount` (desconto de linha): reflecte **todos** os descontos (a proporção dos globais e os da própria linha) que afectam o `GrossTotal`.
- `IECAmount`: montante do imposto especial de consumo contido na base tributável da linha, quando não está discriminado em linha independente com `ProductType = E`.
- `Tax` (imposto da linha): `TaxType` (`IVA`, `IS`, `NS`), `TaxCode` (como R-070), `TaxPercentage` (obrigatório se percentagem; refere-se ao `DebitAmount` ou `CreditAmount`; `0` em isenção ou não sujeição) e `TaxAmount` (obrigatório em verba fixa de imposto do selo; **multiplicado pela `Quantity` concorre para o `TaxPayable`**).
- `TaxExemptionReason` e `TaxExemptionCode`: **obrigatórios** quando `TaxPercentage` ou `TaxAmount` são `0`; indicam o preceito legal e o código do motivo; preenchem-se também nos casos de **não sujeição**.
- `Settlement` (acordos): `SettlementDiscount` regista acordos de desconto **futuro**; `SettlementAmount` é o valor acordado para esse desconto e **não afecta** o valor presente do `GrossTotal`.
- `PaymentMechanism`: `CC` cartão de crédito; `CD` cartão de débito; `CH` cheque bancário; `CI` crédito documentário internacional; `CO` cheque ou cartão oferta; `CS` compensação de saldos em conta corrente; `DE` dinheiro electrónico; `MB` referências de pagamento para Multicaixa; `NU` numerário; `OU` outros meios; `PR` permuta de bens; `TB` transferência bancária ou débito directo autorizado. Em pagamentos mistos indicam-se os montantes por meio e data.
- `WithholdingTax`: `WithholdingTaxType` indica o imposto retido (`IRT`, `II`, `IS`, `IVA`, `IPU`, `IAC`, `OU`); `WithholdingTaxDescription` o normativo legal, ou o código da verba se for `IS`.

## Documentos de venda (`SalesInvoices`)

### R-100 — Conteúdo e anulação *(verificado: DE 317/20)*
- Constam **todos** os documentos de venda e rectificativos emitidos, **incluindo os anulados** (`A`), para permitir verificar a sequencialidade de cada série.
- **Anulação** (`InvoiceStatus` de `N` para `A`) só é possível em **programa validado pela AGT**, e deve servir **apenas** para rectificar dados de cabeçalho (erro no nome ou NIF do cliente). Em qualquer outro caso emite-se **nota de crédito**.
- O software coloca uma **marca de água "Anulado"** na impressão e reimpressão, e **alerta** o utilizador se o SAF-T relativo ao documento já foi exportado.
- Documento anulado por **emissão inválida**: o original **nunca** fica na posse do cliente, mantém-se no arquivo do emitente.

### R-101 — Tipos de documento de venda *(verificado: DE 317/20)*
`InvoiceType`: `FT` factura; `FR` factura/recibo; `GF` factura genérica; `FG` factura global; `AC` aviso de cobrança; `AR` aviso de cobrança/recibo; `ND` nota de débito; `NC` nota de crédito; `AF` factura/recibo (autofacturação); `TV` talão de venda. No **sector segurador**, quando o documento não conste em `WorkingDocuments`, admitem-se ainda tipos adicionais (o XSD lista `RP`, `RE`, `CS`, `LD`, `RA`).

### R-102 — Indicadores e actividade *(verificado: DE 317/20)*
- `SelfBillingIndicator` (4.1.4.9.1): `1` se respeita a autofacturação, `0` caso contrário.
- `CashVATSchemeIndicator` (4.1.4.9.2): `1` se há adesão (ao regime de IVA de caixa), `0` caso contrário.
- `ThirdPartiesBillingIndicator` (4.1.4.9.3): `1` se a facturação é emitida em nome e por conta de terceiros, `0` caso contrário. *O XSD admite os valores `0` a `3`; o DE 317/20 só descreve `0` e `1` (por confirmar o significado de `2` e `3`).*
- `CAECode`: código CAE da actividade relacionada com a emissão do documento.

### R-103 — Notas de crédito e referências *(verificado: DE 317/20)*
- `References` (4.1.4.19.10): **obrigatório** quando `InvoiceType = NC`. `Reference` é o identificador único da factura referida (estrutura de numeração do sistema de origem) e `Reason` o motivo.
- `OrderReferences` (4.1.4.19.2): **obrigatório** quando a nota de crédito (`NC`) respeita a **documento do ano anterior**; `OriginatingON` indica o tipo, a série e o número do documento que suporta a emissão, e `OrderDate` a sua data. Se o documento está contido no SAF-T, usa-se a numeração do campo de origem.

### R-104 — Entrega *(verificado: DE 317/20)*
Local e data de descarga onde os artigos são colocados à disposição do cliente, ou de quem este indicar em operações triangulares; nestas, indicam-se o local de entrega e o NIF de quem recebeu. No sector segurador, as datas de entrega/recolha indicam o **fim** e o **início** do período de cobertura do risco. `VehicleNumber` (matrícula do veículo ou meio de expedição); `SerialNumber`: número de série do produto (VIN, IMEI, ISSN, ISAN).

## Movimentos de mercadorias (`MovementOfGoods`)

### R-110 — Conteúdo *(verificado: DE 317/20)*
- Exportam-se os **documentos de transporte** (guias de transporte, de remessa) que sirvam como tal.
- **Não** se exportam aqui documentos que devam constar de `SalesInvoices` e que também serviram de transporte (por exemplo, facturas).
- `MovementType`: `GR`, `GT`, `GA`, `GD` (valores do XSD; o DE 317/20 lido não os descreve por extenso).
- `CustomerID`: se o destinatário não é conhecido, usa-se o cliente genérico de R-061. `SupplierID`: em guias de devolução, ou de transporte de bens produzidos ou montados sob encomenda com materiais fornecidos pelo dono da obra (trabalho a feitio).
- Documentos **não valorizados** na base de dados: os campos monetários (`UnitPrice`, `GrossTotal`, `TaxPayable`, `NetTotal`, etc.) levam `0.00`. A estrutura de valores só se cria nos documentos valorizados.
- `ARCNo` (4.2.3.21.16.1, código de referência administrativo ou D.U.): preenche-se com o código atribuído após a validação do documento administrativo.
- Existe um campo (4.2.3.2, sem correspondência no XSD) a preencher com `0` **até à sua regulamentação**.

## Documentos de conferência (`WorkingDocuments`)

### R-120 — Conteúdo *(verificado: DE 317/20)*
- Exportam-se **quaisquer outros** documentos emitidos, independentemente da designação, susceptíveis de apresentação ao cliente para conferência de mercadorias ou de prestação de serviços, mesmo que objecto de facturação posterior. **Não** se exportam os que devam constar de `SalesInvoices` ou de `MovementOfGoods`.
- `WorkType`: `CM` consultas de mesa; `GC` guia de consignação; `GR` guia de remessa; `NR` nota de remessa; `FO` folhas de obra; `NE` nota de encomenda; `OU` outros; `OR` orçamentos; `PP` pró-forma; `DC` documentos emitidos susceptíveis de apresentação ao cliente para conferência. No sector segurador, tipos adicionais (o XSD lista `PF`, `RP`, `RE`, `CS`, `LD`, `RA`).
- `CAECode`: código CAE da actividade relacionada com a emissão. Campos monetários não valorizados na base de dados: `0.00`.

## Recibos (`Payments`)

### R-130 — Conteúdo *(verificado: DE 317/20)*
- Exportam-se os recibos criados **após a entrada em vigor** desta estrutura, dos tipos de `PaymentType`: `RC` recibo emitido; `AR` aviso de cobrança/recibo; `RG` outros recibos emitidos.
- Cada linha indica o **tipo, série e número** da factura ou documento rectificativo a que respeita o pagamento (`SourceDocumentID`), e a **data** desse documento. Se está contido no SAF-T, usa-se a mesma numeração.
- A estrutura de impostos gera-se também em qualquer outro recibo que **discrimine** impostos (`TaxType`).
- `GrossTotal` do recibo **não** reflecte retenções na fonte (`WithholdingTax`).
- `PaymentMechanism` e `WithholdingTax`: ver R-091.

## Compras (`PurchaseInvoices`)

### R-140 — Conteúdo *(verificado: DE 317/20)*
- Produz-se um **ficheiro independente** de aquisição de bens e serviços (tipos `A` ou `Q`).
- `PurchaseType`: `FT`, `FR`, `GF`, `FG`, `AC`, `AR`, `AF`, `TV`, `NL` nota de liquidação, `NC` nota de crédito; e `RC` recibo, **só** para contribuintes no **regime de caixa**.
- `Hash` (4.5.2.3): os **4 valores** (posições 1, 11, 21 e 31) do `Hash` constantes no documento impresso, ou `0` se não houver esta informação. Em compras **não** é a assinatura de 172 caracteres.
- `DeductibleTaxType` (4.5.2.9.4.4, tipo de IVA dedutível): `MFI` meios fixos e investimentos; `INV` existências/inventário; `OBC` outros bens de consumo; `SERV` serviços; `IMPT` importação; `SCE` serviços contratados no estrangeiro. Acompanha `DeductiblePercentage` (percentagem de imposto deduzido).
- `WithholdingTax`: `IVA` quando sujeito a retenção/cativação; indica-se o normativo legal ou a percentagem aplicável.
- `References` (ver R-013) é obrigatório em notas de crédito.


### R-046 — Unicidade e integridade referencial do XSD *(verificado: XSD)*
O XSD define restrições de identidade (`xs:unique` e `xs:keyref`) que **fazem parte da validação do esquema**. Uma biblioteca que valide o XSD tem de as aplicar; uma que **gere classes** a partir do XSD e não valide o documento **não** as herda automaticamente e tem de as implementar à mão.

| Tipo | Restrições |
|---|---|
| **Unicidade** | `AccountID`; `CustomerID`; `SupplierID`; `ProductCode`; `JournalID`; `TransactionID`; `InvoiceNo` (vendas); `DocumentNumber` (movimentos e conferência, cada um na sua tabela); `PaymentRefNo` |
| **Referência a chave existente** | `GroupingCode` → `AccountID`; `AccountID` das linhas de débito e de crédito do razão → `AccountID`; `CustomerID` nos movimentos do razão, vendas, movimentos de mercadorias, conferência e recibos → `CustomerID`; `SupplierID` no razão, movimentos de mercadorias e compras → `SupplierID`; `ProductCode` das linhas de vendas, movimentos e conferência → `ProductCode` |

*Nota:* o `InvoiceNo` dos documentos de **compra** não tem restrição de unicidade no XSD (é o número do fornecedor).

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

### R-010 — Formato de identificação única *(verificado: DE 317/20 e XSD)*
`InvoiceNo` (4.1.4.1), `DocumentNumber` (4.2.3.1, 4.3.4.1) e `PaymentRefNo` (4.4.4.1) são texto até 60 caracteres: **tipo do documento, um espaço, o identificador da série (que inclui o código interno do tipo atribuído pela aplicação), uma barra `/` e o número sequencial dentro da série**.
O XSD impõe o padrão `[^ ]+ [^/^ ]+/[0-9]+` (por exemplo, `FT 2019A1/12360`, como no exemplo oficial). A proposta MinFin (2018) descreve `([a-zA-Z0-9./_-])+ ([a-zA-Z0-9]*/[0-9]+)`; o padrão do XSD, mais recente, prevalece.
Nas **compras** (`PurchaseInvoices`) o `InvoiceNo` é o número original do documento do fornecedor, em texto livre (ver R-012).

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

## O que o texto legal não impõe, mas o validador da AGT verifica

O DE 317/20 **não** afirma, nos campos lidos, as relações abaixo. Porém, **produtores reportam que o validador da AGT as verifica** (ver [`06-validator-observations.md`](06-validator-observations.md), observações O-001 a O-007). São, por isso, candidatas a verificação num **modo estrito** opcional, e **não** a erros por defeito:

- Cálculo de `TaxPayable`, de `NetTotal` e de `GrossTotal` por documento, com os descontos já deduzidos nas linhas (O-001, O-002).
- Valor das linhas e sua relação com preço e quantidade, com sensibilidade a arredondamento (O-004).
- Soma dos `CreditAmount` ≥ soma dos `DebitAmount` por documento (O-005; a versão anterior do validador exigia `>`).
- `GrossTotal` de uma nota de crédito ≤ `GrossTotal` do documento referido (O-006; contestado, com falsos positivos reportados).

Continuam **sem fonte legal e sem observação**: igualdade entre `TotalDebit` e `TotalCredit` do razão, e relação entre `StartDate`/`EndDate` e as datas dos documentos.

## Ainda por confirmar

- Texto final em vigor das regras marcadas **(proposta)**.
- Significado exacto dos tipos de movimento `GT`, `GA`, `GD` (o XSD define-os; o DE 317/20 lido não os descreve por extenso).
- Tabelas de cada tipo de ficheiro para `P` e `E`.
- Códigos de motivo de isenção `M..` (lista de códigos): o anexo remete para tabela própria e o repo de origem tem `TaxExemptions.xml/json`, ainda não incluídos nesta spec.
