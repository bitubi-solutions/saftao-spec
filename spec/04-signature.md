# 04 — Assinatura e encadeamento dos documentos

> **Estado: parcialmente verificado. Não implementar a assinatura enquanto o algoritmo estiver "por confirmar".** Uma assinatura errada produz documentos fiscalmente inválidos.

## O que está verificado (legislação)

- Cada documento assinado tem o campo `Hash` (**Chave do documento**), texto de **172 caracteres** (campo 4.1.4.4 do Decreto Executivo 317/20; equivalentes em 4.2.3.4, 4.3.4.4 e 4.5.2.3).
- Cada documento tem `HashControl` (**Chave de controlo**, texto até 70): contém a **versão da chave privada** usada na assinatura. Deve ser preenchido com `0` quando o documento é gerado por programa **não validado**.
- O `Hash` e o `HashControl` constam do XSD.

## O que vem de fonte secundária (SAP, documentação de produto de 23/10/2020)

*(não verificado em fonte oficial)*

A assinatura é produzida aplicando RSA a uma cadeia de texto formada pela concatenação, separada por `;`, dos campos:

| Tipo de documento | Campos, por ordem |
|---|---|
| Facturas de venda (`SalesInvoices`) | `InvoiceDate`; `SystemEntryDate`; `InvoiceNo`; `GrossTotal`; `Hash` do documento anterior da mesma série |
| Documentos de trabalho (`WorkingDocuments`) | `WorkDate`; `SystemEntryDate`; `DocumentNumber`; `GrossTotal`; `Hash` do documento anterior da mesma série |
| Documentos de movimento (`MovementOfGoods`) | `MovementDate`; `SystemEntryDate`; `DocumentNumber`; `GrossTotal`; `Hash` do documento anterior da mesma série |

- O encadeamento é por **série**: cada `Hash` depende do `Hash` do documento anterior da mesma série.
- A versão da chave privada começa em `1` e incrementa quando o par de chaves é substituído.
- Documentos de **estorno** que anulam uma factura não são assinados, e devem ter numeração própria.
- Na impressão de um documento assinado imprime-se: os caracteres nas posições 1, 11, 21 e 31 do `Hash`, um hífen, e a frase `Processado por programa validado n.º <certificado>/AGT/<ano> - <nome do software>`.

## Por confirmar (bloqueia a implementação)

1. **Algoritmo de resumo**: não está indicado nas fontes lidas. 172 caracteres em base64 correspondem a 128 bytes, o que é compatível com RSA de 1024 bits, mas **não** determina SHA-1 ou SHA-256. *(Inferência: não normativa.)*
2. **Esquema de preenchimento**: PKCS#1 v1.5 ou outro.
3. **Valor de "Hash anterior" no primeiro documento de uma série**: vazio?
4. **Formatação exacta dos campos** na cadeia: formato de `InvoiceDate` e `SystemEntryDate`, número de casas decimais e separador decimal de `GrossTotal`.
5. **Relação com a facturação electrónica de 2025/26**: a API da AGT usa assinatura RS256 (RSA com SHA-256) sobre campos próprios; **não** é o mesmo mecanismo e não deve ser confundida com esta (ver `00-overview.md`).

## Como fechar estes pontos

Fonte primária: o texto do Decreto Presidencial 312/18, de 21 de Dezembro (regime jurídico dos programas de facturação, que o repositório de referência disponibiliza apenas como imagem digitalizada, sem texto) e a documentação técnica da AGT. Passos: obter o texto (OCR ou versão no Diário da República), localizar a norma do algoritmo, e **só depois** escrever os vectores de teste (`conformance/signature/`) com um par de chaves de teste.
