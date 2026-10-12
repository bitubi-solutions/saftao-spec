# Resultados: <validador> — AAAA-MM-DD

Validador: ______  (versão/data)
Quem submeteu: ______

| Ficheiro | O que testa | Esperado (hipótese) | Resultado (ok / aviso / erro) | Mensagem exacta |
|---|---|---|---|---|
| 00-base.xml | Base: 2 facturas FT e 1 nota de crédito NC (com DebitAmount), IVA 14%, assinadas com a chave de teste, software 999/AGT/2026. | Nada de errado no ficheiro. Anotar se o site reclama do número de software ou do hash (pode não conhecer a chave). | | |
| 00b-base-nao-validado.xml | Base com software '0' e Hash '0' (programa não validado). | Nada de errado. | | |
| O-001-taxpayable-errado.xml | TaxPayable da FT 2026A/1 aumentado em 1,00. | O-001: esperado erro de cálculo de TaxPayable. | | |
| O-001b-gross-incoerente.xml | FT 2026A/1 com GrossTotal 999,00 (NetTotal 200,00 + TaxPayable 28,00 = 228,00). | O-001: erro gritante de coerência de totais; se nem este falha, o site não verifica totais. | | |
| O-001c-net-diferente-das-linhas.xml | FT 2026A/1 com NetTotal 1,00 (a linha vale 200,00). | O-001: idem. | | |
| O-002a-desconto-deduzido.xml | FT 2026A/1 com desconto de 20,00 já deduzido em UnitPrice e CreditAmount. | O-002: esperado válido. | | |
| O-002b-desconto-nao-deduzido-no-preco.xml | Como o anterior, mas UnitPrice sem deduzir o desconto. | O-002: esperado erro (UnitPrice/CreditAmount). | | |
| O-003-totalcredit-errado.xml | TotalCredit da secção aumentado em 1,00. | O-003: esperado erro de TotalCredit. | | |
| O-005b-factura-com-debito.xml | As FT usam DebitAmount em vez de CreditAmount. | O-005: esperado erro (crédito < débito) nas FT; a NC com DebitAmount na base é o contraponto. | | |
| O-006-nc-maior-que-origem.xml | NC com GrossTotal (342,00) maior que o da FT referida (228,00). | O-006: esperado erro 'GrossTotal é maior que o documento de origem'. | | |
| O-010-ise-com-percentagem.xml | TaxCode ISE com TaxPercentage 14,00. | O-010: esperado erro (ISE exige percentagem 0). | | |
| O-011a-isencao-texto-exacto.xml | ISE, percentagem 0, M10 com o texto exacto da tabela oficial. | O-011: esperado válido. | | |
| O-011b-isencao-sem-acentos.xml | O mesmo, com o texto do motivo sem acentos. | O-011: esperado 'TaxExemptionReason mal preenchido'. | | |
| O-015-regiao-cabinda.xml | TaxCountryRegion AO-CAB (Cabinda) na tabela e nas linhas. | O-015: ver se o validador aceita AO-CAB. | | |
| O-020-nif-duplicado.xml | Dois clientes com o mesmo CustomerTaxID (os documentos usam só CF). | O-020: ver se rejeita NIF repetido. | | |
| O-032-hash-adulterado.xml | Hash da FT 2026A/2 alterado nos últimos 4 caracteres. | O-032: esperado 'Hash está errado' (se o validador verificar a cadeia). | | |
| O-030-numeracao-com-salto.xml | Série FT 2026A com numeração 1 e 3 (falta o 2). | O-030: ver se o validador exige numeração contínua. | | |
| R-013-nc-sem-references.xml | NC sem References. | Em vendas, References é obrigatório em NC (DE 317/20 4.1.4.19.10). | | |
| C-01-controlo-moeda-invalida.xml | CONTROLO: CurrencyCode EUR (o XSD só admite AOA ou USD). | Tem de falhar: viola o XSD. | | |
| C-02-controlo-campo-em-falta.xml | CONTROLO: Header sem CompanyName (obrigatório). | Tem de falhar: viola o XSD. | | |
| C-04-controlo-customerid-duplicado.xml | CONTROLO: dois Customer com o mesmo CustomerID (xs:unique do XSD). | Tem de falhar num validador que aplique as restrições de identidade do XSD. | | |
| C-05-controlo-customerid-inexistente.xml | CONTROLO: factura com CustomerID que não existe em Customer (xs:keyref do XSD). | Tem de falhar num validador que aplique as restrições de identidade do XSD. | | |
| C-06-controlo-invoiceno-duplicado.xml | CONTROLO: dois documentos com o mesmo InvoiceNo (xs:unique do XSD). | Tem de falhar num validador que aplique as restrições de identidade do XSD. | | |
| C-03-controlo-formato-monetario.xml | CONTROLO: TaxPayable com uma casa decimal (o XSD exige duas). | Tem de falhar: viola o XSD. | | |
| O-023-encoding-latin1.xml | Declarado e codificado em ISO-8859-1, com 'é' no nome da empresa. | O-023: esperado erro de encoding. | | |
