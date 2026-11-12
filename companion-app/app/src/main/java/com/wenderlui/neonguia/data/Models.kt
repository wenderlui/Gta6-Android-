package com.wenderlui.neonguia.data

import kotlinx.serialization.Serializable

/** Conteúdo remoto, publicado em content/content.json no repositório. */
@Serializable
data class Content(
    val version: Int = 1,
    val launchDate: String = "2026-11-19",
    val launchTitle: String = "Contagem para o lançamento",
    val news: List<NewsItem> = emptyList(),
    val guides: List<Guide> = emptyList(),
    val codes: List<CodeItem> = emptyList(),
    val checklists: List<Checklist> = emptyList(),
)

@Serializable
data class NewsItem(
    val id: String,
    val title: String,
    val body: String,
    val date: String = "",
    val url: String? = null,
)

@Serializable
data class Guide(
    val id: String,
    val category: String,
    val title: String,
    val body: String,
)

@Serializable
data class CodeItem(
    val id: String,
    val platform: String,
    val code: String,
    val effect: String,
)

@Serializable
data class Checklist(
    val id: String,
    val title: String,
    val items: List<ChecklistItem>,
)

@Serializable
data class ChecklistItem(
    val id: String,
    val title: String,
    val note: String? = null,
)

/** Marcador criado pelo usuário no mapa (coordenadas normalizadas 0..1). */
@Serializable
data class MapPin(
    val id: Long,
    val x: Float,
    val y: Float,
    val label: String,
    val color: Int = 0,
)
