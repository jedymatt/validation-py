from flask import Flask, redirect, render_template, request, session

from flask_validation import (
    FlaskValidation,
    convert_empty_to_none,
    transform_to_primitive_types,
)
from validation import Rules
from validation.base import Rule
from validation.rules import conditional_rule


def validate_age(field, value, fail):
    if value is None or isinstance(value, str):
        return

    if value < 18:
        fail(f"The {field} must be 18 or above")


class AgeRule(Rule):
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
    @validation.exclude_from_session("password")
    def home():
        if request.method == "POST":
            validated = validation.validate(
                rules={
                    "name": [
                        Rules.required,
                        Rules.string,
                        [Rules.min, 3],
                    ],
                    "age": [
                        Rules.required,
                        Rules.integer,
                        AgeRule,
                        validate_age,
                    ],
                    "password": [Rules.required, Rules.string],
                },
                before_validation=[
                    lambda data: transform_to_primitive_types(["age"], data, int),
                    convert_empty_to_none,
                ],
            )

            session["validated"] = validated

            return redirect("/sucess")

        return render_template("home.html")

    @app.route("/sucess")
    def success_page():
        return render_template("success.html", validated=session.get("validated"))

    return app
