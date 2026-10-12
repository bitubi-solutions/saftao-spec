#!/usr/bin/env python3
"""Gera ficheiros SAF-T (AO) de vendas SINTÉTICOS (dados inventados) para a conformance e para testes manuais
em validadores externos. Assina os documentos com a chave de TESTE de conformance/signature/signing-chain.json.

Uso: python3 tools/make_sales_sample.py DIRETORIO
Requer: cryptography (apenas para assinar). Nenhum dado real; o NIF do emitente é o público do exemplo da AGT.
"""
import base64, json, os, sys
from decimal import Decimal, ROUND_HALF_UP
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

HERE = os.path.dirname(os.path.abspath(__file__))
KEY = json.load(open(os.path.join(HERE, "..", "conformance", "signature", "signing-chain.json"), encoding="utf-8"))["testPrivateKeyPem"]
PRIV = serialization.load_pem_private_key(KEY.encode(), None)

def q(x):
    return Decimal(x).quantize(Decimal("0.01"), ROUND_HALF_UP)

def sign(msg):
    return base64.b64encode(PRIV.sign(msg.encode(), padding.PKCS1v15(), hashes.SHA1())).decode()

NS = "urn:OECD:StandardAuditFile-Tax:AO_1.01_01"

def build(opt=None):
    """opt: dicionário de variações (ver os nomes abaixo)."""
    o = dict(validated=True, tax_payable_delta="0", discount=None, nc_debit="100.00", total_credit_delta="0",
             nc_gross_override=None, tamper_hash=False, discount_unit_not_deducted=False, ft_side="C", ft2_no="FT 2026A/2", ft1_gross_override=None, ft1_net_override=None, line_tax_pct="14.00", line_tax_code="NOR",
             exemption=None, customers=None, tax_region="AO", nc_refs=True, software_no=None)
    o.update(opt or {})
    soft = o["software_no"] or ("999/AGT/2026" if o["validated"] else "0")
    hash_ctl = "1" if o["validated"] else "0"

    # documentos: (série, tipo, nº, data, hora, [linhas])  linha: (qtd, preço unitário, 'C'|'D')
    docs = [("FT", "FT 2026A/1", "2026-05-10", "2026-05-10T10:00:00", [("2", "100.00", o["ft_side"])]),
            ("FT", o["ft2_no"], "2026-05-11", "2026-05-11T11:30:00", [("1", "50.00", o["ft_side"])]),
            ("NC", "NC 2026A/1", "2026-05-12", "2026-05-12T09:15:00", [("1", o["nc_debit"], "D")])]
    prev = {}
    body, tot_c, tot_d = [], Decimal(0), Decimal(0)
    gross_by_no = {}
    for typ, no, d, dt, lines in docs:
        pct = Decimal(o["line_tax_pct"])
        net = Decimal(0); tax = Decimal(0); xml_lines = []
        for i, (qty, price, side) in enumerate(lines, 1):
            unit = Decimal(price)
            amount = q(Decimal(qty) * unit)
            disc = Decimal(o["discount"]) if (o["discount"] and typ == "FT" and no.endswith("/1")) else Decimal(0)
            if disc:                     # desconto já deduzido no valor da linha (O-002)
                amount = amount - disc
                unit = unit if o["discount_unit_not_deducted"] else q(amount / Decimal(qty))
            net += amount; tax += q(amount * pct / 100)
            amt_tag = "CreditAmount" if side == "C" else "DebitAmount"
            ref = ""
            if typ == "NC" and o["nc_refs"]:
                ref = "<References><Reference>FT 2026A/1</Reference><Reason>Devolução</Reason></References>"
            exm = ""
            if o["exemption"]:
                exm = f"<TaxExemptionReason>{o['exemption'][1]}</TaxExemptionReason><TaxExemptionCode>{o['exemption'][0]}</TaxExemptionCode>"
            else:
                exm = ""
            settle = f"<SettlementAmount>{q(disc)}</SettlementAmount>" if disc else ""
            xml_lines.append(
                f"<Line><LineNumber>{i}</LineNumber><ProductCode>P001</ProductCode><ProductDescription>Produto de teste</ProductDescription>"
                f"<Quantity>{qty}</Quantity><UnitOfMeasure>UN</UnitOfMeasure><UnitPrice>{unit}</UnitPrice><TaxPointDate>{d}</TaxPointDate>"
                f"{ref}<Description>Produto de teste</Description><{amt_tag}>{amount}</{amt_tag}>"
                f"<Tax><TaxType>IVA</TaxType><TaxCountryRegion>{o['tax_region']}</TaxCountryRegion><TaxCode>{o['line_tax_code']}</TaxCode><TaxPercentage>{pct}</TaxPercentage></Tax>"
                f"{exm}{settle}</Line>")
            if side == "C": tot_c += amount
            else: tot_d += amount
        tax_payable = q(tax + Decimal(o["tax_payable_delta"]) if typ == "FT" and no.endswith("/1") else tax)
        gross = q(net + tax)
        if typ == "NC" and o["nc_gross_override"]: gross = q(Decimal(o["nc_gross_override"]))
        net_out = q(net)
        if typ == "FT" and no.endswith("/1"):
            if o["ft1_gross_override"]: gross = q(Decimal(o["ft1_gross_override"]))
            if o["ft1_net_override"]: net_out = q(Decimal(o["ft1_net_override"]))
        gross_by_no[no] = gross
        series = no.split("/")[0]
        msg = ";".join([d, dt, no, str(gross), prev.get(series, "")])
        h = sign(msg) if o["validated"] else "0"
        if o["tamper_hash"] and no == o["ft2_no"]: h = h[:-4] + ("AAAA" if h[-4:] != "AAAA" else "BBBB")
        prev[series] = h
        body.append(
            f"<Invoice><InvoiceNo>{no}</InvoiceNo><DocumentStatus><InvoiceStatus>N</InvoiceStatus><InvoiceStatusDate>{dt}</InvoiceStatusDate>"
            f"<SourceID>ADM</SourceID><SourceBilling>P</SourceBilling></DocumentStatus><Hash>{h}</Hash><HashControl>{hash_ctl}</HashControl>"
            f"<Period>5</Period><InvoiceDate>{d}</InvoiceDate><InvoiceType>{typ}</InvoiceType>"
            f"<SpecialRegimes><SelfBillingIndicator>0</SelfBillingIndicator><CashVATSchemeIndicator>0</CashVATSchemeIndicator><ThirdPartiesBillingIndicator>0</ThirdPartiesBillingIndicator></SpecialRegimes>"
            f"<SourceID>ADM</SourceID><SystemEntryDate>{dt}</SystemEntryDate><CustomerID>CF</CustomerID>{''.join(xml_lines)}"
            f"<DocumentTotals><TaxPayable>{tax_payable}</TaxPayable><NetTotal>{net_out}</NetTotal><GrossTotal>{gross}</GrossTotal></DocumentTotals></Invoice>")
    tot_c = q(tot_c + Decimal(o["total_credit_delta"]))
    customers = o["customers"] or [("CF", "999999999", "Consumidor final")]
    cust_xml = "".join(
        f"<Customer><CustomerID>{cid}</CustomerID><AccountID>Desconhecido</AccountID><CustomerTaxID>{nif}</CustomerTaxID><CompanyName>{nm}</CompanyName>"
        f"<BillingAddress><AddressDetail>Desconhecido</AddressDetail><City>Desconhecido</City><Country>Desconhecido</Country></BillingAddress>"
        f"<SelfBillingIndicator>0</SelfBillingIndicator></Customer>" for cid, nif, nm in customers)
    taxentry = f"<TaxTableEntry><TaxType>IVA</TaxType><TaxCountryRegion>{o['tax_region']}</TaxCountryRegion><TaxCode>{o['line_tax_code']}</TaxCode><Description>Taxa de teste</Description><TaxPercentage>{o['line_tax_pct']}</TaxPercentage></TaxTableEntry>"
    return (f'<?xml version="1.0" encoding="UTF-8"?><AuditFile xmlns="{NS}">'
        f"<Header><AuditFileVersion>1.01_01</AuditFileVersion><CompanyID>EMPRESA TESTE</CompanyID><TaxRegistrationNumber>5103105000</TaxRegistrationNumber>"
        f"<TaxAccountingBasis>F</TaxAccountingBasis><CompanyName>Empresa de Teste Sintetico</CompanyName>"
        f"<CompanyAddress><AddressDetail>Rua de Teste</AddressDetail><City>Luanda</City><Country>AO</Country></CompanyAddress>"
        f"<FiscalYear>2026</FiscalYear><StartDate>2026-01-01</StartDate><EndDate>2026-12-31</EndDate><CurrencyCode>AOA</CurrencyCode>"
        f"<DateCreated>2026-10-12</DateCreated><TaxEntity>Global</TaxEntity><ProductCompanyTaxID>5103105000</ProductCompanyTaxID>"
        f"<SoftwareValidationNumber>{soft}</SoftwareValidationNumber><ProductID>SaftAoTeste/Bitubi Solutions</ProductID><ProductVersion>0.1</ProductVersion></Header>"
        f"<MasterFiles>{cust_xml}<Product><ProductType>P</ProductType><ProductCode>P001</ProductCode><ProductDescription>Produto de teste</ProductDescription><ProductNumberCode>P001</ProductNumberCode></Product>"
        f"<TaxTable>{taxentry}</TaxTable></MasterFiles>"
        f"<SourceDocuments><SalesInvoices><NumberOfEntries>{len(docs)}</NumberOfEntries><TotalDebit>{q(tot_d)}</TotalDebit><TotalCredit>{tot_c}</TotalCredit>"
        f"{''.join(body)}</SalesInvoices></SourceDocuments></AuditFile>")

if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "sales-base.xml"), "w", encoding="utf-8").write(build())
    print("ok")
