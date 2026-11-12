package com.wenderlui.neonguia.ui

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ExpandLess
import androidx.compose.material.icons.filled.ExpandMore
import androidx.compose.material3.Checkbox
import androidx.compose.material3.CheckboxDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.unit.dp
import com.wenderlui.neonguia.UiState
import com.wenderlui.neonguia.data.Checklist

@Composable
fun ChecklistScreen(state: UiState, onToggle: (String) -> Unit, onReset: (List<String>) -> Unit) {
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        item {
            SectionTitle("Progresso")
            Text(
                "Marque o que você já fez. Tudo fica salvo só no seu aparelho.",
                color = Neon.Muted,
                style = MaterialTheme.typography.bodyMedium,
            )
        }
        if (state.content.checklists.isEmpty() && !state.loading) {
            item { NeonCard { Text("Nenhuma lista disponível ainda. Toque em atualizar na tela inicial.") } }
        }
        items(state.content.checklists, key = { it.id }) { list ->
            ChecklistCard(list, state.checked, onToggle, onReset)
        }
    }
}

@Composable
private fun ChecklistCard(
    list: Checklist,
    checked: Set<String>,
    onToggle: (String) -> Unit,
    onReset: (List<String>) -> Unit,
) {
    var open by rememberSaveable(list.id) { mutableStateOf(false) }
    val done = list.items.count { it.id in checked }
    NeonCard {
        Row(
            Modifier.fillMaxWidth().clickable { open = !open },
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Column(Modifier.weight(1f)) {
                Text(list.title, fontWeight = FontWeight.Bold, style = MaterialTheme.typography.titleMedium)
                Text("$done/${list.items.size}", color = Neon.Cyan, style = MaterialTheme.typography.labelMedium)
            }
            Icon(
                if (open) Icons.Filled.ExpandLess else Icons.Filled.ExpandMore,
                contentDescription = if (open) "Recolher" else "Expandir",
                tint = Neon.Muted,
            )
        }
        Spacer(Modifier.height(8.dp))
        LinearProgressIndicator(
            progress = { if (list.items.isEmpty()) 0f else done.toFloat() / list.items.size },
            modifier = Modifier.fillMaxWidth().height(6.dp).clip(RoundedCornerShape(3.dp)),
            color = Neon.Pink,
            trackColor = Neon.SurfaceHigh,
            drawStopIndicator = {},
            gapSize = 0.dp,
        )
        if (open) {
            list.items.forEach { item ->
                val isDone = item.id in checked
                Row(
                    Modifier.fillMaxWidth().clickable { onToggle(item.id) },
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Checkbox(
                        checked = isDone,
                        onCheckedChange = { onToggle(item.id) },
                        colors = CheckboxDefaults.colors(checkedColor = Neon.Pink, uncheckedColor = Neon.Muted),
                    )
                    Column(Modifier.weight(1f)) {
                        Text(
                            item.title,
                            textDecoration = if (isDone) TextDecoration.LineThrough else null,
                            color = if (isDone) Neon.Muted else Neon.Text,
                        )
                        item.note?.let { Text(it, color = Neon.Muted, style = MaterialTheme.typography.bodySmall) }
                    }
                }
            }
            if (done > 0) {
                TextButton(onClick = { onReset(list.items.map { it.id }) }) { Text("Desmarcar tudo") }
            }
        }
    }
}
