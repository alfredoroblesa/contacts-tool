import os
import json
from flask import Flask, render_template

DATABASE_PATH = "../.contacts-store"

# Read database and build HTML string
file_names = os.listdir(DATABASE_PATH)
file_names.remove(".git")
html = "<table><th>Contact</th><th>Last Name</th><th>Tlf</th><th>Email</th><th>Job</th><th>Province</th>"
for file_name in file_names:
    file_path = os.path.join(DATABASE_PATH, file_name)
    with open(file_path, 'r') as f:
        data = json.load(f)
        data['name'] = file_name
        html += f"<tr><td>{data['name']}</td><td>{data['last_name']}</td><td>{data['tlf']}</td><td>{data['email']}</td><td>{data['job']}</td><td>{data['province']}</td></tr>"

# Create Flask app
server = Flask(__name__)

@server.route("/")
def contacts_table():
    return html