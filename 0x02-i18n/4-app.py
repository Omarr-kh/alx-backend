#!/usr/bin/env python3
""" Flask Application """
from flask import Flask, render_template, request
from flask_babel import Babel

app = Flask(__name__)


class Config:
    """ Configuration class """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    """ determine the best match with our supported languages """
    language = request.args.get('locale')
    if language and language in app.config['LANGUAGES']:
        return language
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def home():
    """ home template """
    return render_template("4-index.html")


if __name__ == "__main__":
    app.run()
