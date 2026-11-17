# Reel-Studio – Notizen

## Stand (17.11.2026)
- Video v1 „Zeigarnik-Effekt“ fertig: `videos/v1_zeigarnik.mp4` (35 s, 1080×1920)
- Kostenlose Tools: FFmpeg, faster-whisper (Modell „medium“), Piper TTS (de_DE-thorsten-high), HyperFrames 0.9.64, yt-dlp
- Musik und Soundeffekte selbst erzeugt (`werkzeuge/music.py`, Zeitpunkte in `cues.json`)

## Feedback zu v1 → für v2 umsetzen
- ✅ Thema gefällt (Zeigarnik-Effekt beibehalten)
- ✅ Animationsstil grundsätzlich gut, ABER neuer Look gewünscht:
  - Farben: **Blautöne + Schwarz** (statt Lila/Pink/Gelb)
  - **Grafische Illustrationen**, die genau zeigen, was gerade erzählt wird
- ❌ Stimme gefällt nicht:
  - Betonung/Sprachmelodie passt nicht zu den Sätzen
  - Klang der Stimme an sich gefällt nicht
  - → bessere, natürlichere Stimme suchen (Optionen klären: ElevenLabs kann Credits kosten; kostenlose Alternativen testen)

## So neu bauen
1. Voiceover erzeugen (Piper/andere Stimme) → `voice.wav`
2. Whisper → `words.json` (Wort-Zeitstempel)
3. `python3 music.py` → `music.wav`, `sfx.wav`
4. `python3 build.py` → `projekt/index.html`
5. `npx hyperframes check` → `npx hyperframes render -q high -o out.mp4`
