import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
        name='contacts_manager',
        version='1.0',
        description='Contacts manager for your terminal',
        author='Alfredo Robles',
        author_email='alfredoroblesa92@gmail.com',
        license='LICENSE.txt',
        long_description=read('README.md'),
        packages=['contacts', 'contacts.api'],
        entry_points={
        'console_scripts': [
            'contacts = contacts.app:main',
                ],
            },
        include_package_data=True,
     )