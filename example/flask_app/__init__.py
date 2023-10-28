from flask import Flask, flash, redirect, render_template, request, session

from validation import Rules
from validation.errors import ValidationError
from validation.flask_validation.flask_validation import (
    FlaskValidation,
    convert_empty_to_none,
    transform_to_primitive_types,
)
from validation.validation import Validator
from validation.validation_rule import ValidationRule


def validate_age(field, value, fail):
    if value is None or isinstance(value, str):
        return

    if value < 18:
        fail(f"The {field} must be 18 or above")


class AgeRule(ValidationRule):
    def passes(self, field, value):
        self._field = field

        if value is None or isinstance(value, str):
            return

        return value >= 18

    def message(self):
        return f"The {self._field} must be 18 or above"


def create_app():
    app = Flask(__name__)
    validation = FlaskValidation(app)

    # set a secret key for session
    app.secret_key = "secret"

    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            validated = validation.validate(
                rules={
                    "name": [Rules.REQUIRED, Rules.STRING],
                    "age": [Rules.REQUIRED, Rules.INTEGER, AgeRule],
                },
                before_validation=[
                    lambda data: transform_to_primitive_types(["age"], data, int),
                    convert_empty_to_none,
                ],
            )

            session['validated'] = validated

            return redirect("/sucess")

        return render_template("home.html")

    @app.route("/sucess")
    def success_page():
        return render_template("success.html", validated=session.get('validated'))

    return app
