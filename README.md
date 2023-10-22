# CACOPHONY-LOG
**Purpose**: This program watches a kubectl logstream and matches on specific log keys, and will then play a sound based on the value of that key. It's basically a really annoying (or soothing... depends I guess) way to hear patterns in your logs.

### Assumptions:
- you have the correct requirements.txt items installed
- kubectl is installed and has the correct permissions, kubectx, and you know the pod names of the logs you want to watch
- you run this from the environment those kubernetes pods are reachable from
- the logs you are reading from `kubectl logs --namespace your_namespace your_pod_name` are formatted in json
