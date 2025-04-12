from flask import Flask, render_template, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Random secret key to encrypt session data
oauth = OAuth(app)

# Set up OAuth with Google and LinkedIn
google = oauth.register(
    name='google',
    client_id='YOUR_GOOGLE_CLIENT_ID',
    client_secret='YOUR_GOOGLE_CLIENT_SECRET',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    refresh_token_url=None,
    client_kwargs={'scope': 'openid profile email'},
)

linkedin = oauth.register(
    name='linkedin',
    client_id='YOUR_LINKEDIN_CLIENT_ID',
    client_secret='YOUR_LINKEDIN_CLIENT_SECRET',
    authorize_url='https://www.linkedin.com/oauth/v2/authorization',
    authorize_params=None,
    access_token_url='https://www.linkedin.com/oauth/v2/accessToken',
    refresh_token_url=None,
    client_kwargs={'scope': 'r_liteprofile r_emailaddress'},
)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login/google')
def login_google():
    redirect_uri = url_for('google_auth', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/login/linkedin')
def login_linkedin():
    redirect_uri = url_for('linkedin_auth', _external=True)
    return linkedin.authorize_redirect(redirect_uri)

@app.route('/auth/google')
def google_auth():
    token = google.authorize_access_token()
    user = google.parse_id_token(token)
    session['user'] = user
    return redirect(url_for('welcome'))

@app.route('/auth/linkedin')
def linkedin_auth():
    token = linkedin.authorize_access_token()
    user = linkedin.get('v2/me', token=token)
    session['user'] = user
    return redirect(url_for('welcome'))

@app.route('/welcome')
def welcome():
    user_info = session.get('user')
    if user_info:
        name = user_info.get('name') or user_info.get('localizedFirstName', 'User')
        return f"Welcome, {name}!"
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
