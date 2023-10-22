import pygame.mixer
import time
import os
import yaml
import subprocess
import json
import logging

# setup some simple logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CacophonyPlayer:
    def __init__(self, dir: str = "sounds",
                 config_file: str = "sounds/sound_config.yaml") -> None:
        """This sound player is used to put short sounds to logs

        It takes a directory where wav files are stored and a YAML config file
        that maps the sound name to the file name.

        It is assumed that the logs read from kubectl get logs are in JSON
        format.
        """

        pygame.mixer.init()
        self._sound_directory = dir
        self._config_file = config_file
        self._sounds = self.load_sounds()

    def load_sounds(self) -> dict[str, pygame.mixer.Sound]:
        """Loads the sounds from the config file"""

        with open(self._config_file, 'r') as file:
            sound_mappings = yaml.safe_load(file)

        sound_files = {name: os.path.join(self._sound_directory, path)
                       for name, path in sound_mappings.items()
                       }

        # build the sounds dictionary using dict comprehension. It sets the
        # sound object as the value, and the name of the log as the key.
        # Example: {'player_name': <pygame.mixer.Sound object at 0x10>}
        sounds = {name: pygame.mixer.Sound(path)
                  for name, path in sound_files.items()}

        return sounds

    def play_sound(self, sound_obj):
        """Plays the sound object called"""

        sound_obj.play()

    def kgl_sounds(self, namespace, pod, tail_logs=True):
        """Read the logs from kubectl get logs and play sounds

        This takes the namespace and pod name and plays sounds based on the
        logs. If tail_logs is True, it will keep reading the logs.
        """

        # set the tail flag when tail_logs is true.
        # this avoids other flags being passed to kubectl.
        if tail_logs:
            flag = '-f'
        else:
            flag = ''

        cmd = ["kubectl", "logs", "--namespace", namespace, pod, flag]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                universal_newlines=True)
        try:
            for line in iter(proc.stdout.readline, ''):
                try:
                    log = json.loads(line)
                except json.JSONDecodeError:
                    logger.info(f"Couldn't parse log as JSON: {line.strip()}")

                try:
                    self.play_sound_based_on_log(log)
                except Exception as e:
                    logger.error(f"Couldn't play sound: {e}")
        except KeyboardInterrupt:
            proc.terminate()
        proc.wait()

    def play_sound_based_on_log(self, log):
        """Plays sound based on the 'player_name' key in the log.
        If you want to change this so the key firing the sound is different,
        you will want to change it from 'player_name' to the json key in the
        log
        """

        log_field = 'player_name'
        if log_field in log and log[log_field] in self._sounds:
            self.play_sound(self._sounds[log[log_field]])
            logger.info(f'Playing sound: {log[log_field]}')
            time.sleep(0.2)
