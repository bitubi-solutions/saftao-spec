# Resultados: saft.ao — 2026-10-12

Validador: [saft.ao](https://saft.ao) (independente, mantido pela equipa do KwanzaGest; **não** é a AGT).
Quem submeteu: o autor do projecto, à mão, no browser (três pedidos de 5 ficheiros cada).
Origem dos dados: resposta JSON do site, colada pelo autor. O pedido incluía um token Cloudflare Turnstile de uso único, que **não** se guarda.

| Ficheiro | O que testa | Esperado (hipótese) | Resultado | Mensagens | `totalInvoiced` |
|---|---|---|---|---|---|
| 00-base.xml | Base: 2 FT e 1 NC | sem erros | **ok** ("Valid") | nenhuma | 399.00 |
| 00b-base-nao-validado.xml | Software `0`, Hash `0` | sem erros | **ok** | nenhuma | 399.00 |
| O-001-taxpayable-errado.xml | `TaxPayable` da FT 1 = 29.00 em vez de 28.00 | erro de cálculo | **ok** ("Valid") | nenhuma | 399.00 |
| O-002a-desconto-deduzido.xml | Desconto já deduzido | sem erros | **ok** | nenhuma | 376.20 |
| O-002b-desconto-nao-deduzido-no-preco.xml | `UnitPrice` sem deduzir o desconto | erro | **ok** ("Valid") | nenhuma | 376.20 |

| O-003-totalcredit-errado.xml | `TotalCredit` da secção = 251.00 em vez de 250.00 | erro de total | **ok** | nenhuma | 399.00 |
| O-005b-factura-com-debito.xml | FT com `DebitAmount` em vez de `CreditAmount` | erro | **ok** | nenhuma | 399.00 |
| O-006-nc-maior-que-origem.xml | NC de 342,00 sobre FT de 228,00 | erro | **ok** | nenhuma | 627.00 |
| O-010-ise-com-percentagem.xml | `ISE` com `TaxPercentage` 14,00 | erro | **ok** | nenhuma | 399.00 |
| O-011a-isencao-texto-exacto.xml | `ISE`, 0%, M10 com texto exacto | sem erros | **ok** | nenhuma | 350.00 |
| O-015-regiao-cabinda.xml | `TaxCountryRegion` `AO-CAB` | ver se aceita | **ok** | nenhuma | 399.00 |
| O-020-nif-duplicado.xml | 2 clientes com o mesmo `CustomerTaxID` | erro (O-020) | **ok** (`customers`: 3) | nenhuma | 399.00 |
| O-023-encoding-latin1.xml | declarado e codificado em ISO-8859-1 | erro de encoding | **ok**, mas `companyName` devolvido como `Sint�tico` | nenhuma | 399.00 |
| O-030-numeracao-com-salto.xml | FT 1 e FT 3 (falta a 2) | erro de numeração | **ok** | nenhuma | 399.00 |
| O-032-hash-adulterado.xml | Hash da FT 2 adulterado | "Hash está errado" | **ok** | nenhuma | 399.00 |

Totais devolvidos: `documents` 3, `customers` 1, `products` 1, `currencyCode` AOA.

## Interpretação

1. **O saft.ao não reproduz O-001 nem O-002.** Aceitou um `TaxPayable` errado em 1,00 e um `UnitPrice` incoerente com o `CreditAmount`. Isto **não** desmente os relatos sobre o validador da AGT: mostra que o saft.ao **não** verifica estes cálculos. O validador da AGT continua por testar.
2. **Sem avisos** em nenhum ficheiro, apesar de o número de software `999/AGT/2026` ser inventado e de os hashes estarem assinados com uma chave que o site não conhece. Logo, o saft.ao não valida o número de software contra a lista da AGT, e não rejeita hashes de chave desconhecida.
3. **`totalInvoiced` soma as notas de crédito com sinal positivo** (228,00 + 57,00 + 114,00 = 399,00; o valor líquido seria 171,00). É uma convenção ou um defeito do site; não afecta a spec.
4. O saft.ao devolve **estado** (`Valid`), **resumo**, **mensagens** e **totais**; não indicou qualquer nível de severidade além disso nestes ficheiros.

## Conclusão provisória (15 ficheiros)

O saft.ao aceitou **todos** os 15 ficheiros, incluindo hash adulterado, numeração com salto, NIF de cliente duplicado e erros de cálculo. Os ficheiros não estão "mal feitos": cada mutação é válida no XSD por desenho.

Um pormenor importante: no ficheiro Latin-1, o site devolveu o nome da empresa como `Sint�tico`. Um parser XML que respeitasse a declaração `encoding="ISO-8859-1"` leria "Sintético". O site leu os bytes como UTF-8 e aceitou o ficheiro sem queixa. Isto sugere que o saft.ao **não usa um parser XML padrão sobre o ficheiro original** (ou ignora a declaração), e portanto **não é prova de que valida o esquema**. Falta o teste decisivo: os controlos `C-01` a `C-03`, que violam o XSD de propósito.

## Por submeter

- **Decisivo:** C-01, C-02, C-03 (controlos que violam o XSD) e O-001b, O-001c (totais gritantes).
- **Pouco provável de revelar algo:** O-011b e R-013.
