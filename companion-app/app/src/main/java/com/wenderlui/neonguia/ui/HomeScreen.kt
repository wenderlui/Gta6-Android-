package com.wenderlui.neonguia.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableLongStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.platform.LocalUriHandler
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.wenderlui.neonguia.UiState
import kotlinx.coroutines.delay
import java.time.LocalDate
import java.time.ZoneId

@Composable
fun HomeScreen(state: UiState, onRefresh: () -> Unit) {
    val uri = LocalUriHandler.current
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        item {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    "NeonGuia",
                    fontSize = 30.sp,
                    fontWeight = FontWeight.Black,
                    color = Neon.Pink,
                    modifier = Modifier.weight(1f),
                )
                if (state.refreshing) {
                    CircularProgressIndicator(Modifier.size(24.dp), color = Neon.Cyan, strokeWidth = 2.dp)
                } else {
                    IconButton(onClick = onRefresh) {
                        Icon(Icons.Filled.Refresh, contentDescription = "Atualizar conteúdo", tint = Neon.Cyan)
                    }
                }
            }
            if (state.offline) {
                Text(
                    "Sem conexão: mostrando o conteúdo salvo no aparelho.",
                    color = Neon.Orange,
                    style = MaterialTheme.typography.bodySmall,
                )
            }
        }
        item { Countdown(state.content.launchDate, state.content.launchTitle) }
        item { ProgressSummary(state) }
        item { SectionTitle("Novidades") }
        items(state.content.news, key = { it.id }) { n ->
            NeonCard {
                if (n.date.isNotBlank()) Text(n.date, color = Neon.Cyan, style = MaterialTheme.typography.labelMedium)
                Text(n.title, fontWeight = FontWeight.Bold, style = MaterialTheme.typography.titleMedium)
                Spacer(Modifier.height(4.dp))
                Text(n.body, color = Neon.Muted, style = MaterialTheme.typography.bodyMedium)
                n.url?.let { link ->
                    TextButton(onClick = { runCatching { uri.openUri(link) } }) { Text("Abrir link") }
                }
            }
        }
    }
}

@Composable
private fun Countdown(launchDate: String, title: String) {
    val target = remember(launchDate) {
        runCatching {
            LocalDate.parse(launchDate).atStartOfDay(ZoneId.systemDefault()).toInstant().toEpochMilli()
        }.getOrNull()
    }
    var now by remember { mutableLongStateOf(System.currentTimeMillis()) }
    LaunchedEffect(Unit) {
        while (true) {
            now = System.currentTimeMillis()
            delay(1000)
        }
    }
    Column(
        Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(22.dp))
            .background(Brush.linearGradient(listOf(Neon.Violet, Neon.Pink, Neon.Orange)))
            .padding(20.dp),
    ) {
        Text(title, color = Neon.Bg, fontWeight = FontWeight.Bold, style = MaterialTheme.typography.titleMedium)
        Spacer(Modifier.height(8.dp))
        if (target == null) {
            Text("Data a confirmar", color = Neon.Bg, fontSize = 28.sp, fontWeight = FontWeight.Black)
            return@Column
        }
        val left = (target - now).coerceAtLeast(0) / 1000
        if (left == 0L) {
            Text("Já disponível!", color = Neon.Bg, fontSize = 32.sp, fontWeight = FontWeight.Black)
        } else {
            Row(horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
                TimeBox(left / 86400, "dias")
                TimeBox(left % 86400 / 3600, "horas")
                TimeBox(left % 3600 / 60, "min")
                TimeBox(left % 60, "seg")
            }
        }
    }
}

@Composable
private fun TimeBox(value: Long, label: String) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Text(value.toString().padStart(2, '0'), color = Neon.Bg, fontSize = 34.sp, fontWeight = FontWeight.Black)
        Text(label, color = Neon.Bg, style = MaterialTheme.typography.labelMedium)
    }
}

@Composable
private fun ProgressSummary(state: UiState) {
    val all = state.content.checklists.flatMap { it.items }
    if (all.isEmpty()) return
    val done = all.count { it.id in state.checked }
    NeonCard {
        Text("Seu progresso", fontWeight = FontWeight.Bold)
        Spacer(Modifier.height(8.dp))
        androidx.compose.material3.LinearProgressIndicator(
            progress = { done.toFloat() / all.size },
            modifier = Modifier.fillMaxWidth().height(8.dp).clip(RoundedCornerShape(4.dp)),
            color = Neon.Cyan,
            trackColor = Neon.SurfaceHigh,
            drawStopIndicator = {},
            gapSize = 0.dp,
        )
        Spacer(Modifier.height(6.dp))
        Text("$done de ${all.size} itens concluídos", color = Neon.Muted, style = MaterialTheme.typography.bodySmall)
    }
}
