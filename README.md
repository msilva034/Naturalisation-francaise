# Parcours Citoyen

Curso gratuito e trilíngue (PT / EN / FR) para o **examen civique** e a **entrevista de naturalização francesa**: 23 módulos de 15 minutos, 331 questões no formato oficial (44 situações práticas; o simulado completo segue a proporção oficial 28 + 12), blocos "Aprofundar" em 13 módulos, flashcards, simulados cronometrados, perguntas frequentes da entrevista, os 101 departamentos, contas opcionais e doações via PayPal.

O site inteiro é **um único arquivo**: `dist/index.html`. Não precisa de servidor.

---

## 1. Configurar (5 minutos)

Abra `src/config.js` e preencha:

| Campo | O que colocar |
|---|---|
| `maintainer` | Seu nome, se quiser aparecer na página "Apoiar" (ou deixe `""`). |
| `paypal.paypalMe` | Seu usuário PayPal.Me (crie em https://www.paypal.com/paypalme). Ex.: `"mashuca"` → os botões levam a `paypal.me/mashuca/5EUR`. |
| `paypal.hostedButtonId` | *Alternativa*: o ID de um botão "Doar" criado em https://www.paypal.com/donate/buttons (preencha só um dos dois). |
| `paypal.amounts` | Valores sugeridos, ex.: `[3, 5, 10, 20]`. |
| `supabase.url` / `anonKey` | Opcional — só para contas na nuvem (seção 3). |

Depois gere o site (o QR code de doação é gerado automaticamente a partir do `paypalMe`; requer `pip install qrcode`):

```bash
python3 build.py      # cria dist/index.html
```

## 2. Publicar (grátis)

**Opção A — Netlify Drop (mais simples):** abra https://app.netlify.com/drop e arraste a pasta `dist/`. Você recebe um endereço `https://…netlify.app` na hora. Pode ligar um domínio próprio depois.

**Opção B — GitHub Pages:** crie um repositório, envie `dist/index.html` para a raiz, e em *Settings → Pages* escolha a branch `main`.

**Opção C — Cloudflare Pages / Vercel / seu servidor:** qualquer hospedagem de arquivos estáticos funciona.

## 3. Ativar contas de usuário (opcional)

Sem configurar nada, o site já funciona: o progresso fica salvo no navegador de cada pessoa, e há um "código de transferência" para levar o progresso a outro aparelho. Para contas de verdade (login por e-mail, sincronização entre aparelhos e painel de administração):

1. Crie um projeto gratuito em https://supabase.com.
2. *SQL Editor* → cole `supabase/schema.sql` → **Run**.
3. *Authentication → URL Configuration*: em **Site URL** e **Redirect URLs** coloque o endereço do seu site (ex.: `https://parcours-citoyen.netlify.app`).
4. *Project Settings → API*: copie **Project URL** e a chave **anon public** para `src/config.js`, rode `python3 build.py` e publique de novo.
5. Entre no site com seu e-mail (aba *Minha conta*), depois rode no SQL Editor:
   ```sql
   insert into public.admins (user_id) select id from auth.users where email = 'SEU@EMAIL';
   ```
   Recarregue o site: aparece a aba **Admin**, com número de usuários, ativos na semana, progresso médio, idiomas e a lista (apelido, dias concluídos, melhor simulado, última atividade).

**Como funciona o login:** sem senha. A pessoa digita o e-mail e recebe um link mágico. Nome/apelido e datas são opcionais. O botão "Apagar minha conta" remove tudo (RGPD). A chave *anon* pode ficar pública: a segurança vem das políticas do `schema.sql` (cada usuário só lê e altera a própria linha; só admins leem todas).

> O envio de e-mails do plano gratuito do Supabase é limitado (poucos por hora). Se o site crescer, configure um SMTP próprio em *Authentication → Emails* (ex.: Resend, Brevo).

## 4. Doações

A doação não exige conta no site: o botão abre o PayPal, que cuida do pagamento e do recibo. O dinheiro cai direto na sua conta PayPal. Para doações recorrentes ou recibos fiscais, use um botão "Doar" oficial do PayPal (campo `hostedButtonId`).

## 5. Atualizar o conteúdo

| Arquivo | Conteúdo |
|---|---|
| `src/mods.pt.js`, `mods.en.js`, `mods.fr.js` | Texto dos 23 módulos + armadilhas, em cada idioma |
| `src/deep.pt.js`, `deep.en.js`, `deep.fr.js` | Blocos "Aprofundar" (contexto, casos, raciocínio) |
| `src/bank.js`, `src/bank2.js` | Banco de questões (pergunta em francês + explicação PT/EN/FR). Formato: `[módulo, pergunta, [certa, errada, errada, errada], explicação PT, EN, FR]` — a primeira opção é sempre a certa; o site embaralha. Acrescente `"s"` no fim da linha para marcar uma situação prática. |
| `src/shared.js` | Vocabulário, perguntas de entrevista com respostas-modelo, departamentos, frases de apoio |
| `src/ui.js` | Textos da interface nos 3 idiomas |

Depois de editar: `python3 build.py` e publique `dist/` de novo. Pontos a revisar periodicamente: nome do Primeiro-Ministro (o site pede para verificar), regras do exame (service-public.gouv.fr), novas entradas no Panthéon.

## 6. Aviso legal

O site se apresenta como **independente e não oficial** (rodapé em todas as páginas). Não use o logotipo da República Francesa nem do Ministério do Interior.
