# Reel de Apruvi: motivacion

Proyecto HyperFrames del video de motivación (13 s) para el correo de ánimo y redes, en formato 9:16. Diseño según `motion.md` (raíz del repo); Apruvi y la plantilla de escenas vienen de `marketing/shared/hf_kit.py`.

- Plan: `STORYBOARD.md` y `storyboard.html` (lo genera `marketing/shared/make_storyboards.py`).
- Escenas: `python scripts/build_frames.py`; `index.html` lo arma el ensamblador del flujo music-to-video.
- **Música (no incluida):** "Wake up" de MBB, del segundo 28,33 a 41,33 (13 s). Para reconstruirla:
  `ffmpeg -ss 28.33 -t 13 -i "<tema>.mp3" -af "afade=t=in:st=0:d=0.3,afade=t=out:st=12.2:d=0.8" -ar 44100 -b:a 192k assets/bgm.mp3`
  Al publicar, acreditar: "Música: Wake up – MBB".
- Render: `npx hyperframes render . -q delivery --fps 30 -o renders/video.mp4` (los renders no se versionan).
