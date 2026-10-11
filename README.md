# saftao-spec

Especificação e testes de conformidade partilhados das bibliotecas `saftao-*`, que geram, lêem e validam o ficheiro SAF-T (AO).

Este repo é a fonte de verdade das regras de negócio e dos casos de teste. Cada biblioteca (`saftao-java`, `saftao-python`, `saftao-csharp`, `saftao-php`, e depois `saftao-rust` e `saftao-c`) implementa a especificação de forma nativa e tem de passar os mesmos testes.

## Estado

Em arranque. Ainda sem especificação nem testes.

## Planeado

- `spec/`: regras de negócio em Markdown (totais, numeração, datas, assinatura/encadeamento).
- `conformance/`: ficheiros SAF-T válidos e inválidos, cada um com o resultado esperado.

## Licença

Apache-2.0. Ver [LICENSE](LICENSE).
