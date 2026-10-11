# 04 — Assinatura e encadeamento dos documentos

> **Estado: especificado, com a ressalva de que a fonte é uma proposta oficial de 2018** (ver abaixo). Os parâmetros (RSA 1024 bits, SHA-1, PKCS#1 v1.5) vêm dessa proposta e têm vectores de teste (`conformance/signature/`). **Antes de usar em produção, confirmar** que continuam em vigor no regime actual, incluindo o de facturação electrónica de 2025/26.

## Níveis de verificação usados aqui

| Estado | Significado |
|---|---|
| **verificado** | Consta de legislação publicada no Diário da República |
| **verificado (proposta)** | Consta da *Proposta de Decreto Executivo* do Ministério das Finanças "Regras e requisitos para validação de sistemas de processamento electrónico de facturação dos contribuintes" (2018). Não foi confirmado que o texto final em vigor é idêntico |
| **inferido** | Deduzido a partir de evidência indirecta; não normativo |
| **por confirmar** | Sem fonte primária |

## Base legal

- O Decreto Presidencial 312/18, art. 7.º, alínea c), exige que o sistema permita identificar alterações aos registos de facturas e documentos rectificativos "através de um algoritmo de cifra assimétrica e de uma chave privada de conhecimento exclusivo do produtor do sistema". *(verificado)*
- Os requisitos técnicos concretos são remetidos, no art. 7.º, alínea f), para acto próprio do titular do departamento ministerial das Finanças. A proposta de 2018 (acima) é a fonte desses requisitos que localizámos. *(verificado)*

## Algoritmo e chaves

| Item | Valor | Estado |
|---|---|---|
| Algoritmo | **RSA** (chaves assimétricas) | verificado (proposta) |
| Chave privada | Do exclusivo conhecimento do produtor do software, protegida no software | verificado (proposta) |
| Chave pública | Extraída da privada, formato **PEM em base64**, ficheiro `.txt`, enviada à AGT com a Declaração Modelo 8 | verificado (proposta) |
| Mudança de par de chaves | Só pelo produtor, após comunicação à AGT (Modelo 8) e envio da nova chave pública | verificado (proposta) |
| Versão da chave | Inteiros sequenciais, a partir de 1 | verificado (proposta) |
| Tamanho da chave | **1024 bits** (Anexo II da proposta; coerente com 172 caracteres base64 = 128 bytes) | verificado (proposta) |
| Algoritmo de resumo (digest) | **SHA-1** ("Formato do Hash da mensagem = SHA-1"; exemplo `openssl dgst -sha1 -sign`) | verificado (proposta) |
| Padding | **PKCS#1 v1.5** (a proposta escreve "OAEP Padding = PKCS1 v1.5 padding", terminologia imprecisa; o procedimento exemplificado, `openssl dgst -sha1 -sign`, é a assinatura RSASSA-PKCS1-v1_5) | verificado (proposta) |
| Mensagem | UTF-8, sem quebra de linha no fim | verificado (proposta) |
| Codificação da assinatura | Base64 numa única linha, **172 caracteres** (campo `Hash`, texto 172) | verificado + verificado (proposta) |
| Certificado | Não é exigido certificado de entidade credenciada; pode ser auto-assinado, para extrair a chave pública | verificado (proposta) |

## Mensagem a assinar

*(verificado (proposta))*

A mensagem é o texto formado pela concatenação dos campos abaixo, **separados por `;`** (ponto e vírgula), sem aspas nem quebras de linha.

| Documento | Campos, por ordem |
|---|---|
| Facturas de venda (`SalesInvoices`, tabela 4.1) | `InvoiceDate`; `SystemEntryDate`; `InvoiceNo`; `GrossTotal`; `Hash` do documento anterior |
| Documentos de movimento (`MovementOfGoods`, 4.2) e de conferência (`WorkingDocuments`, 4.3) | O equivalente: data do documento (`MovementDate`/`WorkDate`); `SystemEntryDate`; número do documento (`DocumentNumber`); `GrossTotal`; `Hash` do documento anterior *(a proposta detalha apenas o caso das facturas; os outros seguem a SAP e a analogia, estado: não verificado)* |

