// Arquivo gerado por tools/catalog.py — não edite à mão.
package com.wenderlui.neonshore

object Catalog {
    val icons = intArrayOf(
        R.drawable.ic_phone,
        R.drawable.ic_messages,
        R.drawable.ic_whatsapp,
        R.drawable.ic_camera,
        R.drawable.ic_instagram,
        R.drawable.ic_gallery,
        R.drawable.ic_spotify,
        R.drawable.ic_music,
        R.drawable.ic_youtube,
        R.drawable.ic_playstore,
        R.drawable.ic_browser,
        R.drawable.ic_mail,
        R.drawable.ic_maps,
        R.drawable.ic_settings,
        R.drawable.ic_clock,
        R.drawable.ic_calculator,
        R.drawable.ic_calendar,
        R.drawable.ic_contacts,
        R.drawable.ic_facebook,
        R.drawable.ic_x,
        R.drawable.ic_tiktok,
        R.drawable.ic_netflix,
        R.drawable.ic_telegram,
        R.drawable.ic_files,
        R.drawable.ic_notes,
        R.drawable.ic_google,
        R.drawable.ic_drive,
        R.drawable.ic_cloud,
        R.drawable.ic_wallet,
        R.drawable.ic_bank,
        R.drawable.ic_car,
        R.drawable.ic_games,
        R.drawable.ic_weather,
        R.drawable.ic_recorder,
        R.drawable.ic_meet,
        R.drawable.ic_shop,
        R.drawable.ic_food,
        R.drawable.ic_disc,
    )

    val wallpapers = listOf(
        Wallpaper(R.drawable.wall_sunset_shore, R.drawable.wall_sunset_shore_thumb, "Pôr do sol na orla"),
        Wallpaper(R.drawable.wall_neon_grid, R.drawable.wall_neon_grid_thumb, "Grade neon"),
        Wallpaper(R.drawable.wall_skyline, R.drawable.wall_skyline_thumb, "Cidade ao entardecer"),
        Wallpaper(R.drawable.wall_palm_night, R.drawable.wall_palm_night_thumb, "Noite de palmeiras"),
        Wallpaper(R.drawable.wall_highway, R.drawable.wall_highway_thumb, "Estrada infinita"),
        Wallpaper(R.drawable.wall_waves, R.drawable.wall_waves_thumb, "Ondas pastel"),
        Wallpaper(R.drawable.wall_neon_sign, R.drawable.wall_neon_sign_thumb, "Letreiro neon"),
        Wallpaper(R.drawable.wall_pastel_shore, R.drawable.wall_pastel_shore_thumb, "Calçadão"),
    )
}

data class Wallpaper(val full: Int, val thumb: Int, val title: String)
