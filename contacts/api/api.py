import os
import json
import subprocess

class ContactsManagerAPI:
    def remove(self, path):
        cmd = f"rm {path}"
        self.execute_command(cmd)

    def rename(self, path, path_destn):
        cmd = f"mv {path} {path_destn}"
        self.execute_command(cmd)

    def read(self, path):
        with open(path, 'r') as f:
            data = json.load(f)
            return data

    def write(self, path, data):
        with open(path, 'w') as f:
            json.dump(data, f, ensure_ascii=False)

    def git(self, path, command):
        cmd = f"cd {path}; git {command}"
        self.execute_stdout_command(cmd)

    def git_commit(self, path, msg):
        cmd = f"cd {path}; git add .; git commit -m {msg}"
        self.execute_command(cmd)

    def start_server(self, path, app):
        cmd = f"cd {path}; export FLASK_APP={app}; flask run"
        self.execute_stdout_command(cmd)

    def execute_command(self, cmd):
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

    def execute_stdout_command(self, cmd):
        subprocess.Popen(cmd, shell=True)