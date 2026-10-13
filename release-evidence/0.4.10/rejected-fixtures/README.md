# Preserved rejected Mac audit results

Run 38448751575 used wall-time waits that could sample before input reached a physics step on slow virtual graphics devices. The Intel free-stance test sampled 19 catch-up ticks after its input timeout; costs and physical stance checks passed. The Apple Silicon release check sampled before actual Release ran.

The final audit adapters wait for input polling and a completed physics step. They still require every held tick to accept Ctrl without cost, and actual grip/target release before an immediate zero-offset render. No production controls, physics costs, grip thresholds or rendering rules were weakened. All final functional checks passed in run 38451841211. Gym performance failures remain separately documented.
