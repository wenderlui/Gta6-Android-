package com.wenderlui.neonshore

import android.app.WallpaperManager
import android.os.Bundle
import android.view.View
import android.widget.ImageView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.updatePadding
import java.util.concurrent.Executors

class WallpaperActivity : AppCompatActivity() {

    private val io = Executors.newSingleThreadExecutor()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        WindowCompat.setDecorFitsSystemWindows(window, false)
        setContentView(R.layout.activity_wallpaper)

        val index = intent.getIntExtra(EXTRA_INDEX, 0).coerceIn(0, Catalog.wallpapers.lastIndex)
        val wallpaper = Catalog.wallpapers[index]
        title = wallpaper.title
        findViewById<ImageView>(R.id.preview).setImageResource(wallpaper.full)

        val actions = findViewById<View>(R.id.actions)
        ViewCompat.setOnApplyWindowInsetsListener(actions) { v, insets ->
            val bars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.updatePadding(bottom = bars.bottom + 16)
            insets
        }

        findViewById<View>(R.id.setHome).setOnClickListener { apply(wallpaper, WallpaperManager.FLAG_SYSTEM) }
        findViewById<View>(R.id.setLock).setOnClickListener { apply(wallpaper, WallpaperManager.FLAG_LOCK) }
        findViewById<View>(R.id.setBoth).setOnClickListener {
            apply(wallpaper, WallpaperManager.FLAG_SYSTEM or WallpaperManager.FLAG_LOCK)
        }
    }

    private fun apply(wallpaper: Wallpaper, which: Int) {
        val progress = findViewById<View>(R.id.progress)
        progress.visibility = View.VISIBLE
        Toast.makeText(this, R.string.wallpaper_applying, Toast.LENGTH_SHORT).show()
        val appContext = applicationContext
        io.execute {
            val ok = runCatching {
                resources.openRawResource(wallpaper.full).use { stream ->
                    WallpaperManager.getInstance(appContext).setStream(stream, null, true, which)
                }
            }.isSuccess
            runOnUiThread {
                if (isDestroyed) return@runOnUiThread
                progress.visibility = View.GONE
                Toast.makeText(
                    this,
                    if (ok) R.string.wallpaper_done else R.string.wallpaper_error,
                    Toast.LENGTH_SHORT,
                ).show()
            }
        }
    }

    override fun onDestroy() {
        io.shutdown()
        super.onDestroy()
    }

    companion object {
        const val EXTRA_INDEX = "index"
    }
}
