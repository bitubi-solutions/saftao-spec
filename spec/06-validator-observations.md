# 06 — Observações sobre o validador da AGT

> **Estado: observações comunitárias, NÃO normativas.** O validador de produtores de software do portal da AGT aplica regras que não constam do XSD nem do texto legal que lemos. Esta página regista o que produtores de software **reportaram publicamente**, com a referência do issue, para orientar a implementação e dar origem a testes. Nada aqui foi confirmado por nós contra o portal.

## Fonte e limites

- Fonte: os issues públicos do repositório [assoft-portugal/SAF-T-AO](https://github.com/assoft-portugal/SAF-T-AO/issues) (2020 a 2025), onde produtores colam as mensagens do validador. A referência `#n` é o número do issue.
- O validador **muda ao longo do tempo** e teve falhas reconhecidas pelos próprios produtores (alguns relatos indicam falsos positivos). Cada observação tem a data aproximada do issue.
- Respostas de outros utilizadores nos issues **não são oficiais**. Uma observação só passa a regra (`R-nnn`) quando houver fonte legal ou confirmação por teste.
- Não se reproduzem dados pessoais nem ficheiros de terceiros.

## Conclusão principal

O validador **não usa só o esquema**: valida também razões de cálculo e regras de negócio (#36, #44). Um ficheiro que passa o XSD pode ser rejeitado. É por isso que as bibliotecas devem poder oferecer um **modo estrito** que aplique estas verificações (ver o fim).

## Observações

Cada linha: identificador `O-nnn`, o que se observou, os issues, e o estado.

### Cálculos

| ID | Observação | Issues | Estado |
|---|---|---|---|
| O-001 | `TaxPayable` de cada documento é verificado: *"o `TaxPayable` do documento X está mal calculado"* | #17, #32, #33, #66 | observado |
| O-002 | Um **desconto** (`SettlementAmount`) tem de estar **já deduzido** em `UnitPrice`, `CreditAmount` e `DebitAmount`. Exemplo reportado: 100 unidades, preço unitário 0,45 (e não 0,55), `CreditAmount` 45,00, desconto 10,00 → `TaxPayable` 6,30, `NetTotal` 45,00, `GrossTotal` 51,30 (IVA 14%) | #36 | observado |
| O-003 | `TotalCredit` e `TotalDebit` de cada secção (vendas, conferência, recibos) são verificados | #33, #43, #237 | observado; coincide com R-002/R-003, R-007, R-008 |
| O-004 | O valor de linha (`CreditAmount`) é verificado, com sensibilidade a arredondamento: *"CreditAmount mal calculado"* | #43, #52 | observado |
| O-005 | Por documento: **soma dos `CreditAmount` ≥ soma dos `DebitAmount`** (versão recente), reportada numa **nota de débito** (`ND`). Numa versão anterior exigia-se **>** estrito, o que rejeitava documentos legítimos de total 0 (anulados); foi reportado como erro do validador. **Atenção:** uma nota de crédito (`NC`) usa `DebitAmount` nas linhas, por isso a regra tem de depender do tipo de documento; o validador não documenta como | #227 (≥), #62 (>) | observado, **varia com a versão e com o tipo; por testar** |
| O-006 | O `GrossTotal` de uma **nota de crédito** não pode exceder o `GrossTotal` do documento a que se refere (`References`). Há vários relatos de **falsos positivos** | #165, #172, #173, #210 | observado, contestado |
| O-007 | Em compras, `DeductibleAmount` é verificado: *"mal calculado"*; deve ser o imposto dedutível em valor monetário | #125, #193, #249 | observado |

### Impostos e isenções

| ID | Observação | Issues | Estado |
|---|---|---|---|
| O-010 | Com `TaxCode = ISE`, `TaxPercentage` tem de ser `0` | #101 | observado; coerente com R-070 e R-091 |
| O-011 | `TaxExemptionReason` tem de ser **exactamente o texto da tabela oficial** do código `M..`, **incluindo acentos** (um produtor falhou ao escrever "Regime transitorio" sem acento em vez de "Regime transitório") | #101, #105, #137, #142, #180 | observado |
| O-012 | Os motivos de isenção só se usam nos regimes Geral e Transitório; para não sujeição (`NS`) os valores são predefinidos | #101 | observado |
| O-013 | Com taxa de IVA 0, `TaxExemptionReason` e `TaxExemptionCode` são obrigatórios (nota acrescentada ao XSD em 2020-09-18) | #92 | observado; coerente com R-091 |
| O-014 | Há documentos que *"não devem conter IVA"*, por exemplo `FT` com certo código de isenção | #108 | observado, causa não documentada |
| O-015 | `TaxCountryRegion` só aceita `AO` no validador, segundo um relato de 2021. **Conflito** com `AO-CAB` (Cabinda) do DE 317/20 | #60 | observado, **por confirmar** |
| O-016 | Em recibos, não há obrigatoriedade de discriminar o regime de impostos, excepto no IVA de caixa | #70 | observado (resposta de utilizador) |

### Clientes e cabeçalho

| ID | Observação | Issues | Estado |
|---|---|---|---|
| O-020 | Em produção, o validador rejeitou ficheiros com **dois `Customer` com o mesmo `CustomerTaxID`** (*"está repetido com o NIF do cliente …"*), o que choca com a prática de criar um cliente por documento a "clientes passantes" | #99, #107, #185 | observado, **contestado**; o XSD não impõe isto |
| O-021 | `SoftwareValidationNumber` tem de **coincidir com o do programa validado** registado na AGT (não basta o formato) | #45, #88, #152 | observado |
| O-022 | O campo `ProductID` é validado (*"Falha na validação do campo ProductID"*); a causa não está documentada | #78, #88, #101, #185, #186, #247 | observado |
| O-023 | O ficheiro tem de estar em **UTF-8**; um ficheiro declarado `iso-8859-1` foi rejeitado | #62 | observado |

### Numeração e assinatura

| ID | Observação | Issues | Estado |
|---|---|---|---|
| O-030 | A numeração de documentos numa série começa em 1 e é contínua e sequencial, sem prefixo no número de ordem | #62 | observado (citação num comentário) |
| O-031 | O formato do `InvoiceNo` é validado pelo portal além do XSD (*"Falha na validação do formato do campo InvoiceNo"*) | #48 | observado |
| O-032 | **Causas reais de "Hash está errado"**: separador decimal vírgula na mensagem em vez de ponto (#78); campos da mensagem não formatados como no esquema (#49); documento anulado de total 0 omitido, que quebra a cadeia (#62); **documento `SourceBilling = I` no meio de uma série `P`** (#195); falhas só a partir do 2.º documento de uma série (#201) | #49, #62, #78, #195, #201, #244 | observado |
| O-033 | Validar o ficheiro **truncado** (só alguns documentos) pode não dar erro de hash mesmo havendo um problema, porque o primeiro documento do ficheiro não é verificado contra o anterior | #195 | observado |

### Listas de valores

| ID | Observação | Issues | Estado |
|---|---|---|---|
| O-040 | Em 2021 o validador **rejeitou `GC` (guia de consignação)** tanto em `WorkingDocuments` como em `MovementOfGoods`; as listas permitidas eram `WorkType` (CM, CC, GR, NR, FO, NE, OU, OR, PP, DC, RP, RE, CS, LD, RA) e `MovementType` (GR, GT, GA, GD). O DE 317/20 (dezembro de 2020) lista `GC` em `WorkType`; verificar a versão actual | #158, #111 | observado, **varia com a versão** |
| O-041 | `WithholdingTaxType` só aceita IVA, IRT, II, IPU, IS, IAC, OU | #188 | observado; coerente com o XSD |
| O-042 | `InvoiceType = RE` (recibo) só se usa no sector segurador quando não se usa `WorkingDocuments`; os restantes usam `FR` para pronto-pagamento | #91 | observado (resposta de utilizador) |

### Outras

| ID | Observação | Issues | Estado |
|---|---|---|---|
| O-050 | Segundo um relato, vendas dos tipos `FT`, `VD`, `GF`, `FG` e `TV` (citação: `VD` não consta do XSD) devem dar lugar a um recibo `RC` em `Payments`; uma `FR` serve de recibo e não o exige | #91 | observado (citação), **por confirmar** |
| O-051 | A FAQ n.º 56 da AGT, citada num issue, define uma tag `CUD` a preencher com `0` até nova definição; não consta do XSD 1.01_01 | #8 | observado |
| O-052 | O erro `E04` (*numberOfEntries vs documents*) reportado em 2025 é da **API de facturação electrónica**, não do SAF-T | #261 | fora do âmbito |

## Validadores de terceiros: o que afirmam verificar

O [saft.ao](https://saft.ao) é um validador **gratuito e independente** (sem afiliação à AGT), mantido pela equipa do KwanzaGest e operado pela GloboSoft. Aceita ficheiros até 20 MB. O que **afirma** verificar, em seis módulos *(informação do próprio site, não confirmada por nós; não conseguimos testá-lo, porque exige confirmação anti-robô)*:

1. **Estrutura:** conformidade com o esquema oficial da AGT 1.01.
2. **Cabeçalho:** dados da empresa, NIF do contribuinte e período fiscal.
3. **Entidades:** clientes, fornecedores e produtos referenciados no ficheiro.
4. **Impostos:** taxas, isenções e motivos de isenção.
5. **Documentos:** numeração sequencial, datas e hashes.
6. **Totais:** coerência entre linhas, impostos e totais.

Distingue **erros** (bloqueiam a submissão) de **avisos** (campos incompletos ou incoerentes, que não bloqueiam mas convém corrigir). As seis categorias coincidem com as observações O-001 a O-050, o que reforça que a validação prática vai além do esquema. **A distinção erro/aviso é útil para as bibliotecas**: as verificações do modo estrito devem poder sair como *avisos* e não como erros.

Privacidade (política do site, não verificada por nós): o ficheiro é processado em memória e não é gravado em disco nem em base de dados; os servidores estão em Portugal (transferência fora de Angola, que a política enquadra nos artigos 33.º e 34.º da Lei n.º 22/11); o site usa Cloudflare Turnstile (confirmação anti-robô), Sentry (gravação de sessão com texto mascarado, sem enviar o conteúdo do SAF-T) e Google Analytics. Ver também `conformance/oracle/README.md`.

## Resultados de testes em validadores externos

Registo dos testes feitos com o pacote `conformance/oracle/`. Cada resultado é do validador indicado, **não** da AGT, salvo indicação.

| Observação | Validador | Data | Resultado |
|---|---|---|---|
| O-001 (`TaxPayable` errado) | saft.ao | 2026-10-12 | **não reproduzida**: aceitou o ficheiro sem mensagens |
| O-002 (desconto/`UnitPrice`) | saft.ao | 2026-10-12 | **não reproduzida**: aceitou os dois ficheiros |

O saft.ao **não** verifica estes cálculos, por isso não serve de oráculo para a família O-001 a O-004. Detalhes em `conformance/oracle/results/saft.ao-2026-10-12.md`. As restantes observações continuam por testar. Para a AGT, o único teste fiável é o validador de produtores do portal.

## Como as bibliotecas devem usar isto

1. **Modo estrito (opcional).** Além das regras `R-nnn`, a biblioteca oferece um modo que aplica as observações marcadas "observado" **sem contestação**: O-001 a O-004, O-007, O-010, O-011, O-013, O-023, O-032 (O-005 só depois de testada por tipo de documento). Por defeito desligado, porque a fonte não é oficial e o validador varia. Os problemas do modo estrito saem com severidade **aviso**, não erro.
2. **Nunca rejeitar por observações contestadas** (O-006, O-020, O-015) sem opção explícita.
3. **Cada observação precisa de um caso de teste** antes de passar a regra. O melhor teste é submeter ficheiros sintéticos ao próprio validador da AGT, por quem tenha acesso e **só ao validador, nunca à entrega**; ver o plano na conversa do projecto.
4. As observações **não** substituem a spec: a lei e o XSD prevalecem.
