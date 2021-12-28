#!/usr/bin/python3
import sys

DATABASE_PATH = ""
HELP_DOCUMENT_PATH = "./help.txt"


class ContactsManager():
    def __init__(self):
        pass
    
    def get_args(self):
        return sys.argv[1:]

    def help(self):
        with open(HELP_DOCUMENT_PATH) as file:
            help_str = "".join(file.readlines())
            print(help_str)

    def add_contact(self, name):
        print("## Add new contact", name)
        tlf = input("Tlf: ")
        email = input("Email: ")
        province = input("Province: ")
    
    def list_contacts(self, mode='normal'):
        print("List of contacts")

    def remove_contact(self, name):
        pass

    def rename_contact(self, name, name_new):
        print("Renaming contact with name", name, "to", name_new)

    def edit_contact(self, name):
        print("## Edit contact", name)

    def show_contact(self, name):
        print("## Contact", name)

    def parse_args(self):
        args = self.get_args()
        if len(args) > 0:
            name = args[1]
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

    def run(self):
        self.parse_args()

if __name__ == "__main__":
    app = ContactsManager()
    app.run()
    