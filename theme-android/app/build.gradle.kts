import java.util.Properties

plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

// Assinatura de upload: lida de keystore.properties (local) ou de variáveis de ambiente (CI).
val keystoreProps = Properties().apply {
    val f = rootProject.file("keystore.properties")
    if (f.exists()) f.inputStream().use { load(it) }
}
fun signingValue(key: String, env: String): String? =
    keystoreProps.getProperty(key) ?: System.getenv(env)

val storeFilePath = signingValue("storeFile", "NEON_KEYSTORE_PATH")

android {
    namespace = "com.wenderlui.neonshore"
    compileSdk = 36

    defaultConfig {
        applicationId = "com.wenderlui.neonshore"
        minSdk = 26
        targetSdk = 36
        versionCode = (System.getenv("NEON_VERSION_CODE") ?: "1").toInt()
        versionName = "1.0.0"
    }

    signingConfigs {
        if (storeFilePath != null) {
            create("upload") {
                storeFile = file(storeFilePath)
                storePassword = signingValue("storePassword", "NEON_KEYSTORE_PASSWORD")
                keyAlias = signingValue("keyAlias", "NEON_KEY_ALIAS")
                keyPassword = signingValue("keyPassword", "NEON_KEY_PASSWORD")
            }
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            isShrinkResources = false // os ícones são carregados pelos launchers por nome; não podem ser removidos
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
            if (storeFilePath != null) signingConfig = signingConfigs.getByName("upload")
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }

    buildFeatures { buildConfig = false }

    androidResources {
        // wallpapers já são JPEG otimizados
        noCompress += listOf("jpg")
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.16.0")
    implementation("androidx.appcompat:appcompat:1.7.1")
    implementation("androidx.recyclerview:recyclerview:1.4.0")
    implementation("com.google.android.material:material:1.12.0")
}
