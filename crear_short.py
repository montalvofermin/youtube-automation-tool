# ============================================================
#  Data Mundial 2026 — Short v3
#  ✅ Zoom Ken Burns | Palabras animadas | Fundido | Logo
# ============================================================

from moviepy import ImageClip, TextClip, CompositeVideoClip
from moviepy.video.fx import FadeIn, FadeOut
import os

# ── CONFIGURACIÓN ─────────────────────────────────────────────
FOTOS         = ["foto1.jpg", "foto2.jpg", "foto3.jpg"]
DURACION_FOTO = 4.0         # Segundos por foto
FADE_DUR      = 1.8         # Duración del fundido entre fotos
SALIDA        = "short_v3.mp4"
FUENTE        = "C:/Windows/Fonts/impact.ttf"
LOGO          = "logo.png"

# Un subtítulo por foto — se muestra palabra por palabra
SUBTITULOS = [
    "TODA LA INFORMACION SOBRE EL MUNDIAL",
    "DATOS ESTADISTICAS Y PASION TOTAL",
    "QUIEN LEVANTARA LA COPA EN 2026",
]

print("⚙️  Construyendo short v3... esto puede tardar 30-60 seg.")

# ── 1. DIMENSIONES desde la primera foto ─────────────────────
ref = ImageClip(FOTOS[0])
ANCHO, ALTO = ref.size
ref.close()

# ── 2. FOTOS con zoom Ken Burns + fundidos ────────────────────
STEP  = DURACION_FOTO - FADE_DUR          # Separación entre inicios
TOTAL = DURACION_FOTO + (len(FOTOS) - 1) * STEP

foto_clips = []
for i, foto in enumerate(FOTOS):
    clip = (
        ImageClip(foto)
        .with_duration(DURACION_FOTO)
        # Zoom: empieza en 50% y llega al 110%
        .resized(lambda t, d=DURACION_FOTO: 1 + 0.10 * (t / d))
        .with_position("center")
        .with_start(i * STEP)
    )
    efectos = []
    if i > 0:
        efectos.append(FadeIn(FADE_DUR))
    if i < len(FOTOS) - 1:
        efectos.append(FadeOut(FADE_DUR))
    if efectos:
        clip = clip.with_effects(efectos)
    foto_clips.append(clip)

# ── 3. PALABRAS ANIMADAS (aparecen de a una por subtítulo) ────
word_clips = []
for i, frase in enumerate(SUBTITULOS):
    palabras   = frase.split()
    t_inicio   = i * STEP
    dur_palabra = DURACION_FOTO / len(palabras)

    for j, palabra in enumerate(palabras):
        wc = (
            TextClip(
                text=palabra,
                font_size=30,
                color="#1D2FCE",       # azul
                font=FUENTE,
                stroke_color="black",
                stroke_width=5,
            )
            .with_start(t_inicio + j * dur_palabra)
            .with_duration(dur_palabra)
            .with_position("center")
        )
        word_clips.append(wc)

# ── 4. TÍTULO FIJO arriba ─────────────────────────────────────
titulo = (
    TextClip(
        text="DATA MUNDIAL 2026",
        font_size=30,
        color="white",
        font=FUENTE,
        stroke_color="#39FF14",
        stroke_width=3,
    )
    .with_duration(TOTAL)
    .with_position(("center", 45))
)

# ── 5. LOGO marca de agua (opcional) ─────────────────────────
logo_clips = []
if os.path.exists(LOGO):
    logo_clip = (
        ImageClip(LOGO)
        .with_duration(TOTAL)
        .resized(height=30)
        .with_opacity(1.8)
        .with_position((ANCHO - 120, ALTO - 90))
    )
    logo_clips = [logo_clip]
    print("✅ Logo encontrado y agregado.")
else:
    print("⚠️  logo.png no encontrado — se omite la marca de agua.")

# ── 6. COMPOSICIÓN FINAL ──────────────────────────────────────
video_final = CompositeVideoClip(
    foto_clips + word_clips + [titulo] + logo_clips,
    size=(ANCHO, ALTO)
)

# ── 7. EXPORTAR ───────────────────────────────────────────────
video_final.write_videofile(
    SALIDA,
    fps=24,
    codec="libx264",
    audio=False,
)

print(f"\n✅ ¡Listo! Video guardado como '{SALIDA}' en tu carpeta.")