package com.wenderlui.neonguia

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.wenderlui.neonguia.data.Content
import com.wenderlui.neonguia.data.ContentRepository
import com.wenderlui.neonguia.data.LocalStore
import com.wenderlui.neonguia.data.MapPin
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

data class UiState(
    val content: Content = Content(),
    val loading: Boolean = true,
    val refreshing: Boolean = false,
    val offline: Boolean = false,
    val checked: Set<String> = emptySet(),
    val favorites: Set<String> = emptySet(),
    val pins: List<MapPin> = emptyList(),
    val notes: String = "",
)

class AppViewModel(app: Application) : AndroidViewModel(app) {
    private val repo = ContentRepository(app)
    private val store = LocalStore(app)

    private val _state = MutableStateFlow(
        UiState(
            checked = store.checked(),
            favorites = store.favorites(),
            pins = store.pins(),
            notes = store.notes(),
        )
    )
    val state: StateFlow<UiState> = _state.asStateFlow()

    init {
        viewModelScope.launch {
            val local = repo.load()
            _state.update { it.copy(content = local, loading = false) }
            refresh()
        }
    }

    fun refresh() {
        if (_state.value.refreshing) return
        viewModelScope.launch {
            _state.update { it.copy(refreshing = true) }
            val fresh = repo.refresh()
            _state.update {
                it.copy(
                    content = fresh ?: it.content,
                    refreshing = false,
                    offline = fresh == null,
                )
            }
        }
    }

    fun toggleChecked(id: String) {
        val next = _state.value.checked.let { if (id in it) it - id else it + id }
        store.setChecked(next)
        _state.update { it.copy(checked = next) }
    }

    fun resetChecklist(ids: List<String>) {
        val next = _state.value.checked - ids.toSet()
        store.setChecked(next)
        _state.update { it.copy(checked = next) }
    }

    fun toggleFavorite(id: String) {
        val next = _state.value.favorites.let { if (id in it) it - id else it + id }
        store.setFavorites(next)
        _state.update { it.copy(favorites = next) }
    }

    fun addPin(x: Float, y: Float, label: String, color: Int) {
        val next = _state.value.pins + MapPin(System.currentTimeMillis(), x, y, label, color)
        store.setPins(next)
        _state.update { it.copy(pins = next) }
    }

    fun removePin(id: Long) {
        val next = _state.value.pins.filterNot { it.id == id }
        store.setPins(next)
        _state.update { it.copy(pins = next) }
    }

    fun setNotes(text: String) {
        store.setNotes(text)
        _state.update { it.copy(notes = text) }
    }
}
