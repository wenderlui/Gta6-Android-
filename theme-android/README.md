# Neon Shore — tema Android (ícones + wallpapers)

Pacote de ícones neon e wallpapers retrô no estilo "cidade tropical à noite". Toda a arte é original e gerada por código
(`tools/`), sem logotipos, nomes ou elementos de jogos de terceiros.

- **Pacote:** `com.wenderlui.neonshore` · minSdk 26 · targetSdk 36
- **Conteúdo:** 38 ícones (87 apps mapeados em `appfilter.xml`), fundo automático para apps sem ícone, 8 wallpapers 1440×3200
- **Launchers:** Nova, Lawnchair, Smart Launcher, Niagara, Action, Apex, Hyperion, Microsoft, POCO
- **Sem internet, sem anúncios, sem coleta de dados**

## Gerar o AAB
O GitHub Actions (`.github/workflows/theme-android.yml`) gera o AAB de release e um APK de teste a cada push.
Com os segredos `NEON_KEYSTORE_BASE64`, `NEON_KEYSTORE_PASSWORD`, `NEON_KEY_ALIAS` e `NEON_KEY_PASSWORD` configurados,
o AAB já sai assinado com a chave de upload. O `versionCode` é o número da execução do workflow.

Localmente (Android SDK instalado):
```bash
cd theme-android
# crie keystore.properties com storeFile, storePassword, keyAlias, keyPassword (não versionado)
./gradlew bundleRelease   # app/build/outputs/bundle/release/app-release.aab
```

## Regerar a arte
```bash
cd theme-android/tools
python3 icons.py && python3 wallpapers.py && python3 branding.py && python3 catalog.py
```
Para adicionar um ícone: crie uma função `g_<nome>` em `icons.py`, registre em `ICONS` com a cor e os componentes
(`pacote/atividade`) e rode os scripts.

## Publicação
- Ficha da loja em português: `store/listing-pt-BR.md`
- Respostas do Play Console (classificação, segurança dos dados, público): `store/play-console-respostas.md`
- Política de privacidade: `store/privacy-policy.html` (publique numa URL pública, ex.: GitHub Pages ou Google Sites)
- Ícone, gráfico de recursos e capturas: `store/graphics/`
