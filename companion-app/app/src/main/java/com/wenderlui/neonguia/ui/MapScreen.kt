package com.wenderlui.neonguia.ui

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.unit.dp
import com.wenderlui.neonguia.UiState

/** Mapa de anotações: arte original e estilizada; o usuário marca seus próprios pontos. */
@Composable
fun MapScreen(state: UiState, onAdd: (Float, Float, String, Int) -> Unit, onRemove: (Long) -> Unit) {
    var pending by remember { mutableStateOf<Offset?>(null) }

    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(10.dp),
    ) {
        item {
            SectionTitle("Meu mapa")
            Text(
                "Toque no mapa para marcar esconderijos, colecionáveis ou pontos de encontro.",
                color = Neon.Muted,
                style = MaterialTheme.typography.bodyMedium,
            )
            Spacer(Modifier.size(8.dp))
            Box(
                Modifier
                    .fillMaxWidth()
                    .aspectRatio(0.85f)
                    .clip(RoundedCornerShape(20.dp))
                    .border(1.dp, Neon.Violet.copy(alpha = 0.5f), RoundedCornerShape(20.dp)),
            ) {
                Canvas(
                    Modifier
                        .fillMaxSize()
                        .pointerInput(Unit) {
                            detectTapGestures { p ->
                                pending = Offset(p.x / size.width, p.y / size.height)
                            }
                        },
                ) {
                    drawStylizedMap()
                    state.pins.forEach { pin ->
                        val c = Neon.PinColors[pin.color.mod(Neon.PinColors.size)]
                        val center = Offset(pin.x * size.width, pin.y * size.height)
                        drawCircle(c.copy(alpha = 0.3f), radius = 18f, center = center)
                        drawCircle(c, radius = 9f, center = center)
                        drawCircle(Color.White, radius = 3.5f, center = center)
                    }
                }
            }
        }
        if (state.pins.isNotEmpty()) item { SectionTitle("Marcadores (${state.pins.size})") }
        items(state.pins.asReversed(), key = { it.id }) { pin ->
            NeonCard {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Box(
                        Modifier
                            .size(14.dp)
                            .clip(CircleShape)
                            .background(Neon.PinColors[pin.color.mod(Neon.PinColors.size)]),
                    )
                    Spacer(Modifier.width(12.dp))
                    Text(pin.label, modifier = Modifier.weight(1f))
                    IconButton(onClick = { onRemove(pin.id) }) {
                        Icon(Icons.Filled.Delete, contentDescription = "Remover marcador", tint = Neon.Muted)
                    }
                }
            }
        }
    }

    pending?.let { point ->
        AddPinDialog(
            onDismiss = { pending = null },
            onConfirm = { label, color ->
                onAdd(point.x, point.y, label, color)
                pending = null
            },
        )
    }
}

@Composable
private fun AddPinDialog(onDismiss: () -> Unit, onConfirm: (String, Int) -> Unit) {
    var label by remember { mutableStateOf("") }
    var color by remember { mutableIntStateOf(0) }
    AlertDialog(
        onDismissRequest = onDismiss,
        containerColor = Neon.Surface,
        title = { Text("Novo marcador") },
        text = {
            androidx.compose.foundation.layout.Column {
                OutlinedTextField(
                    value = label,
                    onValueChange = { label = it.take(60) },
                    placeholder = { Text("Ex.: garagem secreta") },
                    singleLine = true,
                )
                Spacer(Modifier.size(12.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    Neon.PinColors.forEachIndexed { i, c ->
                        Box(
                            Modifier
                                .size(32.dp)
                                .clip(CircleShape)
                                .background(c)
                                .border(if (color == i) 3.dp else 0.dp, Color.White, CircleShape)
                                .clickable { color = i },
                        )
                    }
                }
            }
        },
        confirmButton = {
            TextButton(onClick = { onConfirm(label.ifBlank { "Marcador" }, color) }) { Text("Salvar") }
        },
        dismissButton = { TextButton(onClick = onDismiss) { Text("Cancelar") } },
    )
}

/** Desenha uma península tropical fictícia com ilhas e avenidas — arte 100% original. */
private fun DrawScope.drawStylizedMap() {
    val w = size.width
    val h = size.height
    drawRect(Brush.verticalGradient(listOf(Color(0xFF0B2A4A), Color(0xFF071A33))))

    // grade
    val grid = Color(0x22FFFFFF)
    for (i in 1 until 10) {
        drawLine(grid, Offset(w * i / 10f, 0f), Offset(w * i / 10f, h), 1f)
        drawLine(grid, Offset(0f, h * i / 10f), Offset(w, h * i / 10f), 1f)
    }

    fun p(vararg pts: Float): Path = Path().apply {
        moveTo(pts[0] * w, pts[1] * h)
        var i = 2
        while (i < pts.size) {
            lineTo(pts[i] * w, pts[i + 1] * h); i += 2
        }
        close()
    }

    val land = Color(0xFF2A1F4A)
    val shore = Neon.Cyan.copy(alpha = 0.7f)
    val mainland = p(
        0.05f, 0.02f, 0.80f, 0.02f, 0.86f, 0.18f, 0.78f, 0.30f, 0.84f, 0.46f,
        0.74f, 0.62f, 0.66f, 0.78f, 0.56f, 0.86f, 0.48f, 0.80f, 0.42f, 0.66f,
        0.30f, 0.58f, 0.22f, 0.44f, 0.12f, 0.36f, 0.04f, 0.20f,
    )
    drawPath(mainland, land)
    drawPath(mainland, shore, style = Stroke(3f))

    val islands = listOf(
        p(0.60f, 0.90f, 0.66f, 0.88f, 0.70f, 0.91f, 0.64f, 0.94f),
        p(0.74f, 0.92f, 0.80f, 0.90f, 0.86f, 0.93f, 0.79f, 0.96f),
        p(0.88f, 0.70f, 0.94f, 0.66f, 0.97f, 0.72f, 0.91f, 0.76f),
        p(0.10f, 0.70f, 0.20f, 0.68f, 0.24f, 0.78f, 0.12f, 0.80f),
    )
    islands.forEach {
        drawPath(it, land)
        drawPath(it, shore, style = Stroke(2.5f))
    }

    // lago
    drawOval(Color(0xFF0B2A4A), topLeft = Offset(0.30f * w, 0.18f * h), size = androidx.compose.ui.geometry.Size(0.18f * w, 0.10f * h))

    // avenidas
    val road = Neon.Pink.copy(alpha = 0.75f)
    drawLine(road, Offset(0.12f * w, 0.10f * h), Offset(0.76f * w, 0.42f * h), 4f, StrokeCap.Round)
    drawLine(road, Offset(0.55f * w, 0.05f * h), Offset(0.52f * w, 0.80f * h), 4f, StrokeCap.Round)
    drawLine(road, Offset(0.25f * w, 0.48f * h), Offset(0.80f * w, 0.20f * h), 3f, StrokeCap.Round)
    drawLine(Neon.Orange.copy(alpha = 0.7f), Offset(0.56f * w, 0.86f * h), Offset(0.88f * w, 0.93f * h), 3f, StrokeCap.Round)
}
