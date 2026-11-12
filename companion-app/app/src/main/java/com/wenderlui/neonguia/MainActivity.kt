package com.wenderlui.neonguia

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Checklist
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Map
import androidx.compose.material.icons.filled.MenuBook
import androidx.compose.material3.Icon
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.NavigationBarItemDefaults
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.wenderlui.neonguia.ui.AboutScreen
import com.wenderlui.neonguia.ui.ChecklistScreen
import com.wenderlui.neonguia.ui.GuidesScreen
import com.wenderlui.neonguia.ui.HomeScreen
import com.wenderlui.neonguia.ui.MapScreen
import com.wenderlui.neonguia.ui.Neon
import com.wenderlui.neonguia.ui.NeonTheme

private data class Tab(val label: String, val icon: ImageVector)

private val tabs = listOf(
    Tab("Início", Icons.Filled.Home),
    Tab("Progresso", Icons.Filled.Checklist),
    Tab("Guias", Icons.Filled.MenuBook),
    Tab("Mapa", Icons.Filled.Map),
    Tab("Sobre", Icons.Filled.Info),
)

class MainActivity : ComponentActivity() {
    private val vm: AppViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent { NeonTheme { App(vm) } }
    }
}

@Composable
private fun App(vm: AppViewModel) {
    val state by vm.state.collectAsStateWithLifecycle()
    var tab by rememberSaveable { mutableIntStateOf(0) }

    Scaffold(
        containerColor = Neon.Bg,
        bottomBar = {
            NavigationBar(containerColor = Neon.Surface) {
                tabs.forEachIndexed { i, t ->
                    NavigationBarItem(
                        selected = tab == i,
                        onClick = { tab = i },
                        icon = { Icon(t.icon, contentDescription = t.label) },
                        label = { Text(t.label) },
                        colors = NavigationBarItemDefaults.colors(
                            selectedIconColor = Neon.Pink,
                            selectedTextColor = Neon.Pink,
                            indicatorColor = Neon.SurfaceHigh,
                            unselectedIconColor = Neon.Muted,
                            unselectedTextColor = Neon.Muted,
                        ),
                    )
                }
            }
        },
    ) { padding ->
        Box(Modifier.padding(padding)) {
            when (tab) {
                0 -> HomeScreen(state, onRefresh = vm::refresh)
                1 -> ChecklistScreen(state, onToggle = vm::toggleChecked, onReset = vm::resetChecklist)
                2 -> GuidesScreen(state, onToggleFavorite = vm::toggleFavorite)
                3 -> MapScreen(state, onAdd = vm::addPin, onRemove = vm::removePin)
                else -> AboutScreen(state, onNotes = vm::setNotes)
            }
        }
    }
}
