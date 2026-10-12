# Pacote para validadores externos

Ficheiros SAF-T (AO) **sintéticos** (dados inventados), cada um a isolar **uma** observação de [`spec/06-validator-observations.md`](../../spec/06-validator-observations.md). Servem para descobrir, num validador externo, regras que o XSD e a lei não explicam.

Os ficheiros `O-*` e `R-*` passam o XSD (confirmado com `tools/validate.py`): **qualquer erro** que um validador externo dê a estes vem de regras **além do esquema**. Os ficheiros `C-*` (C-01 a C-06) são **controlos** que **violam** o XSD de propósito: um validador de esquema tem de os rejeitar. Se não os rejeitar, não está a validar o esquema, e o resto dos resultados não conta. Ver `pack.json` para o que cada ficheiro faz e o que se espera.

## Regras de uso

1. **Só estes ficheiros sintéticos.** A política de privacidade do [saft.ao](https://saft.ao) diz que o ficheiro é processado em memória, não é gravado e o conteúdo nunca vai para as ferramentas de analítica. Ainda assim, os servidores estão em Portugal (transferência fora de Angola, Lei n.º 22/11) e o site usa Cloudflare Turnstile, Sentry (gravação de sessão com texto mascarado) e Google Analytics. Por prudência, **nunca carregar ficheiros reais de contribuintes** em validadores de terceiros; para dados reais, usar o validador oficial da AGT.
2. **À mão, um a um, no browser.** O saft.ao pede confirmação anti-robô (Cloudflare Turnstile) e não anuncia uma API; **não automatizar nem contornar**. Se for preciso volume, pedir uma API ao operador pelo link "Contacte-nos" do site.
3. **O saft.ao não é a AGT.** É um validador independente, mantido pela equipa do KwanzaGest, sem afiliação à AGT. Um resultado dele mostra o que **esse** validador faz, não o que a AGT faz. Só o validador da AGT é oficial.
4. **O validador de produtores da AGT** (no portal, com a tua conta): usar **apenas a função de validar**, nunca a de entrega. Confirmar os termos de uso antes.

## Onde estão os ficheiros

No Windows: `C:\Users\DumildeFernando\github\bitubi\saftao-spec\conformance\oracle\` (a mesma pasta que no WSL). Começar por `00-base.xml`: se o validador reclamar do ficheiro-base, anotar a mensagem, porque afecta a leitura de todos os outros.

## Como registar resultados

Copiar `results/TEMPLATE.md` para `results/<validador>-AAAA-MM-DD.md` e preencher as duas últimas colunas.

Para cada ficheiro, copiar a mensagem **exacta** do validador (ou "sem erros") para `results/<validador>-AAAA-MM-DD.md`, neste formato:

```markdown
| Ficheiro | Resultado | Mensagem exacta |
|---|---|---|
| 00-base.xml | erro | "…" |
| O-001-taxpayable-errado.xml | erro | "…" |
```

Com os resultados, cada observação passa de "observada" a "confirmada em <validador>, data" (ou "não reproduzida"), e as confirmadas viram casos de conformance.

## Regenerar

```bash
python3 tools/make_oracle_pack.py conformance/oracle     # requer: cryptography
```

## Ficheiros `nv/` (sem assinatura)

`nv/` tem as mesmas variações com **software `0` e `Hash` `0`** (programa não validado), para que o número de software e o hash não mascarem os outros erros. O ficheiro `O-032` (hash adulterado) não tem versão `nv`. Os ficheiros da pasta principal estão assinados com a chave de teste e usam o número de software inventado `999/AGT/2026`, que um validador com a lista da AGT recusará.

## Testar no validador da AGT (portal)

Só o validador da AGT pode confirmar as observações de `06-validator-observations.md`. Decisão e responsabilidade são de quem testa; sugestão de procedimento:

1. **Ler os termos de uso** do portal e confirmar que o teste repetido de ficheiros é permitido.
2. **Usar apenas a função de validar do portal do produtor de software**, nunca a de entrega/submissão. Se o ecrã falar em "submeter", "entregar" ou emitir comprovativo, **parar**.
3. **Usar o NIF da própria empresa que testa** em vez do NIF de exemplo da AGT: `python3 tools/make_oracle_pack.py conformance/oracle --nif <NIF>` (requer `cryptography`). Só dados inventados nos restantes campos.
4. **Começar por `nv/00-base-nv.xml`**. Se o validador rejeitar a versão `nv` por completo, anotar a mensagem e passar à versão assinada, esperando erro do número de software.
5. **Ficheiros indentados** dão números de linha úteis nas mensagens (os do pacote estão numa só linha).
6. Registar a mensagem **exacta** em `results/` (ver acima).
