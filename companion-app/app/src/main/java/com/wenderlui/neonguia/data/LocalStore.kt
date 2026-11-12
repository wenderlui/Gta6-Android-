package com.wenderlui.neonguia.data

import android.content.Context
import kotlinx.serialization.builtins.ListSerializer
import kotlinx.serialization.json.Json

/** Progresso, marcadores e anotações ficam apenas no aparelho (SharedPreferences). */
class LocalStore(context: Context) {
    private val prefs = context.getSharedPreferences("neonguia", Context.MODE_PRIVATE)
    private val json = Json { ignoreUnknownKeys = true }

    fun checked(): Set<String> = prefs.getStringSet(KEY_CHECKED, emptySet())!!.toSet()
    fun setChecked(value: Set<String>) = prefs.edit().putStringSet(KEY_CHECKED, value).apply()

    fun favorites(): Set<String> = prefs.getStringSet(KEY_FAV, emptySet())!!.toSet()
    fun setFavorites(value: Set<String>) = prefs.edit().putStringSet(KEY_FAV, value).apply()

    fun pins(): List<MapPin> = runCatching {
        json.decodeFromString(ListSerializer(MapPin.serializer()), prefs.getString(KEY_PINS, "[]")!!)
    }.getOrDefault(emptyList())

    fun setPins(value: List<MapPin>) =
        prefs.edit().putString(KEY_PINS, json.encodeToString(ListSerializer(MapPin.serializer()), value)).apply()

    fun notes(): String = prefs.getString(KEY_NOTES, "")!!
    fun setNotes(value: String) = prefs.edit().putString(KEY_NOTES, value).apply()

    private companion object {
        const val KEY_CHECKED = "checked"
        const val KEY_FAV = "favorites"
        const val KEY_PINS = "pins"
        const val KEY_NOTES = "notes"
    }
}
