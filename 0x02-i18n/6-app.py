#!/usr/bin/env python3
""" Flask Application """
from flask import Flask, render_template, request, g
from flask_babel import Babel
from typing import Dict, Union

app = Flask(__name__)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """ Configuration class """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    """ determine the best match with our supported languages

    The order of priority should be:

        1-Locale from URL parameters
        2-Locale from user settings
        3-Locale from request header
        4-Default locale
    """

    # locale from URL parameters
    language = request.args.get('locale')
    if language and language in app.config['LANGUAGES']:
        return language
    
    # locale from user settings
    if g.user:
        language = g.user.get('locale')
        if language and language in app.config['LANGUAGES']:
            return language
        
    # locale from request header
    language = request.headers.get('locale')
    if language and language in app.config['LANGUAGES']:
        return language

    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user() -> Union[Dict, None]:
    """ gets the user logged in """
    try:
        user = int(request.args.get('login_as'))
    except BaseException:
        return None

    return users.get(user)


@app.before_request
def before_request() -> None:
    """ find a user and set it as a global variable """
    g.user = get_user()


@app.route('/', strict_slashes=False)
def home():
    """ home template """
    return render_template('6-index.html', user=g.user)


if __name__ == "__main__":
    app.run()
