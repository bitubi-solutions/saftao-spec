#!/usr/bin/env python3
"""Gera o pacote de ficheiros SINTÉTICOS de conformance/oracle/ para testes manuais em validadores externos.
Cada ficheiro isola uma observação de spec/06-validator-observations.md. Depois de gerar, confirma-se que
todos passam (ou não) o XSD, para que um erro do validador externo possa ser atribuído a regras além do esquema.

Uso: python3 tools/make_oracle_pack.py conformance/oracle
"""
import json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_sales_sample import build

M10 = ("M10", "Isento nos termos da alínea a) do nº1 do artigo 12.º do CIVA")
M10_SEM_ACENTOS = ("M10", "Isento nos termos da alinea a) do n1 do artigo 12. do CIVA")

# controlos que DEVEM falhar em qualquer validador de esquema (post = alteração ao texto do XML)
CONTROLS = [
 ("C-01-controlo-moeda-invalida", lambda x: x.replace("<CurrencyCode>AOA<", "<CurrencyCode>EUR<", 1), "CONTROLO: CurrencyCode EUR (o XSD só admite AOA ou USD).", "Tem de falhar: viola o XSD."),
 ("C-02-controlo-campo-em-falta", lambda x: x.replace("<CompanyName>Empresa de Teste Sintetico</CompanyName>", "", 1), "CONTROLO: Header sem CompanyName (obrigatório).", "Tem de falhar: viola o XSD."),
 ("C-04-controlo-customerid-duplicado", lambda x: re.sub(r"(<Customer>.*?</Customer>)", r"\1\1", x, count=1, flags=re.S), "CONTROLO: dois Customer com o mesmo CustomerID (xs:unique do XSD).", "Tem de falhar num validador que aplique as restrições de identidade do XSD."),
 ("C-05-controlo-customerid-inexistente", lambda x: x.replace("<CustomerID>CF</CustomerID><Line>", "<CustomerID>XX</CustomerID><Line>", 1), "CONTROLO: factura com CustomerID que não existe em Customer (xs:keyref do XSD).", "Tem de falhar num validador que aplique as restrições de identidade do XSD."),
 ("C-06-controlo-invoiceno-duplicado", lambda x: x.replace("<InvoiceNo>FT 2026A/2</InvoiceNo>", "<InvoiceNo>FT 2026A/1</InvoiceNo>", 1), "CONTROLO: dois documentos com o mesmo InvoiceNo (xs:unique do XSD).", "Tem de falhar num validador que aplique as restrições de identidade do XSD."),
 ("C-03-controlo-formato-monetario", lambda x: x.replace("<TaxPayable>28.00<", "<TaxPayable>28.0<", 1), "CONTROLO: TaxPayable com uma casa decimal (o XSD exige duas).", "Tem de falhar: viola o XSD."),
]

