# Pacote para validadores externos

Ficheiros SAF-T (AO) **sintéticos** (dados inventados), cada um a isolar **uma** observação de [`spec/06-validator-observations.md`](../../spec/06-validator-observations.md). Servem para descobrir, num validador externo, regras que o XSD e a lei não explicam.

Todos passam o XSD (confirmado com `tools/validate.py`). Logo, **qualquer erro** que um validador externo dê a estes ficheiros vem de regras **além do esquema**. Ver `pack.json` para o que cada ficheiro faz e o que se espera.

## Regras de uso

1. **Só estes ficheiros sintéticos.** A política de privacidade do [saft.ao](https://saft.ao) diz que o ficheiro é processado em memória, não é gravado e o conteúdo nunca vai para as ferramentas de analítica. Ainda assim, os servidores estão em Portugal (transferência fora de Angola, Lei n.º 22/11) e o site usa Cloudflare Turnstile, Sentry (gravação de sessão com texto mascarado) e Google Analytics. Por prudência, **nunca carregar ficheiros reais de contribuintes** em validadores de terceiros; para dados reais, usar o validador oficial da AGT.
2. **À mão, um a um, no browser.** O saft.ao pede confirmação anti-robô (Cloudflare Turnstile) e não anuncia uma API; **não automatizar nem contornar**. Se for preciso volume, pedir uma API ao operador pelo link "Contacte-nos" do site.
3. **O saft.ao não é a AGT.** É um validador independente, mantido pela equipa do KwanzaGest, sem afiliação à AGT. Um resultado dele mostra o que **esse** validador faz, não o que a AGT faz. Só o validador da AGT é oficial.
4. **O validador de produtores da AGT** (no portal, com a tua conta): usar **apenas a função de validar**, nunca a de entrega. Confirmar os termos de uso antes.

## Como registar resultados

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
