#!/usr/bin/python3
import os
import sys
from contacts.api.api import ContactsManagerAPI

DATABASE_PATH = "./contacts/.contacts-store"
HELP_DOCUMENT_PATH = "./contacts/docs/help.txt"
GIT_DIR = ".git"
FLASK_APP = "server"
FLASK_PATH = "./contacts/server"
COLUMN_WIDTH_NAME = 10
COLUMN_WIDTH_LNAME = 10
COLUMN_WIDTH_TLF = 12
COLUMN_WIDTH_EMAIL = 22
COLUMN_WIDTH_JOB = 8
COLUMN_WIDTH_PROV = 10


class ContactsManager:
    columns = ["Last Name", "Tlf", "Email", "Job", "Province"]
    table_columns = ["Contact", "Last Name", "Tlf", "Email", "Job", "Province"]
    table_columns_width = [COLUMN_WIDTH_NAME, COLUMN_WIDTH_LNAME, COLUMN_WIDTH_TLF, COLUMN_WIDTH_EMAIL, COLUMN_WIDTH_JOB, COLUMN_WIDTH_PROV]
    files = list(os.listdir(DATABASE_PATH))

    def __init__(self):
        self.flag_init = False
    
    def get_args(self):
        return sys.argv[1:]
    
    def initialize_database(self):
        if not os.path.isdir(DATABASE_PATH):
            api.git(DATABASE_PATH, "init")
            cur_dir = os.path.abspath(os.getcwd())
            db_dir = os.path.join(cur_dir, ".contacts-store")
            print(f"Initialized contacts store in {db_dir}")
            self.flag_init = True

    def check_initialization(self):
        if os.path.isdir(os.path.join(DATABASE_PATH, GIT_DIR)):
            self.flag_init = True

    def help(self):
        with open(HELP_DOCUMENT_PATH) as file:
            help_str = "".join(file.readlines())
            print(help_str)

    def add_contact(self, name):
        if name not in self.files:
            print("## Add new contact", name)
            last_name = input("Last name: ")
            tlf = input("Tlf: ")
            email = input("Email: ")
            job = input("Job: ")
            province = input("Province: ")
            data = {"last_name": last_name, "tlf": tlf, "email": email, "job": job, "province": province}
            path = os.path.join(DATABASE_PATH, name)
            api.write(path, data)
            # Git commit
            msg = f"'Add {name}'"
            api.git_commit(DATABASE_PATH, msg)
        elif name in self.files:
            print(f"ERROR: Contact {name} already exist.")
    
    def list_contacts_normal(self):
        for file_name in self.files:
            print(file_name)

    def list_contacts_table(self):
        header = ""
        sep = ""
        for c, w in zip(self.table_columns, self.table_columns_width):
            header += c.ljust(w) + " "
            sep += "-" * w + " "
        print(sep,'\n', header, '\n', sep, sep='')
        for file_name in self.files:
            file_path = os.path.join(DATABASE_PATH, file_name)
            data = api.read(file_path)
            print(file_name.ljust(COLUMN_WIDTH_NAME),data['last_name'].ljust(COLUMN_WIDTH_LNAME), data['tlf'].ljust(COLUMN_WIDTH_TLF), data['email'].ljust(COLUMN_WIDTH_EMAIL),data['job'].ljust(COLUMN_WIDTH_JOB),data['province'].ljust(COLUMN_WIDTH_PROV), sep=' ')

    def list_contacts(self, mode='normal'):
        self.files.remove(".git")
        if mode == 'normal':
            self.list_contacts_normal()
        elif mode == 'table':
            self.list_contacts_table()

    def remove_contact(self, name):
        if name in self.files:
            path = os.path.join(DATABASE_PATH, name)
            api.remove(path)
        else:
            print(f"ERROR: Contact {name} does not exist.")
        # Git commit
        msg = f"'Delete {name}'"
        api.git_commit(DATABASE_PATH, msg)

    def rename_contact(self, name, name_new):
        path = os.path.join(DATABASE_PATH, name)
        path_destn = os.path.join(DATABASE_PATH, name_new)
        if name in self.files and name_new not in self.files:
            api.rename(path, path_destn)
        elif name in self.files and name_new in self.files:
            print(f"Destination contact {name_new} already exists.")
            opt = input(f"Delete {name_new} and move {name} to {name_new}? [y/n]: ")
            if opt.lower() == 'y':
                api.remove(path_destn) # delete existing contact
                api.rename(path, path_destn) # rename current contact
            else: return
        print(f"Renamed {name} to {name_new}.")
        # Git commit
        msg = f"'Move {name} to {name_new}'"
        api.git_commit(DATABASE_PATH, msg)

    def edit_contact(self, name):
        print("## Edit contact", name)
        # Read data
        file_path = os.path.join(DATABASE_PATH, name)
        data = api.read(file_path)
        # Modify data
        i = 0
        for k, v in data.items():
            new_data = input(f"{self.columns[i]} [{data[k]}]: ")
            if new_data.strip():
                data[k] = new_data
            i += 1
        # Write data
        api.write(file_path, data)
        # Git commit
        msg = f"'Edit {name}'"
        api.git_commit(DATABASE_PATH, msg)

    def show_contact(self, name):
        file_path = os.path.join(DATABASE_PATH, name)
        if name in self.files:
            print("## Contact", name)
            # Read data
            data = api.read(file_path)
            # Show data
            i = 0
            for k, v in data.items():
                data[k] = print(f"{self.columns[i]}: {data[k]}")
                i += 1
        else: print("Contact does not exist.")
    
    def server(self):
        api.start_server(FLASK_PATH, FLASK_APP)

    def git(self, command):
        api.git(DATABASE_PATH, command)

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
            self.server()
        elif 'git' in args:
            command = args[1]
            self.git(command)

    def run(self):
        self.parse_args()


def main():
    cm.run()


# Classes instantiation
cm = ContactsManager()
api = ContactsManagerAPI()