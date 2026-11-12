package com.wenderlui.neonshore

import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.updatePadding
import androidx.recyclerview.widget.GridLayoutManager
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        WindowCompat.setDecorFitsSystemWindows(window, false)
        setContentView(R.layout.activity_main)

        val root = findViewById<View>(R.id.root)
        ViewCompat.setOnApplyWindowInsetsListener(root) { v, insets ->
            val bars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.updatePadding(left = bars.left, right = bars.right, bottom = bars.bottom)
            insets
        }

        findViewById<View>(R.id.applyIcons).setOnClickListener { Launchers.showChooser(this) }

        findViewById<RecyclerView>(R.id.wallpapers).apply {
            layoutManager = LinearLayoutManager(context, LinearLayoutManager.HORIZONTAL, false)
            adapter = WallpaperAdapter(Catalog.wallpapers) { index ->
                startActivity(
                    Intent(this@MainActivity, WallpaperActivity::class.java)
                        .putExtra(WallpaperActivity.EXTRA_INDEX, index)
                )
            }
        }

        findViewById<TextView>(R.id.iconsTitle).text = getString(R.string.section_icons, Catalog.icons.size)
        findViewById<RecyclerView>(R.id.icons).apply {
            layoutManager = GridLayoutManager(context, 4)
            adapter = IconAdapter(Catalog.icons)
        }
    }
}

private class WallpaperAdapter(
    private val items: List<Wallpaper>,
    private val onClick: (Int) -> Unit,
) : RecyclerView.Adapter<WallpaperAdapter.VH>() {

    class VH(view: View) : RecyclerView.ViewHolder(view) {
        val thumb: ImageView = view.findViewById(R.id.thumb)
        val title: TextView = view.findViewById(R.id.title)
        val card: View = view.findViewById(R.id.card)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int) =
        VH(LayoutInflater.from(parent.context).inflate(R.layout.item_wallpaper, parent, false))

    override fun getItemCount() = items.size

    override fun onBindViewHolder(holder: VH, position: Int) {
        val item = items[position]
        holder.thumb.setImageResource(item.thumb)
        holder.title.text = item.title
        holder.card.contentDescription = item.title
        holder.card.setOnClickListener { onClick(holder.bindingAdapterPosition) }
    }
}

private class IconAdapter(private val icons: IntArray) : RecyclerView.Adapter<IconAdapter.VH>() {
    class VH(view: View) : RecyclerView.ViewHolder(view) {
        val icon: ImageView = view as ImageView
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int) =
        VH(LayoutInflater.from(parent.context).inflate(R.layout.item_icon, parent, false))

    override fun getItemCount() = icons.size

    override fun onBindViewHolder(holder: VH, position: Int) {
        holder.icon.setImageResource(icons[position])
    }
}
