import subprocess

def is_docker_running():
    try:
        result = subprocess.run(
            ["systemctl", "is-active", "--quiet", "docker"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False