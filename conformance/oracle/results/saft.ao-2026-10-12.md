# Resultados: saft.ao — 2026-10-12

Validador: [saft.ao](https://saft.ao) (independente, mantido pela equipa do KwanzaGest; **não** é a AGT).
Quem submeteu: o autor do projecto, à mão, no browser (dois pedidos de 5 ficheiros cada).
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

Totais devolvidos: `documents` 3, `customers` 1, `products` 1, `currencyCode` AOA.

## Interpretação

1. **O saft.ao não reproduz O-001 nem O-002.** Aceitou um `TaxPayable` errado em 1,00 e um `UnitPrice` incoerente com o `CreditAmount`. Isto **não** desmente os relatos sobre o validador da AGT: mostra que o saft.ao **não** verifica estes cálculos. O validador da AGT continua por testar.
2. **Sem avisos** em nenhum ficheiro, apesar de o número de software `999/AGT/2026` ser inventado e de os hashes estarem assinados com uma chave que o site não conhece. Logo, o saft.ao não valida o número de software contra a lista da AGT, e não rejeita hashes de chave desconhecida.
3. **`totalInvoiced` soma as notas de crédito com sinal positivo** (228,00 + 57,00 + 114,00 = 399,00; o valor líquido seria 171,00). É uma convenção ou um defeito do site; não afecta a spec.
4. O saft.ao devolve **estado** (`Valid`), **resumo**, **mensagens** e **totais**; não indicou qualquer nível de severidade além disso nestes ficheiros.

## Conclusão provisória (10 ficheiros)

O saft.ao aceitou **todos** os 10 ficheiros, incluindo erros de cálculo, de totais de secção, de notas de crédito acima do original e uma isenção com taxa de 14%. Os ficheiros não estão "mal feitos": cada mutação é válida no XSD por desenho. A hipótese mais simples é que o saft.ao **valida apenas o esquema** (e talvez o cabeçalho), apesar de os seus módulos "Documentos" e "Totais" sugerirem mais. Para o confirmar, o pacote ganhou **controlos** que violam o XSD (C-01 a C-03) e variantes mais gritantes de erros de totais (O-001b, O-001c).

## Por submeter

- **Controlos e totais gritantes (1.º lote):** C-01, C-02, C-03, O-001b, O-001c.
- **2.º lote:** O-032 (hash), O-030 (numeração), O-011b (acentos), O-020 (NIF duplicado), R-013 (NC sem `References`).
- **Provavelmente sem interesse** se o saft.ao só valida o esquema: O-015, O-023.
