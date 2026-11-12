package com.wenderlui.neonshore

import android.content.ActivityNotFoundException
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.BaseAdapter
import android.widget.TextView
import android.widget.Toast
import androidx.core.content.ContextCompat
import com.google.android.material.dialog.MaterialAlertDialogBuilder

/** Launchers compatíveis e como aplicar o pacote de ícones em cada um. */
object Launchers {

    private enum class Mode { NOVA, SMART, ACTION, APEX, MANUAL }

    private data class Launcher(val name: String, val packages: List<String>, val mode: Mode)

    private val all = listOf(
        Launcher("Nova Launcher", listOf("com.teslacoilsw.launcher"), Mode.NOVA),
        Launcher("Lawnchair", listOf("app.lawnchair", "app.lawnchair.play"), Mode.MANUAL),
        Launcher("Smart Launcher", listOf("ginlemon.flowerfree", "ginlemon.flowerpro"), Mode.SMART),
        Launcher("Niagara Launcher", listOf("bitpit.launcher"), Mode.MANUAL),
        Launcher("Action Launcher", listOf("com.actionlauncher.playstore"), Mode.ACTION),
        Launcher("Apex Launcher", listOf("com.anddoes.launcher"), Mode.APEX),
        Launcher("Hyperion Launcher", listOf("projekt.launcher"), Mode.MANUAL),
        Launcher("Microsoft Launcher", listOf("com.microsoft.launcher"), Mode.MANUAL),
        Launcher("POCO Launcher", listOf("com.mi.android.globallauncher"), Mode.MANUAL),
    )

    private fun installedPackage(context: Context, launcher: Launcher): String? =
        launcher.packages.firstOrNull { pkg ->
            try {
                context.packageManager.getPackageInfo(pkg, 0)
                true
            } catch (_: PackageManager.NameNotFoundException) {
                false
            }
        }

    fun showChooser(context: Context) {
        val sorted = all.sortedBy { if (installedPackage(context, it) != null) 0 else 1 }
        val adapter = object : BaseAdapter() {
            override fun getCount() = sorted.size
            override fun getItem(position: Int) = sorted[position]
            override fun getItemId(position: Int) = position.toLong()
            override fun getView(position: Int, convertView: View?, parent: ViewGroup): View {
                val v = convertView ?: LayoutInflater.from(context).inflate(R.layout.item_launcher, parent, false)
                val launcher = sorted[position]
                val installed = installedPackage(context, launcher) != null
                v.findViewById<TextView>(R.id.name).text = launcher.name
                v.findViewById<TextView>(R.id.status).apply {
                    setText(if (installed) R.string.launcher_installed else R.string.launcher_get)
                    setTextColor(
                        ContextCompat.getColor(context, if (installed) R.color.neon_cyan else R.color.text_secondary)
                    )
                }
                return v
            }
        }
        MaterialAlertDialogBuilder(context)
            .setTitle(R.string.choose_launcher)
            .setAdapter(adapter) { _, which -> apply(context, sorted[which]) }
            .show()
    }

    private fun apply(context: Context, launcher: Launcher) {
        val pkg = installedPackage(context, launcher)
        if (pkg == null) {
            openStore(context, launcher.packages.first())
            return
        }
        val me = context.packageName
        val intent: Intent? = when (launcher.mode) {
            Mode.NOVA -> Intent("com.teslacoilsw.launcher.APPLY_ICON_THEME")
                .setPackage(pkg)
                .putExtra("com.teslacoilsw.launcher.extra.ICON_THEME_TYPE", "GO")
                .putExtra("com.teslacoilsw.launcher.extra.ICON_THEME_PACKAGE", me)
            Mode.SMART -> Intent("ginlemon.smartlauncher.setGSLTHEME")
                .putExtra("package", me)
            Mode.ACTION -> context.packageManager.getLaunchIntentForPackage(pkg)
                ?.putExtra("apply_icon_pack", me)
            Mode.APEX -> Intent("com.anddoes.launcher.SET_THEME")
                .putExtra("com.anddoes.launcher.THEME_PACKAGE_NAME", me)
                .putExtra("com.anddoes.launcher.THEME_TYPE", "ICON_THEME")
            Mode.MANUAL -> null
        }
        if (intent != null) {
            try {
                context.startActivity(intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK))
                return
            } catch (_: ActivityNotFoundException) {
                // segue para a instrução manual
            } catch (_: SecurityException) {
            }
        }
        Toast.makeText(context, context.getString(R.string.applied_manual, launcher.name), Toast.LENGTH_LONG).show()
        context.packageManager.getLaunchIntentForPackage(pkg)?.let {
            try {
                context.startActivity(it.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK))
            } catch (_: ActivityNotFoundException) {
            }
        }
    }

    private fun openStore(context: Context, pkg: String) {
        val market = Intent(Intent.ACTION_VIEW, Uri.parse("market://details?id=$pkg"))
        try {
            context.startActivity(market)
        } catch (_: ActivityNotFoundException) {
            context.startActivity(
                Intent(Intent.ACTION_VIEW, Uri.parse("https://play.google.com/store/apps/details?id=$pkg"))
            )
        }
    }
}