CASES = [
 ("00-base", None, "Base: 2 facturas FT e 1 nota de crédito NC (com DebitAmount), IVA 14%, assinadas com a chave de teste, software 999/AGT/2026.", "Nada de errado no ficheiro. Anotar se o site reclama do número de software ou do hash (pode não conhecer a chave)."),
 ("00b-base-nao-validado", dict(validated=False), "Base com software '0' e Hash '0' (programa não validado).", "Nada de errado."),
 ("O-001-taxpayable-errado", dict(tax_payable_delta="1.00"), "TaxPayable da FT 2026A/1 aumentado em 1,00.", "O-001: esperado erro de cálculo de TaxPayable."),
 ("O-001b-gross-incoerente", dict(ft1_gross_override="999.00"), "FT 2026A/1 com GrossTotal 999,00 (NetTotal 200,00 + TaxPayable 28,00 = 228,00).", "O-001: erro gritante de coerência de totais; se nem este falha, o site não verifica totais."),
 ("O-001c-net-diferente-das-linhas", dict(ft1_net_override="1.00"), "FT 2026A/1 com NetTotal 1,00 (a linha vale 200,00).", "O-001: idem."),
 ("O-002a-desconto-deduzido", dict(discount="20.00"), "FT 2026A/1 com desconto de 20,00 já deduzido em UnitPrice e CreditAmount.", "O-002: esperado válido."),
 ("O-002b-desconto-nao-deduzido-no-preco", dict(discount="20.00", discount_unit_not_deducted=True), "Como o anterior, mas UnitPrice sem deduzir o desconto.", "O-002: esperado erro (UnitPrice/CreditAmount)."),
 ("O-003-totalcredit-errado", dict(total_credit_delta="1.00"), "TotalCredit da secção aumentado em 1,00.", "O-003: esperado erro de TotalCredit."),
 ("O-005b-factura-com-debito", dict(ft_side="D"), "As FT usam DebitAmount em vez de CreditAmount.", "O-005: esperado erro (crédito < débito) nas FT; a NC com DebitAmount na base é o contraponto."),
 ("O-006-nc-maior-que-origem", dict(nc_debit="300.00"), "NC com GrossTotal (342,00) maior que o da FT referida (228,00).", "O-006: esperado erro 'GrossTotal é maior que o documento de origem'."),
 ("O-010-ise-com-percentagem", dict(line_tax_code="ISE", line_tax_pct="14.00", exemption=M10), "TaxCode ISE com TaxPercentage 14,00.", "O-010: esperado erro (ISE exige percentagem 0)."),
 ("O-011a-isencao-texto-exacto", dict(line_tax_code="ISE", line_tax_pct="0.00", exemption=M10), "ISE, percentagem 0, M10 com o texto exacto da tabela oficial.", "O-011: esperado válido."),
 ("O-011b-isencao-sem-acentos", dict(line_tax_code="ISE", line_tax_pct="0.00", exemption=M10_SEM_ACENTOS), "O mesmo, com o texto do motivo sem acentos.", "O-011: esperado 'TaxExemptionReason mal preenchido'."),
 ("O-015-regiao-cabinda", dict(tax_region="AO-CAB"), "TaxCountryRegion AO-CAB (Cabinda) na tabela e nas linhas.", "O-015: ver se o validador aceita AO-CAB."),
 ("O-020-nif-duplicado", dict(customers=[("CF", "999999999", "Consumidor final"), ("C2", "1234567890", "Cliente A"), ("C3", "1234567890", "Cliente B")]), "Dois clientes com o mesmo CustomerTaxID (os documentos usam só CF).", "O-020: ver se rejeita NIF repetido."),
 ("O-032-hash-adulterado", dict(tamper_hash=True), "Hash da FT 2026A/2 alterado nos últimos 4 caracteres.", "O-032: esperado 'Hash está errado' (se o validador verificar a cadeia)."),
 ("O-030-numeracao-com-salto", dict(ft2_no="FT 2026A/3"), "Série FT 2026A com numeração 1 e 3 (falta o 2).", "O-030: ver se o validador exige numeração contínua."),
 ("R-013-nc-sem-references", dict(nc_refs=False), "NC sem References.", "Em vendas, References é obrigatório em NC (DE 317/20 4.1.4.19.10)."),
]

if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    xsd = os.path.join(here, "..", "schema", "SAFTAO1.01_01.xsd")
    rows = []
    for name, opt, what, expect in CASES:
        path = os.path.join(out, name + ".xml")
        open(path, "w", encoding="utf-8").write(build(opt))
        r = json.loads(subprocess.run([sys.executable, os.path.join(here, "validate.py"), xsd, path], capture_output=True, text=True).stdout)
        rows.append((name, what, expect, r["valid"], (r["errors"][:1] or [{}])[0].get("message", "")))
    for name, post, what, expect in CONTROLS:
        path = os.path.join(out, name + ".xml")
        open(path, "w", encoding="utf-8").write(post(build(None)))
        r = json.loads(subprocess.run([sys.executable, os.path.join(here, "validate.py"), xsd, path], capture_output=True, text=True).stdout)
        assert not r["valid"], name + " devia violar o XSD"
        rows.append((name, what, expect, r["valid"], (r["errors"][:1] or [{}])[0].get("message", "")))
    # latin-1
    lat = build(None).replace("Empresa de Teste Sintetico", "Empresa de Teste Sintético").replace('encoding="UTF-8"', 'encoding="ISO-8859-1"')
    open(os.path.join(out, "O-023-encoding-latin1.xml"), "wb").write(lat.encode("latin-1"))
    rows.append(("O-023-encoding-latin1", "Declarado e codificado em ISO-8859-1, com 'é' no nome da empresa.", "O-023: esperado erro de encoding.", True, ""))
    json.dump([dict(file=r[0] + ".xml", what=r[1], expect=r[2], xsd_valid=r[3], xsd_error=r[4]) for r in rows],
              open(os.path.join(out, "pack.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    for r in rows:
        print(("XSD OK  " if r[3] else "XSD ERRO"), r[0], r[4][:100])

    # folha de resultados pré-preenchida
    lines = ["# Resultados: <validador> — AAAA-MM-DD", "", "Validador: ______  (versão/data)", "Quem submeteu: ______", "",
             "| Ficheiro | O que testa | Esperado (hipótese) | Resultado (ok / aviso / erro) | Mensagem exacta |", "|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r[0]}.xml | {r[1]} | {r[2]} | | |")
    open(os.path.join(out, "results", "TEMPLATE.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
