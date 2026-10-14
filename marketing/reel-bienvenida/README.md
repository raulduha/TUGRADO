# Reel de Apruvi: bienvenida

Proyecto HyperFrames del video de bienvenida (16,9 s) para quien recién se registra, en formato 9:16. Diseño según `motion.md` (raíz del repo); Apruvi y la plantilla de escenas vienen de `marketing/shared/hf_kit.py`.

- Plan: `STORYBOARD.md` y `storyboard.html` (lo genera `marketing/shared/make_storyboards.py`).
- Escenas: `python scripts/build_frames.py`; `index.html` lo arma el ensamblador del flujo music-to-video.
- **Música (no incluida):** "Wake up" de MBB, del segundo 99,54 a 116,45 (16,91 s). Para reconstruirla:
  `ffmpeg -ss 99.54 -t 16.91 -i "<tema>.mp3" -af "afade=t=in:st=0:d=0.05,afade=t=out:st=15.91:d=1.0" -ar 44100 -b:a 192k assets/bgm.mp3`
  Al publicar, acreditar: "Música: Wake up – MBB".
- Render: `npx hyperframes render . -q delivery --fps 30 -o renders/video.mp4` (los renders no se versionan).
