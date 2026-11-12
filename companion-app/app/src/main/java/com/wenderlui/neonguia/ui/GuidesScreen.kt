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
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ContentCopy
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Star
import androidx.compose.material.icons.filled.StarBorder
import androidx.compose.material3.FilterChip
import androidx.compose.material3.FilterChipDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.SecondaryTabRow
import androidx.compose.material3.Tab
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.wenderlui.neonguia.UiState

@Composable
fun GuidesScreen(state: UiState, onToggleFavorite: (String) -> Unit) {
    var tab by rememberSaveable { mutableIntStateOf(0) }
    var query by rememberSaveable { mutableStateOf("") }
    var category by rememberSaveable { mutableStateOf<String?>(null) }
    var expanded by rememberSaveable { mutableStateOf<String?>(null) }
    @Suppress("DEPRECATION")
    val clipboard = LocalClipboardManager.current
    val q = query.trim().lowercase()

    Column(Modifier.fillMaxSize()) {
        SecondaryTabRow(selectedTabIndex = tab, containerColor = Neon.Bg, contentColor = Neon.Pink) {
            listOf("Guias", "Códigos", "Favoritos").forEachIndexed { i, label ->
                Tab(selected = tab == i, onClick = { tab = i }, text = { Text(label) })
            }
        }
        OutlinedTextField(
            value = query,
            onValueChange = { query = it },
            leadingIcon = { Icon(Icons.Filled.Search, contentDescription = null) },
            placeholder = { Text("Buscar") },
            singleLine = true,
            modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp),
        )

        val guides = state.content.guides.filter {
            (q.isEmpty() || it.title.lowercase().contains(q) || it.body.lowercase().contains(q)) &&
                (tab != 2 || it.id in state.favorites)
        }
        val codes = state.content.codes.filter {
            (q.isEmpty() || it.effect.lowercase().contains(q) || it.code.lowercase().contains(q)) &&
                (tab != 2 || it.id in state.favorites)
        }

        if (tab == 0) {
            val categories = state.content.guides.map { it.category }.distinct()
            LazyRow(
                contentPadding = PaddingValues(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                item {
                    FilterChip(category == null, onClick = { category = null }, label = { Text("Todos") }, colors = chipColors())
                }
                items(categories) { c ->
                    FilterChip(category == c, onClick = { category = if (category == c) null else c }, label = { Text(c) }, colors = chipColors())
                }
            }
        }

        LazyColumn(
            modifier = Modifier.fillMaxSize(),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            if (tab != 1) {
                items(guides.filter { tab != 0 || category == null || it.category == category }, key = { "g-" + it.id }) { g ->
                    NeonCard(Modifier.clickable { expanded = if (expanded == g.id) null else g.id }) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Column(Modifier.weight(1f)) {
                                Text(g.category.uppercase(), color = Neon.Cyan, style = MaterialTheme.typography.labelSmall)
                                Text(g.title, fontWeight = FontWeight.Bold, style = MaterialTheme.typography.titleMedium)
                            }
                            FavButton(g.id in state.favorites) { onToggleFavorite(g.id) }
                        }
                        if (expanded == g.id) {
                            Spacer(Modifier.height(8.dp))
                            Text(g.body, color = Neon.Muted, style = MaterialTheme.typography.bodyMedium)
                        }
                    }
                }
            }
            if (tab != 0) {
                items(codes, key = { "c-" + it.id }) { c ->
                    NeonCard {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Column(Modifier.weight(1f)) {
                                Text(c.platform.uppercase(), color = Neon.Orange, style = MaterialTheme.typography.labelSmall)
                                Text(c.effect, fontWeight = FontWeight.Bold)
                                Text(c.code, fontFamily = FontFamily.Monospace, color = Neon.Cyan)
                            }
                            IconButton(onClick = { clipboard.setText(AnnotatedString(c.code)) }) {
                                Icon(Icons.Filled.ContentCopy, contentDescription = "Copiar código", tint = Neon.Muted)
                            }
                            FavButton(c.id in state.favorites) { onToggleFavorite(c.id) }
                        }
                    }
                }
            }
            if ((tab == 0 && guides.isEmpty()) || (tab == 1 && codes.isEmpty()) || (tab == 2 && guides.isEmpty() && codes.isEmpty())) {
                item {
                    Text(
                        when {
                            tab == 2 -> "Toque na estrela de um guia ou código para salvá-lo aqui."
                            tab == 1 && q.isEmpty() -> "Os códigos serão publicados aqui assim que forem descobertos após o lançamento."
                            else -> "Nada encontrado."
                        },
                        color = Neon.Muted,
                    )
                }
            }
        }
    }
}

@Composable
private fun FavButton(active: Boolean, onClick: () -> Unit) {
    IconButton(onClick = onClick) {
        Icon(
            if (active) Icons.Filled.Star else Icons.Filled.StarBorder,
            contentDescription = if (active) "Remover dos favoritos" else "Adicionar aos favoritos",
            tint = if (active) Neon.Orange else Neon.Muted,
        )
    }
}

@Composable
private fun chipColors() = FilterChipDefaults.filterChipColors(
    selectedContainerColor = Neon.Pink,
    selectedLabelColor = Neon.Bg,
    labelColor = Neon.Muted,
)
