#!/usr/bin/python3
import os
import sys
import json
import subprocess

DATABASE_PATH = "./.contacts-store"
HELP_DOCUMENT_PATH = "./help"
GIT_DIR = ".git"
COLUMN_WIDTH_NAME = 10
COLUMN_WIDTH_LNAME = 10
COLUMN_WIDTH_TLF = 12
COLUMN_WIDTH_EMAIL = 22
COLUMN_WIDTH_JOB = 8
COLUMN_WIDTH_PROV = 10

class ContactsManager():
    table_columns = ["Contact", "Last Name", "Tlf", "Email", "Job", "Province"]
    table_columns_width = [COLUMN_WIDTH_NAME, COLUMN_WIDTH_LNAME, COLUMN_WIDTH_TLF, COLUMN_WIDTH_EMAIL, COLUMN_WIDTH_JOB, COLUMN_WIDTH_PROV]
    columns = ["Last Name", "Tlf", "Email", "Job", "Province"]

    def __init__(self):
        self.flag_init = False
    
    def initialize_database(self):
        if not os.path.isdir(DATABASE_PATH):
            command = f"git init {DATABASE_PATH}"
            subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            cur_dir = os.path.abspath(os.getcwd())
            db_dir = os.path.join(cur_dir, ".contacts-store")
            print(f"Initialized contacts store in {db_dir}")
            self.flag_init = True

    def check_initialization(self):
        if os.path.isdir(os.path.join(DATABASE_PATH, GIT_DIR)):
            self.flag_init = True

    def get_args(self):
        return sys.argv[1:]

    def git_commit(self, msg):
        command = f"cd {DATABASE_PATH}; git add .; git commit -m {msg}"
        subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

    def help(self):
        with open(HELP_DOCUMENT_PATH) as file:
            help_str = "".join(file.readlines())
            print(help_str)

    def add_contact(self, name):
        files = list(os.listdir(DATABASE_PATH))
        if name not in files:
            print("## Add new contact", name)
            last_name = input("Last name: ")
            tlf = input("Tlf: ")
            email = input("Email: ")
            job = input("Job: ")
            province = input("Province: ")
            data = {"last_name": last_name, "tlf": tlf, "email": email, "job": job, "province": province}
            with open(os.path.join(DATABASE_PATH, name), 'w') as f:
                json.dump(data, f, ensure_ascii=False)
            # Git commit
            msg = f"'Add {name}'"
            self.git_commit(msg)
        elif name in files:
            print(f"ERROR: Contact {name} already exist.")

    def list_contacts(self, mode='normal'):
        files = list(os.listdir(DATABASE_PATH))
        files.remove(".git")
        if mode == 'normal':
            for file_name in files:
                print(file_name)
        elif mode == 'table':
            header = ""
            sep = ""
            for c, w in zip(self.table_columns, self.table_columns_width):
                header += c.ljust(w) + " "
                sep += "-" * w + " "
            print(sep,'\n', header, '\n', sep, sep='')
            for file_name in files:
                file_path = os.path.join(DATABASE_PATH, file_name)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                print(file_name.ljust(COLUMN_WIDTH_NAME),data['last_name'].ljust(COLUMN_WIDTH_LNAME), data['tlf'].ljust(COLUMN_WIDTH_TLF), data['email'].ljust(COLUMN_WIDTH_EMAIL),data['job'].ljust(COLUMN_WIDTH_JOB),data['province'].ljust(COLUMN_WIDTH_PROV), sep=' ')

    def remove_contact(self, name):
        files = list(os.listdir(DATABASE_PATH))
        if name in files:
            command = f"rm {os.path.join(DATABASE_PATH, name)}"
            subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        else:
            print(f"ERROR: Contact {name} does not exist.")
        # Git commit
        msg = f"'Delete {name}'"
        self.git_commit(msg)

    def rename_contact(self, name, name_new):
        print(f"Renaming contact with name {name} to {name_new}")
        files = list(os.listdir(DATABASE_PATH))
        if name in files and name_new not in files:
            command = f"mv {os.path.join(DATABASE_PATH, name)} {os.path.join(DATABASE_PATH, name_new)}"
            subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        elif name in files and name_new in files:
            print(f"Destination contact {name_new} already exists.")
            opt = input(f"Delete {name_new} and move {name} to {name_new}? [y/n]: ")
            if opt.lower() == 'y':
                # Delete existing contact
                command = f"rm {os.path.join(DATABASE_PATH, name_new)}"
                subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
                # Rename current contact
                command = f"mv {os.path.join(DATABASE_PATH, name)} {os.path.join(DATABASE_PATH, name_new)}"
                subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        print(f"Renamed {name} to {name_new}.")
        # Git commit
        msg = f"'Move {name} to {name_new}'"
        self.git_commit(msg)

    def edit_contact(self, name):
        print("## Edit contact", name)
        file_path = os.path.join(DATABASE_PATH, name)
        # Read data
        with open(file_path, 'r') as f:
            data = json.load(f)
        # Modify data
        i = 0
        for k, v in data.items():
            new_data = input(f"{self.columns[i]} [{data[k]}]: ")
            if new_data.strip():
                data[k] = new_data
            i += 1
        # Write data
        with open(file_path, 'w') as f:
            data = json.dump(data, f, ensure_ascii=False)
        # Git commit
        msg = f"'Edit {name}'"
        self.git_commit(msg)

    def show_contact(self, name):
        print("## Contact", name)
        file_path = os.path.join(DATABASE_PATH, name)
        # Read data
        with open(file_path, 'r') as f:
            data = json.load(f)
        # Show data
        i = 0
        for k, v in data.items():
            data[k] = print(f"{self.columns[i]}: {data[k]}")
            i += 1
    
    def start_server(self):
        pass

    def parse_args(self):
        args = self.get_args()
        self.check_initialization()
        if 'init' in args and not self.flag_init:
            self.initialize_database()
        elif not self.flag_init:
            print("ERROR: please, initialize the contacts store first with 'contacts init'.")
            return
        # Get name of contact    
        if len(args) > 1:
            name = args[1]
        # Parse the corresponding option
        if 'help' in args:
            self.help()
        elif 'add' in args:
            self.add_contact(name)
        elif 'ls' in args or len(args) == 0:
            self.list_contacts(mode='normal')
        elif 'table' in args:
            self.list_contacts(mode='table')
        elif 'rm' in args:
            self.remove_contact(name)
        elif 'mv' in args:
            name_new = args[2]
            self.rename_contact(name, name_new)
        elif 'edit' in args:
            self.edit_contact(name)
        elif 'show' in args:
            self.show_contact(name)
        elif 'server' in args:
            self.start_server()

    def run(self):
        self.parse_args()

if __name__ == "__main__":
    app = ContactsManager()
    app.run()
