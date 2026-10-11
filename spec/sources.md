# Fontes

Esta especificação foi construída a partir das fontes abaixo. **Nenhuma foi obtida directamente do portal da AGT.** O XSD e os diplomas vêm do repositório comunitário `assoft-portugal/SAF-T-AO`, que os reúne; a proposta de requisitos vem do sítio do Ministério das Finanças (`ucm.minfin.gov.ao`).

Os PDFs **não** são copiados para este repo; indicam-se aqui a origem e o SHA-256 do ficheiro lido.

## Primárias (legislação, proposta oficial e esquema)

| Fonte | Uso | Notas |
|---|---|---|
| `XSD/SAFTAO1.01_01.xsd` de [assoft-portugal/SAF-T-AO](https://github.com/assoft-portugal/SAF-T-AO) | `schema/SAFTAO1.01_01.xsd`, `spec/02-fields.md` | Autoria AGT segundo o próprio ficheiro; `Status: Development`; `Copyright OECD`; data de modificação no ficheiro: 2024-10-16. Repositório sob licença MIT. SHA-256: `e9a938e1f47ac3d84ffbb26d0d95b827fc769a065c9d20533d0262c12f8c2631` |
| Decreto Presidencial n.º 312/18, de 21 de Dezembro (Diário da República, I Série, n.º 189) e anexo "Estrutura de Dados" | `spec/03-business-rules.md` (R-030 a R-034), `spec/04-signature.md` (base legal) | PDF só com imagem (29 páginas). **Lidas visualmente as páginas 2 a 6** (art. 1.º a 14.º e início do anexo). O resto do anexo (tabelas de campos) não foi relido: coincide com o DE 317/20. SHA-256: `d008e3591828f5516583451dbb9c3ec6dcdd96c110e3b919daa70d37350acf53` |
| Decreto Executivo n.º 317/20, de 14 de Dezembro (Diário da República, I Série, n.º 201) | `spec/03-business-rules.md` (R-001 a R-013, R-020 a R-022, R-040, R-041), `spec/04-signature.md` | Anexo "Estrutura de dados". PDF com texto. SHA-256: `73be36b631a565e17ef0ed36c18771809b0e5fcab931d38c83a6bc3259d9e0ec` |
| *Regras e requisitos para validação de sistemas de processamento electrónico de facturação dos contribuintes* — **Proposta de Decreto Executivo** (Ministério das Finanças, 2018, 27 pp.) em [`ucm.minfin.gov.ao`](http://www.ucm.minfin.gov.ao/cs/groups/public/documents/document/zmlu/mdu1/~edisp/minfin055809.pdf) | `spec/04-signature.md` (algoritmo, mensagem, encadeamento, `HashControl`), R-023, R-024, R-035, R-042 a R-044 | **É uma proposta, não o texto final.** Não encontrámos o acto final publicado. SHA-256: `4bc3a781b72964dc52a604ad26edf8b857084172ccd892a727880cb41bd91f73` |

## Secundárias (não normativas)

| Fonte | Uso |
|---|---|
| SAP, *SAF-T Digital Signature for Angola — Product Documentation*, 23/10/2020 | Confirma a cadeia de assinatura; origem da frase impressa com o ano (`/AGT/AAAA`) e dos documentos de movimento e conferência |
| Pesquisas web sobre o digest | Indicam SHA-1 e chave de 1024 bits nas especificações **portuguesas** equivalentes (2010–2014) e numa biblioteca PHP/Laravel de terceiros para Angola. Não usadas como normativas |
| Documentação "Registar Factura" da AGT (quiosque AGT, facturação electrónica) | RS256 na API de facturação electrónica; **fora do âmbito** |

## Dados do repositório de origem

Para conferência:

- Releases do repo da ASSOFT publicam SHA-256 por revisão do XSD; **não foram comparados** com o hash acima.
- O repo inclui também `decreto-71-25.pdf` e `decreto-executivo-683-25.pdf` (facturação electrónica), **não lidos**: fora do âmbito.

## O que ficou por verificar

- Texto final em vigor do acto de requisitos técnicos (a proposta MinFin é de 2018).
- Digest e padding da assinatura (ver `04-signature.md`).
- Versão mais recente do XSD no portal da AGT.
- Todo o conteúdo marcado "por confirmar" ou "por transcrever" em `03-business-rules.md`.

## Como actualizar

Quando o XSD mudar, substituir `schema/`, actualizar o SHA-256 aqui e em `NOTICE`, e regenerar a referência de campos:

```bash
python3 -I tools/xsd_to_md.py schema/SAFTAO1.01_01.xsd > spec/02-fields.md
```
