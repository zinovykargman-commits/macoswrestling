# GRIP BREAK for Mac — 0.4.5

Extract GRIP_BREAK-macOS.zip, then open GRIP BREAK.app. Both Intel and Apple Silicon native executables are included. This first Mac package uses keyboard/mouse, AI local and joining a Windows-hosted private invite. Game physics and network protocol12 match Windows0.4.5. The Windows friend hosts, copies the invite and sends it; the Mac player pastes it into Private Online, joins and readies up. Both ready; Windows host starts.

WASD move; mouse aims arms; left/right click hold each hand; release the click to let go. Shift sprint, Space jump, Q shot (grab manually), E sprawl, R lift, C pin, Ctrl+move scramble, X shove. F1 controls; F11 fullscreen (some Mac keyboards require Fn). Escape pause/back. Saved Keybinds page permits changing keys. Prefer a mouse with separate left/right buttons.

GET LATEST MAC VERSION opens this repository's release page; updates are manual. Mac invite hosting and controller support are not included in this first package. Your friend does not need Unity or its build module.

This is a Windows-cross-built, unnotarized Mac test package. It has not yet been run on a physical Mac. If macOS blocks it as an unidentified developer, follow Apple's per-app Open Anyway instructions at https://support.apple.com/en-us/102445 after verifying the download hash. Do not disable Gatekeeper globally. The ZIP preserves executable permissions; no Terminal step should be needed. If extraction loses those permissions, run chmod +x on the app's Contents/MacOS executable, as described by Unity: https://docs.unity3d.com/6000.3/Documentation/Manual/macos-building.html .

Please test launch, rendering, WASD/mouse/keys, local AI, pasted invite connection, ready/start and multiplayer movement. The native checks and inspected screenshots support startup, rendering, physics accounting and the tested cross-machine connection. They do not establish every controller/human play exchange. macOS12 or later is configured; actual supported OS/hardware needs native confirmation.

0.4.5: scramble never automatically releases opponent grips. Real strain still breaks holds; Ctrl release has0.4s recovery against jitter clicking. Holding resumes once ready; exhausted recovery remains1.2s. Both players need0.4.5.
