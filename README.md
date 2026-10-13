# GRIP BREAK for Mac — 0.4.10

**[Download the Mac game](https://github.com/zinovykargman-commits/macoswrestling/releases/latest)**. Extract GRIP_BREAK-macOS.zip, then open GRIP BREAK.app. Universal Intel and Apple Silicon; macOS 12 or later. Your friend does not need Unity. Use a mouse with separate left/right buttons.

Private online: your Windows friend hosts, copies the complete invite link and sends it. Paste it into PRIVATE ONLINE, JOIN FRIEND, then READY UP. Both ready; the Windows host starts. Keyboard/mouse, AI local and joining Windows-hosted private matches are included. Mac invite hosting/controllers are not included. Same 92-body protocol 12; both players should use 0.4.10.

WASD move, mouse aims arms, left/right clicks hold each grip; release that click to let go. Shift sprint, Space jump, Q forward shot (grab manually), E sprawl, R lift, C pin. Hold Ctrl standing to lower into a normal wrestling stance, without scramble stamina cost. On the ground Ctrl + move bridges/rolls and costs stamina. F1 controls, F11 fullscreen (Fn may be needed), Escape pause/back. Controls can be changed in Keybinds. X shove/tackle/throw buttons are removed.

This version carries the frozen Windows f182 gameplay/assets, including the slightly lower Q shot, arm shape/skinning/IK refinements and indoor menu camera. Settings offers High, Balanced and Performance graphics; Mac starts on Balanced. These presets change lighting/edges, not physics or model detail. No claim that every arm pose is visually perfect; see KNOWN_ISSUES.md.

Grounded stamina: after 2.5 seconds physically on the mat, resting can regenerate at the original 19 stamina/second, including while being pinned. Active gripping/lifting/sprinting/sprawling or scrambling still costs stamina and cannot regenerate. Ctrl attempts retain the existing 0.8-second recovery block; tapping does not create free recovery. Standing recovery and its rate are unchanged.

Pin chest-down or back-down with both actual shoulders grounded for 2.5 seconds; ropes count. The out-of-bounds offender restarts on hands/knees with the opponent kneeling behind, then rapid 3/2/1 and whistle.

GET LATEST MAC VERSION opens the latest Mac release. Download and replace the app manually; automatic installation is not included.

Native macOS 15 Intel and Apple Silicon startup, gameplay, gym geometry and appearance checks passed; actual screenshots were inspected (300/302 total assertions). The gym frame-rate benchmark failed on 2 virtual graphics runner(s); actual FPS and failures are preserved in raw reports. Physical-Mac performance remains unverified. Current 0.4.10 live internet play is untested. See VALIDATION.md.

Built with Unity 6000.3.7f1. Local ad-hoc signatures are verified on both architectures. The app is not Apple Developer ID signed or notarized; macOS may require the per-app Open Anyway flow: https://support.apple.com/en-us/102445 .
