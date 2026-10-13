# Mac 0.4.8 verification

Unity6000.3.7f1 universal Mono/Metal build for macOS12 or later. The native executable and libraries contain Intel x86_64 and Apple Silicon arm64. 104/106 existing native assertions passed across macOS15 Intel and Apple Silicon runners, with zero reported runtime issues: stamina, scramble, appearance/bone/texture/shoe checks, gym/rope geometry, and rendered startup/menu capture. The gym_performance assertion failed on both Apple Paravirtual graphics devices; actual FPS is preserved in raw reports. This is not an all-pass claim. It leaves physical-Mac frame rate unverified; rendered menus and images do not establish smooth gameplay. Native screenshots were inspected separately. Reports are in release-evidence/0.4.8.

The app matches released Windows f167 gameplay/assets, with documented Mac platform adapters. Signing changes are confined to native signatures; managed code/assets remain byte-identical to the raw universal build. The source/build manifests identify raw and signed contents. ZIP permissions/CRC/hashes are checked; public downloads are verified after upload.

Same92-body protocol12 and Windows-hosted copied invites are retained. Current0.4.8 live internet play, human gameplay feel, long sessions, other macOS versions and physical keyboards/mice are not verified by these checks. This Mac version joins Windows-hosted invites; Mac hosting/controllers are not included. GET LATEST MAC VERSION opens downloads for manual replacement.

Local ad-hoc signatures are verified on both native architectures. This is not Apple Developer ID signing or notarization; Gatekeeper may require Apple's per-app Open Anyway flow: https://support.apple.com/en-us/102445 .

Known Windows limitations remain: two inconsistent scripted pin/legacy-walk scenarios (337/339 Windows assertions passed) and the user-deferred overhead shoulder deformation/blue athlete's crooked relaxed arm. See KNOWN_ISSUES.md. Native appearance assertions and screenshots do not certify all animation poses.
