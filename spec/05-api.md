# 05 — Contrato mínimo das bibliotecas

Todas as bibliotecas `saftao-*` oferecem as mesmas capacidades, com nomes e tipos idiomáticos de cada linguagem. Este documento define **o que** oferecem, não **como** se chamam.

## Níveis de conformidade

Uma biblioteca declara o nível que cumpre. Cada nível inclui o anterior.

| Nível | Capacidade | Como se prova |
|---|---|---|
| **1. Esquema** | Validar um ficheiro contra o XSD, **incluindo** as restrições de identidade (`xs:unique`, `xs:keyref`, ver R-046) | Casos `level = schema` de `conformance/cases/` |
| **2. Regras** | Aplicar as regras de negócio de `03-business-rules.md` | Casos `level = business-rule`; cada biblioteca lista as regras (`R-nnn`) que implementa |
| **3. Assinatura** | Construir a mensagem a assinar, formatar o `GrossTotal`, assinar e verificar o `Hash` | `conformance/signature/` |

Uma biblioteca de nível 1 é útil e legítima. Declara o que não faz.

## Operações

### `validate(entrada) → relatório`
- Entrada: um ficheiro (caminho) ou o conteúdo em memória.
- Relatório: `válido` (booleano) e uma lista de problemas.
- Problema: `nível` (`schema` | `business-rule`), `regra` (`R-nnn`, só em `business-rule`), `mensagem`, `linha` e `coluna` (ou "desconhecido").
- `válido` é verdadeiro **se e só se** a lista de problemas está vazia.
- Só o **resultado** (`válido`) é comparado entre linguagens; as mensagens podem variar.
- Se o ficheiro não é XML bem formado, reportam-se só problemas de `schema`.

### `buildSigningMessage(dataDocumento, dataHoraGravação, númeroDocumento, totalComImpostos, hashAnterior) → texto`
Ver `04-signature.md`. Rejeita formatos inválidos (datas, `GrossTotal` sem duas casas, etc.). `hashAnterior` vazio no primeiro documento.

### `formatGrossTotal(valor) → texto`
Duas casas decimais, ponto decimal, sem separador de milhares. Rejeita valores negativos.

### `sign(chavePrivada, mensagem) → hash` e `verify(chavePública, mensagem, hash) → booleano`
RSA, SHA-1, PKCS#1 v1.5; mensagem em UTF-8; `hash` em base64 numa só linha. Aceita chaves PEM em PKCS#1 e PKCS#8.

## Requisitos de segurança (todas as linguagens)

1. **Não aceitar `DOCTYPE`** nem resolver entidades externas.
2. **Não aceder à rede** ao validar: o `xsi:schemaLocation` do ficheiro é ignorado e o XSD vem embebido na biblioteca.
3. **Streaming** sempre que a linguagem o permita: os ficheiros SAF-T podem ter centenas de MB.
4. Documentar que SHA-1 e RSA de 1024 bits são fracos e só se usam no campo `Hash`.

## Versões mínimas das linguagens

Cada biblioteca escolhe a versão mínima **mais antiga que ainda seja comum em Angola**, para que o maior número possível de produtores a possa usar. A escolha é registada no `README` de cada biblioteca e justificada.

| Biblioteca | Mínimo | Nota |
|---|---|---|
| `saftao-java` | Java 8 | Decisão do produto; testada num JDK 8 real |
| outras | a definir quando cada uma arrancar | |

## Dependências

Quanto menos, melhor: uma biblioteca fiscal com muitas dependências é difícil de auditar e de actualizar. Preferir a biblioteca padrão da linguagem. Dependências de teste são livres.
