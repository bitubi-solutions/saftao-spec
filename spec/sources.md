# Fontes

Esta especificação foi construída a partir das fontes abaixo. **Nenhuma foi obtida directamente do portal da AGT**: o XSD e os diplomas vêm do repositório comunitário `assoft-portugal/SAF-T-AO`, que os reúne.

## Primárias (legislação e esquema)

| Fonte | Uso | Notas |
|---|---|---|
| `XSD/SAFTAO1.01_01.xsd` do repositório [assoft-portugal/SAF-T-AO](https://github.com/assoft-portugal/SAF-T-AO) | `schema/SAFTAO1.01_01.xsd`, `spec/02-fields.md` | Autoria AGT segundo o próprio ficheiro; `Status: Development`; `Copyright OECD`. Repositório sob licença MIT. SHA-256 do ficheiro: `e9a938e1f47ac3d84ffbb26d0d95b827fc769a065c9d20533d0262c12f8c2631`. Data de modificação no ficheiro: 2024-10-16. |
| Decreto Executivo n.º 317/20, de 14 de Dezembro (Diário da República, I Série) | `spec/03-business-rules.md`, `spec/04-signature.md` | Anexo "Estrutura de dados". Lido a partir do PDF com texto. |
| Decreto Presidencial n.º 312/18, de 21 de Dezembro | Fundamento legal; **ainda não lido** | PDF disponível só como imagem; precisa de OCR. |
| Decreto Presidencial n.º 71/25 e Decreto Executivo n.º 683/25 | Facturação electrónica; **fora do âmbito** | PDFs só em imagem. |

## Secundárias (não normativas)

| Fonte | Uso |
|---|---|
| SAP, *SAF-T Digital Signature for Angola — Product Documentation*, 23/10/2020 | Composição da cadeia de assinatura em `04-signature.md` (marcada não verificada) |
| Documentação "Registar Factura" da AGT (quiosque AGT, facturação electrónica) | Indicação de RS256 na API de facturação electrónica; **fora do âmbito** desta versão |

## O que ficou por verificar

- Hash do XSD contra as *releases* do repositório de origem (a pesquisa indica que publicam SHA-256 por revisão; não foi comparado).
- Existência de versão mais recente do XSD no portal da AGT.
- Todo o conteúdo marcado "por confirmar" ou "não verificado" em `03-business-rules.md` e `04-signature.md`.

## Como actualizar

Quando o XSD mudar, substituir `schema/`, actualizar o SHA-256 aqui, e regenerar a referência de campos:

```bash
python3 -I tools/xsd_to_md.py schema/SAFTAO1.01_01.xsd > spec/02-fields.md
```