### Formato de cada campo

| Campo | Formato | Exemplo |
|---|---|---|
| `InvoiceDate` | `AAAA-MM-DD` | `2019-01-11` |
| `SystemEntryDate` | `AAAA-MM-DDTHH:MM:SS`, sem fuso horário nem milissegundos | `2019-01-11T11:27:08` |
| `InvoiceNo` | `<tipo interno> <série>/<sequência>`, ver R-010 | `FAC 001/9` |
| `GrossTotal` | Decimal com **duas casas**, ponto como separador, **sem separador de milhares** | `1200.00` |
| `Hash` anterior | Base64 | (ver exemplo) |

- O `GrossTotal` assinado é **o valor arredondado a duas casas decimais**, e é esse mesmo valor que se exporta no SAF-T. *(verificado (proposta))*
- Em **moeda estrangeira**, assina-se o **contravalor em AOA**, que é o valor exportado. *(verificado (proposta))*
- Em documentos de movimento e de conferência (4.2 e 4.3) sem valor na base de dados, `GrossTotal` assume `0.00` na assinatura. *(verificado (proposta))*
- Datas e valores monetários seguem também as regras gerais R-030 e R-031.

### Encadeamento

- Cada documento é assinado com o `Hash` do **último documento emitido da mesma série e tipo**. *(verificado (proposta))*
- **Primeiro documento da série:** o campo "`Hash` anterior" é **vazio**. *(verificado (proposta))*
- **Séries plurianuais:** no início de cada exercício, o primeiro documento **pode** ser assinado com o `Hash` do último documento do exercício anterior. *(verificado (proposta))*
- No primeiro documento a mensagem **termina em `;`** (campo final vazio), sem quebra de linha: `2018-05-18;2018-05-18T11:22:19;FAC 001/18;53.00;`. *(verificado (proposta), Anexo II)*

### Exemplo oficial

*(da proposta de 2018)* Com `InvoiceDate = 2019-01-11`, `SystemEntryDate = 2019-01-11T11:27:08`, `InvoiceNo = FAC 001/9`, `GrossTotal = 1200.00` e o `Hash` anterior do vector `conformance/signature/message-construction.json`, a mensagem é:

```
2019-01-11;2019-01-11T11:27:08;FAC 001/9;1200.00;<Hash anterior em base64, 172 caracteres>
```

> O texto extraído do PDF da proposta tem o `Hash` do exemplo corrompido na linha da mensagem (170 caracteres, base64 inválido). A versão da tabela da mesma página tem 172 caracteres e é base64 válido de 128 bytes; é a que se usa nos vectores.

## `HashControl` (chave de controlo)

- Contém a **versão da chave privada** usada na assinatura (inteiro sequencial). *(verificado + verificado (proposta))*
- Documento gerado por programa **não validado** pela AGT: `HashControl = "0"`. *(verificado: Decreto Executivo 317/20)*
- Documentos **integrados** de outro sistema (`SourceBilling = I`): `Hash` **igual** ao do sistema emissor, e `HashControl` = `<n.º do certificado original>.<versão da chave original>`. *(verificado (proposta))*
- Documentos integrados de programa **não validado**: `HashControl = "Não Validado pela AGT"` e `Hash = "0"`; não devem ser reimpressos. *(verificado (proposta))*
- Documentos **recuperados de impressos manuais** (`SourceBilling = M`): `HashControl = <versão da chave>-<tipo>M <série manual>/<número manual>`, por exemplo `1-FTM ab/0001`. *(verificado (proposta))*
- Documentos **recuperados de duplicados** (`SourceBilling = M`): `HashControl = <versão da chave>-<tipo>D <identificação do documento>`, por exemplo `1-FTD KM 2019A/0099`. *(verificado (proposta))*
- Quem integra **não recalcula nem altera** o conteúdo dos documentos integrados, incluindo a identificação única; a assinatura é da responsabilidade do sistema original. *(verificado (proposta))*
- Uma série não pode misturar documentos de origens diferentes (emitidos no sistema e importados). *(verificado (proposta))*

## Impressão (referência, fora do ficheiro SAF-T)

