import platform
import subprocess

command = 'docker ps --filter "label=tag=value" -q'
output = subprocess.check_output(command, shell=True, universal_newlines=True).strip()

subprocess.run(['docker', 'exec', output, 'curl', '-X', 'GET', 'http://127.0.0.1:8080/'])