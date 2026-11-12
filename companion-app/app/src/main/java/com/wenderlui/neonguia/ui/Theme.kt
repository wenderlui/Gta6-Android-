package com.wenderlui.neonguia.ui

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

object Neon {
    val Pink = Color(0xFFFF4FA3)
    val Cyan = Color(0xFF2DE2E6)
    val Orange = Color(0xFFFFB347)
    val Violet = Color(0xFF9D6BFF)
    val Bg = Color(0xFF0E0A1A)
    val Surface = Color(0xFF1A1230)
    val SurfaceHigh = Color(0xFF261A45)
    val Text = Color(0xFFF3ECFF)
    val Muted = Color(0xFFB4A8CF)
    val PinColors = listOf(Pink, Cyan, Orange, Violet, Color(0xFF6BFF8E))
}

private val scheme = darkColorScheme(
    primary = Neon.Pink,
    onPrimary = Color(0xFF2A0016),
    secondary = Neon.Cyan,
    onSecondary = Color(0xFF00282A),
    tertiary = Neon.Orange,
    background = Neon.Bg,
    onBackground = Neon.Text,
    surface = Neon.Surface,
    onSurface = Neon.Text,
    surfaceVariant = Neon.SurfaceHigh,
    onSurfaceVariant = Neon.Muted,
    surfaceContainer = Neon.Surface,
    surfaceContainerHigh = Neon.SurfaceHigh,
    outline = Color(0xFF5A4A80),
)

@Composable
fun NeonTheme(content: @Composable () -> Unit) {
    MaterialTheme(colorScheme = scheme, content = content)
}
