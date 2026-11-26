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

## Cuidados

- Os arquivos `.env`, a pasta `O elo/` e o `o-elo-universal-base-do-projeto.md` estão no `.gitignore` e não vão para o GitHub.
- Commit, push e deploy só com aprovação.
