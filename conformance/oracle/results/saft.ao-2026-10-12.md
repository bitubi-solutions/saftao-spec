# Resultados: saft.ao — 2026-10-12

Validador: [saft.ao](https://saft.ao) (independente, mantido pela equipa do KwanzaGest; **não** é a AGT).
Quem submeteu: o autor do projecto, à mão, no browser (um pedido com 5 ficheiros).
Origem dos dados: resposta JSON do site, colada pelo autor. O pedido incluía um token Cloudflare Turnstile de uso único, que **não** se guarda.

| Ficheiro | O que testa | Esperado (hipótese) | Resultado | Mensagens | `totalInvoiced` |
|---|---|---|---|---|---|
| 00-base.xml | Base: 2 FT e 1 NC | sem erros | **ok** ("Valid") | nenhuma | 399.00 |
| 00b-base-nao-validado.xml | Software `0`, Hash `0` | sem erros | **ok** | nenhuma | 399.00 |
| O-001-taxpayable-errado.xml | `TaxPayable` da FT 1 = 29.00 em vez de 28.00 | erro de cálculo | **ok** ("Valid") | nenhuma | 399.00 |
| O-002a-desconto-deduzido.xml | Desconto já deduzido | sem erros | **ok** | nenhuma | 376.20 |
| O-002b-desconto-nao-deduzido-no-preco.xml | `UnitPrice` sem deduzir o desconto | erro | **ok** ("Valid") | nenhuma | 376.20 |

Totais devolvidos: `documents` 3, `customers` 1, `products` 1, `currencyCode` AOA.

## Interpretação

1. **O saft.ao não reproduz O-001 nem O-002.** Aceitou um `TaxPayable` errado em 1,00 e um `UnitPrice` incoerente com o `CreditAmount`. Isto **não** desmente os relatos sobre o validador da AGT: mostra que o saft.ao **não** verifica estes cálculos. O validador da AGT continua por testar.
2. **Sem avisos** em nenhum ficheiro, apesar de o número de software `999/AGT/2026` ser inventado e de os hashes estarem assinados com uma chave que o site não conhece. Logo, o saft.ao não valida o número de software contra a lista da AGT, e não rejeita hashes de chave desconhecida.
3. **`totalInvoiced` soma as notas de crédito com sinal positivo** (228,00 + 57,00 + 114,00 = 399,00; o valor líquido seria 171,00). É uma convenção ou um defeito do site; não afecta a spec.
4. O saft.ao devolve **estado** (`Valid`), **resumo**, **mensagens** e **totais**; não indicou qualquer nível de severidade além disso nestes ficheiros.

## Por submeter (12 ficheiros)

O-003, O-005b, O-006, O-010, O-011a, O-011b, O-015, O-020, O-023, O-030, O-032 e R-013. Prioridade, pelo que o saft.ao diz verificar (numeração, hashes, isenções, entidades): **O-032, O-030, O-011b, O-010, O-020, R-013**.
