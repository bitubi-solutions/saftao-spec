# Resultados: saft.ao — 2026-10-12

Validador: [saft.ao](https://saft.ao) (independente, mantido pela equipa do KwanzaGest; **não** é a AGT).
Quem submeteu: o autor do projecto, à mão, no browser (quatro pedidos de 5 ficheiros cada).
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
| C-01-controlo-moeda-invalida.xml | CONTROLO: `CurrencyCode` EUR | tem de falhar | **erro** | "Erro na linha 1: O elemento CurrencyCode é inválido. O valor 'EUR' é incompatível com o seu tipo de dados ('String') - O valor não está dentro da lista de possibilidades." | 399.00 |
| C-02-controlo-campo-em-falta.xml | CONTROLO: sem `CompanyName` | tem de falhar | **erro** | "Erro na linha 1: The element 'Header' in namespace 'urn:OECD:StandardAuditFile-Tax:AO_1.01_01' has invalid child element 'CompanyAddress' … List of possible elements expected: 'CompanyName' …" | 399.00 |
| C-03-controlo-formato-monetario.xml | CONTROLO: `TaxPayable` 28.0 | tem de falhar | **erro** | "Erro na linha 1: O elemento TaxPayable é inválido. O valor '28.0' é incompatível com o seu tipo de dados ('SAFMonetaryType2DecimalPlaces') - O valor não está dentro da lista de possibilidades." | 399.00 |
| O-001b-gross-incoerente.xml | `GrossTotal` 999,00 com Net 200 + imposto 28 | erro de totais | **ok** | nenhuma | 1170.00 |
| O-001c-net-diferente-das-linhas.xml | `NetTotal` 1,00 com linha de 200 | erro de totais | **ok** | nenhuma | 399.00 |

Totais devolvidos: `documents` 3, `customers` 1, `products` 1, `currencyCode` AOA.

## Interpretação

1. **O saft.ao não reproduz O-001 nem O-002.** Aceitou um `TaxPayable` errado em 1,00 e um `UnitPrice` incoerente com o `CreditAmount`. Isto **não** desmente os relatos sobre o validador da AGT: mostra que o saft.ao **não** verifica estes cálculos. O validador da AGT continua por testar.
2. **Sem avisos** em nenhum ficheiro, apesar de o número de software `999/AGT/2026` ser inventado e de os hashes estarem assinados com uma chave que o site não conhece. Logo, o saft.ao não valida o número de software contra a lista da AGT, e não rejeita hashes de chave desconhecida.
3. **`totalInvoiced` soma as notas de crédito com sinal positivo** (228,00 + 57,00 + 114,00 = 399,00; o valor líquido seria 171,00). É uma convenção ou um defeito do site; não afecta a spec.
4. O saft.ao devolve **estado** (`Valid`), **resumo**, **mensagens** e **totais**; não indicou qualquer nível de severidade além disso nestes ficheiros.

## Conclusão (20 ficheiros)

**O saft.ao valida o esquema XSD, e só isso.** Rejeitou os 3 controlos que violam o XSD (moeda inválida, campo obrigatório em falta, formato monetário), e aceitou **todos os 17 ficheiros** que passam o XSD, incluindo hash adulterado, numeração com salto, `TaxPayable` e `GrossTotal` incoerentes, nota de crédito acima do original, NIF de cliente duplicado e uma isenção com taxa de 14%.

Pormenores:
- As mensagens de erro identificam o elemento e o tipo do XSD (por exemplo `SAFMonetaryType2DecimalPlaces`) e vêm em português ou em inglês, consoante o tipo de erro; o texto inglês parece ser do motor de validação XML do .NET. O número da linha foi sempre `1`, porque os ficheiros do pacote estão numa só linha.
- O ficheiro Latin-1 foi aceite, com o nome devolvido como `Sint�tico`: o site lê os bytes como UTF-8, mas valida o esquema.
- `totalInvoiced` soma as notas de crédito com sinal positivo.
- Apesar de os módulos "Documentos" (numeração, datas, hashes) e "Totais" (coerência) do site sugerirem mais, **não observámos nenhuma verificação além do esquema**.

**Consequência:** passar no saft.ao prova só conformidade com o XSD. **Não** prova que o ficheiro passa o validador da AGT. As observações O-001 a O-050 ficam **sem confirmação** por este canal; só o validador de produtores do portal da AGT as pode confirmar.

## Por submeter (opcional)

Novos controlos, para saber se o saft.ao aplica também as restrições de identidade do XSD (`xs:unique`, `xs:keyref`): **C-04** (CustomerID duplicado), **C-05** (CustomerID inexistente) e **C-06** (InvoiceNo duplicado). Servem para caracterizar o saft.ao, não para as regras da AGT. Os restantes (O-011b, R-013) têm pouca probabilidade de revelar algo.
