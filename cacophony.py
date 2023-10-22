
from cac_player import CacophonyPlayer


if __name__ == "__main__":
    kubelog_player = CacophonyPlayer()
    namespace = 'some_namespace'
    pod = 'some_pod_name'
    kubelog_player.kgl_sounds(namespace, pod)
