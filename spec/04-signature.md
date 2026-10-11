# 04 — Assinatura e encadeamento dos documentos

> **Estado: especificado, excepto o algoritmo de resumo (digest) e o padding, que continuam por confirmar.** As bibliotecas podem implementar a **construção da mensagem a assinar** (testável, ver `conformance/signature/`). **Não** devem implementar a assinatura propriamente dita até o digest estar confirmado: uma assinatura errada produz documentos fiscalmente inválidos.

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
| Tamanho da chave | **1024 bits**: o exemplo oficial de assinatura da proposta tem 172 caracteres base64 = 128 bytes, que é o tamanho de uma assinatura RSA de 1024 bits | **inferido** |
| Algoritmo de resumo (digest) | SHA-1 nas especificações portuguesas equivalentes e numa biblioteca de terceiros para Angola; **a proposta diz só "RSA"** | **por confirmar** |
| Padding | PKCS#1 v1.5 é o habitual; não indicado | **por confirmar** |
| Codificação da assinatura | Base64, 172 caracteres (campo `Hash`, texto 172) | verificado + verificado (proposta) |

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
- Se a mensagem do primeiro documento termina em `;` (campo final vazio): **por confirmar**; na especificação portuguesa equivalente termina.

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

## O que falta para fechar

1. Fonte para o **digest** e o **padding** (texto final do acto de requisitos técnicos, ou documentação técnica da AGT para produtores de software).
2. Se o texto final da proposta é idêntico ao localizado.
3. Forma exacta da frase impressa.

Quando o digest estiver confirmado, acrescentam-se a chave de teste e os vectores de assinatura (`conformance/signature/`), e as bibliotecas passam a implementar a assinatura.

## Facturação electrónica (fora do âmbito)

A API de facturação electrónica de 2025/26 usa assinatura **RS256** (RSA com SHA-256) sobre campos próprios. É outro mecanismo. Não usar como evidência do digest do `Hash` do SAF-T.
