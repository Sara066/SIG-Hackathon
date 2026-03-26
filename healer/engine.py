import docker

client = docker.from_env()

def fix_container(name):
    print(f"[HEALER] Attempting to restart {name}...")
    container = client.containers.get(name)
    container.restart()
    print(f"[HEALER] {name} is back online!")