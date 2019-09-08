from flask import Flask, render_template, url_for, make_response, request, redirect
import json

app = Flask(__name__)
org_json = "organizations.json"

def search(search_words):  # inefficient search
    #takes in a string that the user puts
    search_words = search_words.upper()  # turns words to upper case to prevent formatting issues
    search_words = search_words.split(' ')  # splits words apart at spaces
    with open(org_json) as file:
        org_data = json.load(file)
    
    # dictionaries which keep track of the org names and the amount of matches to the search
    name_list = {}
    tag_list = {}

    # first searching through the organizations name
    for i in search_words:
        for key in org_data.keys():
            if i in key.split('-'):
                if key not in name_list:
                    name_list[key] = 1  # puts counter to one
                else:
                    name_list[key] += 1 # adds one to counter since match occurred

    # then searching through tags
    for key, value in org_data.items():
        if " ".join(search_words) in value["tags"]:
            if key not in name_list and key not in tag_list:  # preventing the inclusion of orgs that are already in name_list
                tag_list[key] = 1
            elif key in tag_list:
                tag_list[key] += 1

    # create list for org names arranged in priority of name (from greatest value to least)  and tags (from greatest to least)
    final_list =[]
    for key, value in name_list.items():
        for i in range(len(search_words), 0, -1):
            if i == value:
                final_list.append(key)
    for key, value in tag_list.items():
        for i in range(len(search_words), 0, -1):
            if i == value:
                final_list.append(key)
    
    return final_list
                

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")

@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template("about.html")

@app.route("/organizations")
def organization():
    with open(org_json) as file:
        org_data = json.load(file)

    return render_template("list_organizations.html", org_data = org_data)

# for testing purposes
# @app.route("/single")
# def org():
#     return render_template("organization.html")

# Basic idea for API:
#   get and post request for search
#   get request with organization name in title (most likely will have to be exact name)
#   post request (if adding functionality for organization accounts) which handles adding new info to database
#   post request which updates organization info

@app.route("/search", methods=["GET", "POST"])
def org_search():
    if request.method == "POST":
        search_words = request.form["search"]
        with open(org_json) as file:
            org_date = json.load(file)
        org_endpoint = search(search_words)
        if len(org_endpoint) != 0:
            org_list = [org_date[i]["name"] for i in org_endpoint]
            return render_template("search.html", org_list = org_list, org_endpoint = org_endpoint)
        else:
            return render_template("search.html")
    return render_template("search.html")

@app.route("/organizations/<org_name>", methods=["GET"])
def org_info(org_name):
    try:
        org_name = org_name.upper()
        with open(org_json) as file:
            org_data = json.load(file)
        
        uni_level = {"UG": "Undergraduate", "G": "Graduate", "F/S": "Faculty and Staff"}

        title = org_data[org_name]["name"]
        abbreviation = org_data[org_name]["abbrev"]
        description = org_data[org_name]["description"]
        contact = org_data[org_name]["contact"]
        website = org_data[org_name]["website"]
        level = ", ".join([uni_level[l] for l in org_data[org_name]["level"]])
        dues = org_data[org_name]["dues"]
        size = org_data[org_name]["size"]
        tags = org_data[org_name]["tags"]
        FAQ = org_data[org_name]["FAQ"]
        if abbreviation != "":
            return render_template("organization.html", title=title, abbreviation=abbreviation, description=description, contact=contact, website=website, level=level, dues=dues, size=size, tags=tags, FAQ = FAQ)
        else:
            return render_template("organization.html", title=title, description=description, contact=contact, website=website, level=level, dues=dues, size=size, tags=tags, FAQ=FAQ)
    except:
        return make_response(render_template("not_found.html"), 404)

# Will be implemented once authorization is implemented
# @app.route("/organizations/<org_id>/create", methods=["POST"])
# def org_create(org_id):
#     return make_response(200)

# @app.route("/organizations/<org_id>/update", methods=["POST"])
# def org_update(org_id):
#     return make_response(200)

# any invalid endpoint
@app.route("/<random>")
def invalid(random):
    return render_template("not_found.html")

if __name__ == "__main__":
    app.run(debug = True)
    