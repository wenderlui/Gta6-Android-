package com.wenderlui.neonguia.data

import android.content.Context
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.serialization.json.Json
import java.io.File
import java.net.HttpURLConnection
import java.net.URL

/**
 * Carrega o conteúdo do app. Ordem: cache local -> conteúdo embutido (assets).
 * [refresh] baixa a versão mais nova do repositório e atualiza o cache, assim
 * guias, códigos e checklists podem ser atualizados após o lançamento sem nova versão na loja.
 */
class ContentRepository(private val context: Context) {

    private val json = Json { ignoreUnknownKeys = true; isLenient = true }
    private val cacheFile get() = File(context.filesDir, "content.json")

    suspend fun load(): Content = withContext(Dispatchers.IO) {
        val bundled = parse(context.assets.open("content.json").bufferedReader().use { it.readText() })
        val cached = runCatching { if (cacheFile.exists()) parse(cacheFile.readText()) else null }.getOrNull()
        if (cached != null && cached.version >= (bundled?.version ?: 0)) cached else bundled ?: Content()
    }

    /** Retorna o conteúdo novo, ou null se offline/erro. */
    suspend fun refresh(): Content? = withContext(Dispatchers.IO) {
        runCatching {
            val conn = (URL(CONTENT_URL).openConnection() as HttpURLConnection).apply {
                connectTimeout = 8000
                readTimeout = 8000
                useCaches = false
            }
            try {
                if (conn.responseCode != 200) return@runCatching null
                val text = conn.inputStream.bufferedReader().use { it.readText() }
                val parsed = parse(text) ?: return@runCatching null
                cacheFile.writeText(text)
                parsed
            } finally {
                conn.disconnect()
            }
        }.getOrNull()
    }

    private fun parse(text: String): Content? =
        runCatching { json.decodeFromString(Content.serializer(), text) }.getOrNull()

    companion object {
        const val CONTENT_URL =
            "https://raw.githubusercontent.com/wenderlui/Gta6-Android-/main/content/content.json"
    }
}
