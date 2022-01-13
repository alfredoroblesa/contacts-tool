import os
from contacts.app import ContactsManager
from contacts.api.api import ContactsManagerAPI

DATABASE_PATH = "./contacts/.contacts-store"

class TestClass:
    cm = ContactsManager()
    api = ContactsManagerAPI()
    
    def test_one(self):
        test_name = "Test"
        file_path = os.path.join(DATABASE_PATH, test_name)
        # Create and read contact with API
        print("\n\nIntroduce the following testing data:\nLast Name: Test\nTlf: 10\nEmail: test@email.com\nJob: Testing\nProvince: Madrid\n\n")
        self.cm.add_contact(test_name)
        data = self.api.read(file_path)
        # Create testing data
        test_data = {"last_name": "Test", "tlf": "10", "email": "test@email.com", "job": "Testing", "province": "Madrid"}
        self.api.remove(file_path)
        assert test_data == data