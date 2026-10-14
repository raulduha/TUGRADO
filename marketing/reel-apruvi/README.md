# Reel de Apruvi (Instagram Reels, 9:16)

Video de 21 s hecho con HyperFrames (`music-to-video`): Apruvi presenta Aprueba tu examen
(mapa de estudio, rachas y simulación oral). Diseño según `motion.md` de la raíz del repo.

- Plan: `STORYBOARD.md` y `storyboard.html` · marca: `frame.md` · golpes: `audiomap.json`.
- Las escenas se generan con `python scripts/build_frames.py`; `index.html` lo arma el
  ensamblador del flujo.
- **Música (no incluida):** "Wake up" de MBB, del segundo 40,84 al 61,84 con desvanecido
  final de 1 s. Para reconstruirla:
  `ffmpeg -ss 40.84 -t 21 -i "<tema>.mp3" -af "afade=t=in:st=0:d=0.05,afade=t=out:st=20:d=1" -ar 44100 -b:a 192k assets/bgm.mp3`
  Al publicar, acreditar: "Música: Wake up – MBB".
- Render: `npx hyperframes render . -q delivery --fps 30 -o renders/video.mp4` (los renders
  no se versionan).
