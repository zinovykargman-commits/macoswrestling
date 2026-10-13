# GRIP BREAK 0.4.9 known limits

Shoulder weights, render-only shoulder volume pivots, shared body/cloth deformation and elbow routing were refined and inspected in native neutral front/back/side, overhead and live-reach views. The original deferred arm defects have been addressed in this pass, but extreme raised/armpit poses can still fold the clothing trim. Small white wisps near Cobalt's neckline remain cosmetic. Do not interpret the checked poses as a guarantee of perfect anatomy in every possible physics configuration.

The near-contact hand fit is deliberately slight: at most 2.8 cm, applied only to an already-held rival when the authored hand is near the anchor. It leaves physical hand rotation and forces unchanged. Fingers sit closer in the inspected contact view, but palms do not always lie completely flush against every curved body surface. The side/rear contact capture partially obscures the grip.

The editable packed Blender master is authoring source. Its static Cycles hair shading can differ from the native game; native captures are the evidence for shipped appearance.

The final native reports retain every failed scenario unchanged. VALIDATION.md and the current-validation-summary.json identify the actual remaining failures and totals after the final run. Earlier rejected builds and their failures are historical evidence, not current-source proof.

Physical keyboard/controller events, independent-machine internet play, long human matches, balance and enjoyment require hands-on acceptance. Mac joins Windows-hosted invites and uses keyboard/mouse; Mac hosting/controllers and automatic replacement updates are outside the current package. Mac uses manual downloads and is not Developer ID signed or notarized. Hosted Mac-runner checks do not establish physical-Mac GPU performance.


## Mac 0.4.9 verification limit

Fresh native Mac verification is pending. The previous 0.4.8 GitHub Mac runners used Apple Paravirtual GPUs and failed their frame-rate benchmarks. Mac defaults to Balanced graphics in this release; physical-Mac performance, current live internet play, long sessions and human balance remain unverified. Windows results do not establish Mac behavior.
