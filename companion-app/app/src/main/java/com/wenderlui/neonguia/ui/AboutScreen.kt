package com.wenderlui.neonguia.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalUriHandler
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.wenderlui.neonguia.UiState

const val PRIVACY_URL = "https://wenderlui.github.io/Gta6-Android-/privacidade.html"

@Composable
fun AboutScreen(state: UiState, onNotes: (String) -> Unit) {
    val uri = LocalUriHandler.current
    val ctx = LocalContext.current
    val version = runCatching { ctx.packageManager.getPackageInfo(ctx.packageName, 0).versionName }.getOrNull() ?: ""

    Column(
        Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        SectionTitle("Bloco de notas")
        OutlinedTextField(
            value = state.notes,
            onValueChange = onNotes,
            placeholder = { Text("Anote placas, senhas de cofres, rotas…") },
            modifier = Modifier.fillMaxWidth().heightIn(min = 160.dp),
        )

        SectionTitle("Sobre")
        NeonCard {
            Text("NeonGuia $version", fontWeight = FontWeight.Bold)
            Spacer(Modifier.size(6.dp))
            Text(
                "App de fã, gratuito e NÃO OFICIAL. Não é afiliado, patrocinado nem aprovado por " +
                    "nenhuma desenvolvedora ou publicadora de jogos. Todas as marcas citadas pertencem " +
                    "aos seus respectivos donos. Mapa, ícones e textos são criações originais.",
                color = Neon.Muted,
                style = MaterialTheme.typography.bodyMedium,
            )
        }
        NeonCard {
            Text("Privacidade", fontWeight = FontWeight.Bold)
            Spacer(Modifier.size(6.dp))
            Text(
                "Não coletamos dados pessoais. Seu progresso, marcadores e notas ficam somente no seu " +
                    "aparelho. O app apenas baixa o arquivo público de conteúdo (guias e novidades).",
                color = Neon.Muted,
                style = MaterialTheme.typography.bodyMedium,
            )
            TextButton(onClick = { runCatching { uri.openUri(PRIVACY_URL) } }) { Text("Política de privacidade") }
        }
    }
}
