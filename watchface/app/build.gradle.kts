import java.util.Properties

plugins {
    id("com.android.application")
}

// Release signing: read from environment variables (CI) or keystore.properties (local).
// Nothing secret is committed to the repository.
val keystoreProps = Properties().apply {
    val f = rootProject.file("keystore.properties")
    if (f.exists()) f.inputStream().use { load(it) }
}
fun signingValue(env: String, prop: String): String? =
    System.getenv(env)?.takeIf { it.isNotBlank() } ?: keystoreProps.getProperty(prop)

val storeFilePath = signingValue("WATCHFACE_KEYSTORE_PATH", "storeFile")
val hasReleaseSigning = storeFilePath != null && file(storeFilePath).exists()

android {
    namespace = "com.wenderlui.neonbeach.watchface"
    compileSdk = 36

    defaultConfig {
        applicationId = "com.wenderlui.neonbeach.watchface"
        // Watch Face Format v1 requires Wear OS 4 (API 33) or newer:
        // Galaxy Watch4 and later.
        minSdk = 33
        targetSdk = 36
        versionCode = 1
        versionName = "1.0.0"
    }

    signingConfigs {
        if (hasReleaseSigning) {
            create("release") {
                storeFile = file(storeFilePath!!)
                storePassword = signingValue("WATCHFACE_KEYSTORE_PASSWORD", "storePassword")
                keyAlias = signingValue("WATCHFACE_KEY_ALIAS", "keyAlias")
                keyPassword = signingValue("WATCHFACE_KEY_PASSWORD", "keyPassword")
            }
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            if (hasReleaseSigning) signingConfig = signingConfigs.getByName("release")
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}
