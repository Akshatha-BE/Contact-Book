from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

FILE = "contacts.json"


def load_contacts():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    return []


def save_contacts(contacts):
    with open(FILE, "w") as f:
        json.dump(contacts, f, indent=4)


@app.route("/", methods=["GET", "POST"])
def index():

    contacts = load_contacts()

    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]

        contacts.append({
            "name": name,
            "phone": phone
        })

        save_contacts(contacts)

        return redirect("/")

    return render_template("index.html", contacts=contacts)


@app.route("/delete/<int:id>")
def delete(id):

    contacts = load_contacts()

    contacts.pop(id)

    save_contacts(contacts)

    return redirect("/")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    contacts = load_contacts()

    if request.method == "POST":

        contacts[id]["name"] = request.form["name"]
        contacts[id]["phone"] = request.form["phone"]

        save_contacts(contacts)

        return redirect("/")

    return render_template("edit.html", contact=contacts[id], id=id)


@app.route("/search")
def search():

    query = request.args.get("query")

    contacts = load_contacts()

    results = []

    for c in contacts:
        if query.lower() in c["name"].lower():
            results.append(c)

    return render_template("index.html", contacts=results)


if __name__ == "__main__":
    app.run(debug=True)