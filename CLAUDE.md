---
tipo: instrucoes
negocio: elo-universal
atualizado: 2026-11-25
---

# O Elo Universal: página de vendas

- **O que é:** a página de vendas do Elo, feita no Antigravity e no ar em https://o-elo-universal.vercel.app/.
- **Onde fica o site:** na pasta `site/` (é ela que a Vercel publica, conforme o `vercel.json`).
- **Repositório:** GitHub `oelouniversal/O-Elo-Universal`, com a conta `oelouniversal`.
- **Vídeos do Elo:** ficam em outra pasta, `../O elo universal CR/`, que tem as próprias regras.

## Decisões

- **2026-11-19: não reduzir os efeitos visuais da página.** Isso vale para estrelas nos botões, poeira estelar, partículas, sigilo celeste, olho vivo, parallax e flip cards, mesmo que o briefing original vete a "estética cósmica". Não listar "reduzir efeitos" como melhoria. Ajustes de copy, estrutura, conformidade e acessibilidade continuam valendo (o `prefers-reduced-motion` já existe).

- **2026-11-26:**
  - O link "Capítulo 1 grátis" sai do Hero. O Capítulo 1 fica só como saída depois do preço ("Ainda em dúvida?").
  - Novo preço: **R$ 49,90 como preço de lançamento**, que passa a **R$ 67** numa data real (sugestão: 30 dias depois do lançamento). Nunca usar "de/por" com valor inventado.
  - O preço só muda **junto com as melhorias do produto** (fechamento, bônus corrigidos, Caderno vivo). Até lá, a página segue com R$ 37.
  - Título do Hero (aplicado): "Você já conhece as 7 leis. Agora aplique cada uma no seu dia a dia, como um cientista faria: testando."
  - Nova edição do caderno: fechamento "A releitura" e página de créditos aprovados; DOIs do Capítulo 1 e link do Nobel. Bônus A e B refeitos. Antigos em `Produto/antigos/`. Detalhes em `Produto/Notas-Editoriais-e-Pendencias.md`.
  - Seção 4 da página virou uma visita guiada pelas páginas reais do Capítulo 1 (mantém o olho vivo). Ela roda também com movimento reduzido, como o resto da página.
  - O caderno continua assinado só por "O Elo Universal".
  - **Preço em vigor:** R$ 49,90 (já cobrado na Wiven), preço de lançamento **até 31/12/2026**. A partir de 01/01/2027, R$ 67: a página troca sozinha (`OFERTA_FIM` em `site/js/config.js`); **a Wiven precisa ser mudada para R$ 67 à mão no dia 01/01/2027**. Sem "de/por" riscado: o produto nunca custou R$ 67.
  - **Caderno vivo:** o caderno para escrever no próprio aparelho, no link reservado `https://o-elo-universal.vercel.app/caderno-vdx9g64y1a` (fora do Google; quem tiver o link abre: risco aceito para o preço do produto). As anotações ficam só no navegador da pessoa (nada vai para servidor). Tem PDF do caderno preenchido, cópia de segurança e restauração. Texto vem do mesmo `content.json` do PDF: depois de mudar o caderno, rodar `python _trabalho/gerar_caderno_vivo.py`. O link é entregue pela Wiven depois da compra (configuração manual do dono).
  - Seção "Os sete experimentos" virou a "jornada de 22 dias": trilha das 7 leis com os dias de cada uma, terminando na releitura, e um painel com o que a pessoa faz e anota. Links `#exp-N` (eco do vídeo) abrem a lei certa.

## Cuidados

- Os arquivos `.env`, a pasta `O elo/` e o `o-elo-universal-base-do-projeto.md` estão no `.gitignore` e não vão para o GitHub.
- Commit, push e deploy só com aprovação.
