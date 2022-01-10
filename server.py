from flask import Flask, jsonify, request
from flask_cors import CORS

import logging
logging.basicConfig(level=logging.INFO)


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}}) #TODO: see the warning located here to determine if you do not want to allow route requests globally (https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/)


# RECEIVES A JavaScript object with a username and password
# RETURNS A bunch of data including:
# - All the user's friends
# - The events the user has attended
from facebook_scraper import BuildSocialBarriersScraper
TESTING = False
if (TESTING):
    import json
    file = open('login.json')
    login = json.load(file)
    username = login["username"]
    password = login["password"]
    BuildSocialBarriersScraper.buildAndRunScraper(username, password)

@app.route('/logIn', methods=['POST'])
def log_in():
    data = request.json
    logging.debug(data["username"])
    return BuildSocialBarriersScraper.buildAndRunScraper(data["username"], data["password"])

if __name__ == '__main__':
    app.run()
