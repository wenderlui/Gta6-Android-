# NeonGuia — tudo para publicar na Play Store

Pacote: `com.wenderlui.neonguia` · Versão 1.0.0 · targetSdk 36 · minSdk 26 (Android 8+)

## 1. Antes de tudo: prazo da conta (leia!)
- **Conta pessoal criada depois de 13/11/2023:** o Google exige **teste fechado com pelo menos 12 testadores por 14 dias seguidos** antes de liberar a produção. Se for o seu caso, o app **não estará público em 19/11**. Comece o teste fechado hoje; o app pode ir para produção ~26/11 + análise.
- **Conta de organização ou conta antiga:** pode enviar direto para produção (análise costuma levar de 1 a 7 dias para apps novos). Envie o quanto antes.

## 2. Marca registrada (evita rejeição)
- Não use "GTA", "Grand Theft Auto", "Rockstar", "Vice City" ou "Leonida" no nome, descrição, ícone ou capturas. O Google rejeita/remove apps por violação de propriedade intelectual e "personificação".
- O app já é 100% original (nome, ícone, mapa estilizado, textos) e tem aviso de "não oficial".

## 3. Ficha da loja (copiar e colar)

**Nome do app (máx. 30):**
NeonGuia: Guia Mundo Aberto

**Descrição curta (máx. 80):**
Contagem, checklists, guias, códigos e mapa de notas para o seu mundo aberto.

**Descrição completa:**
O NeonGuia é o seu companheiro de bolso para o jogo de mundo aberto mais aguardado do ano.

⏱️ CONTAGEM REGRESSIVA
Acompanhe dias, horas, minutos e segundos até o lançamento.

✅ PROGRESSO
Listas de preparação, primeiros passos, exploração e colecionáveis. Marque o que já fez e veja sua porcentagem de conclusão.

📖 GUIAS E CÓDIGOS
Dicas para iniciantes, direção, combate e exploração. Códigos com botão de copiar e favoritos para achar rápido.

🗺️ MEU MAPA
Toque no mapa para criar marcadores com nome e cor: esconderijos, lojas, colecionáveis e pontos de encontro.

📝 BLOCO DE NOTAS
Anote senhas, rotas e placas sem sair do app.

🔄 SEMPRE ATUALIZADO
Novos guias, códigos e listas chegam automaticamente, sem precisar atualizar o app.

🔒 PRIVACIDADE
Sem cadastro, sem anúncios e sem coleta de dados. Tudo fica salvo só no seu aparelho.

AVISO: O NeonGuia é um app de fã, gratuito e não oficial. Não é afiliado, patrocinado nem aprovado por nenhuma desenvolvedora ou publicadora de jogos. Todas as marcas pertencem aos seus respectivos donos.

**Gráficos (nesta pasta):**
- Ícone 512×512: `icone-512.png`
- Gráfico de destaque 1024×500: `grafico-destaque-1024x500.png`
- Capturas de tela do celular: `capturas/` (geradas no emulador pelo GitHub Actions)

**Categoria:** Entretenimento · **Tags:** Guia, Jogos
**E-mail de contato:** o seu e-mail de desenvolvedor
**Site (opcional):** https://github.com/wenderlui/Gta6-Android-

## 4. Conteúdo do app (Painel > Política > Conteúdo do app)

| Seção | Resposta |
|---|---|
| Política de privacidade | https://wenderlui.github.io/Gta6-Android-/privacidade.html |
| Acesso ao app | Toda a funcionalidade está disponível sem restrições (sem login) |
| Anúncios | Não, o app não contém anúncios |
| Classificação de conteúdo (IARC) | Categoria: "Referência, notícias ou educação". Violência/sexo/drogas/apostas: Não. Interação entre usuários: Não. Compartilha localização: Não. Compras digitais: Não. Resultado esperado: Livre |
| Público-alvo | 18 anos ou mais (evita a política de Famílias; o tema é um jogo para adultos) |
| App de notícias | Não |
| Apps governamentais / financeiros / saúde | Não |
| ID de publicidade | Não usa |

### Segurança dos dados (Data Safety)
- O app coleta ou compartilha algum dos tipos de dados obrigatórios? **Não**
- Todos os dados do usuário são criptografados em trânsito? **Sim** (HTTPS) — só aparece se marcar coleta; com "Não" o formulário termina.
- Resultado na loja: "Nenhum dado coletado · Nenhum dado compartilhado".

## 5. Assinatura e envio do AAB
1. Guarde a pasta `../assinatura/` em local seguro (backup em 2 lugares). Ela tem a **chave de upload** e as senhas.
2. No GitHub: Settings > Secrets and variables > Actions > crie os 4 secrets descritos em `assinatura/LEIA-ME-SECRETS.txt`.
3. Em Actions > "App companheiro (build)" > Run workflow (branch main). Baixe o artefato `neonguia-release-aab`.
4. Play Console > Criar app (Nome: NeonGuia, Idioma padrão: Português (Brasil), App, Gratuito).
5. Aceite o **Play App Signing** (padrão). Envie o `.aab` em Teste > Teste fechado (ou Produção, conforme item 1).
6. Notas da versão: "Primeira versão: contagem regressiva, checklists, guias, códigos, mapa de marcadores e bloco de notas."
7. Países: todos (ou Brasil + Portugal). Enviar para análise.

## 6. Depois do lançamento do jogo
Edite `content/content.json` no repositório (aumente `version` em +1) para publicar códigos, colecionáveis e novidades. Os apps instalados pegam a nova versão ao abrir/atualizar, sem passar pela Play Store.

## 7. Ativar a página da política de privacidade
GitHub > Settings > Pages > Source: **GitHub Actions**. Depois rode o workflow "Publicar política de privacidade" (ou ele roda sozinho no merge).
