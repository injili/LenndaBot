
#!/usr/bin/python3
"""
module main_file
A vanilla python script to interract with a user in form of a chat
"""


from flask import Flask, jsonify, request, render_template, session, url_for, redirect
import google.generativeai as genai
import markdown
from os import environ as env
import json
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

genai.configure(api_key=env.get('API_KEY'))
model=genai.GenerativeModel("gemini-1.5-flash")
initial_message = """
     Your name is CollegeBot.
    You are a sophisticated AI chatbot developed by Lennda.
    Your primary role is to assist users understand College and University, Their Programs, how to apply for them, and what they entail.
    Unless the user specifies the language they want their response in, reply in the language of the prompt.
    You have been trained on a diverse range of data sources, and you can generate creative, engaging, and relevant content.
    You are capable of understanding context, following instructions, and maintaining a consistent tone.
    You are designed to be helpful, knowledgeable, articulate, and polite.
    You always strive to provide responses that are not only accurate but also inspire and engage the user.
    If a user asks anything that is not related to cybersecurity, you are to respond that you only answer University Program questions.
"""
app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")
oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

@app.route('/')
def index():
    return render_template('index.html', session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

def get_response(prompt):
    full_prompt = f"{initial_message}\nUser: {prompt}"
    response = model.generate_content(full_prompt)
    return markdown.markdown(response.text)

@app.route("/get")
def get_the_response():
    userText = request.args.get('msg')
    reply = get_response(userText)
    return reply

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("index", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
