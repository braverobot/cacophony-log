# CACOPHONY-LOG
**Purpose**: This program watches a kubectl logstream and matches on specific log keys, and will then play a sound based on the value of that key. It's basically a really annoying (or soothing... depends I guess) way to hear patterns in your logs.

### Assumptions:
- **your logs don't contain important stuff in them**. This is for fun, and not meant to be run against kubectl logs where secret stuff may pop up in your logs
- you have the correct requirements.txt items installed
- kubectl is installed and has the correct permissions, kubectx, and you know the pod names of the logs you want to watch
- you run this from the environment those kubernetes pods are reachable from
- the logs you are reading from `kubectl logs --namespace your_namespace your_pod_name` are formatted in json


### Run
```
pip3 install -r requirements.txt
python3 cacophony.py
```