- Os documentos assinados só podem ser impressos depois de assinados. *(verificado (proposta))*
- Imprime-se: os caracteres nas posições **1, 11, 21 e 31** do `Hash`, um hífen, e `Processado por programa validado n.º <certificado>/AGT`. Exemplo da proposta: `PbRc-Processado por programa validado n.º 0000/AGT`. A documentação da SAP acrescenta o ano (`/AGT/AAAA`) e o nome do software; **a forma exacta em vigor está por confirmar**.
- Documentos não assinados (por exemplo, recibos) imprimem `Emitido por programa validado n.º <certificado>/AGT`. *(verificado (proposta))*
- Documentos de estorno que anulam uma factura **não são assinados** e têm numeração própria. *(SAP: não verificado)*

## Armazenamento

- A assinatura e a versão da chave são gravadas na base de dados, associadas ao registo integral do documento, sem encriptação, durante o prazo de arquivo legal. *(verificado (proposta))*

## Procedimento de referência (Anexo II da proposta)

Chaves, com OpenSSL (apenas ilustrativo; o produtor pode usar qualquer implementação):

```bash
openssl genrsa -out ChavePrivada.pem 1024
openssl rsa -in ChavePrivada.pem -out ChavePublica.pem -outform PEM -pubout   # a enviar à AGT, renomeada para .txt
```

Assinatura de um documento (mensagem gravada **sem** quebra de linha no fim):

```bash
openssl dgst -sha1 -sign ChavePrivada.pem -out Registo1.sha1 Registo1.txt
openssl enc -base64 -in Registo1.sha1 -out Registo1.b64 -A      # 172 caracteres numa linha
openssl dgst -sha1 -verify ChavePublica.pem -signature Registo1.sha1 Registo1.txt   # verificação
```

## Vectores de teste

`conformance/signature/signing-chain.json` tem uma cadeia de três documentos com a **mensagem, o `Hash` esperado e uma chave de teste** (apenas para estes vectores). Os valores foram gerados com OpenSSL seguindo o procedimento acima e confirmados com uma segunda implementação independente (`python-cryptography`, PKCS#1 v1.5 + SHA-1): as duas dão a mesma assinatura (PKCS#1 v1.5 é determinístico). Uma biblioteca passa se, dada a mesma chave e os mesmos campos, produzir exactamente o `expectedHash`.

## Ressalvas

1. **Fonte é uma proposta de 2018.** Não encontrámos o acto final publicado. O Anexo II é em grande parte adaptado da especificação portuguesa: o próprio texto fala em "SAF-T(PT)" e o exemplo tem gralhas (por exemplo, `53.002;` no cabeçalho do exemplo e datas em formatos diferentes), pelo que usámos o texto passo a passo e não o exemplo literal.
2. **Corroboração prática (não normativa).** Em 2020, um produtor reportou no repo `assoft-portugal/SAF-T-AO` (issue #49) que o validador da AGT rejeitava o 2.º e o 3.º hash de um ficheiro, anexando uma chave pública de nome `public_phpPOS_1024.pem` (o nome sugere 1024 bits; não foi verificado). O que o caso mostra com segurança é que o validador **verifica** a cadeia de hashes. Em 2021, outro (issue #195) mostrou que o portal valida a cadeia por série, e que **um documento com `SourceBilling = I` no meio de uma série `P` fazia falhar a validação** (ver R-045).
3. **Regime de 2025/26.** A facturação electrónica nova usa assinatura **RS256** (RSA com SHA-256) numa API própria. **Não** sabemos se o regime novo alterou também os parâmetros do `Hash` do SAF-T. Confirmar antes de produção.
4. **Segurança.** SHA-1 e RSA de 1024 bits são considerados fracos hoje. Usar estes parâmetros **apenas** para este campo, porque é o que a AGT define; não os usar noutro contexto. Se a AGT migrar para parâmetros mais fortes, esta secção muda.
5. Forma exacta da frase impressa (com ou sem o ano).

## Facturação electrónica (fora do âmbito)

A API de facturação electrónica de 2025/26 usa assinatura **RS256** (RSA com SHA-256) sobre campos próprios. É outro mecanismo. Não usar como evidência do digest do `Hash` do SAF-T.
