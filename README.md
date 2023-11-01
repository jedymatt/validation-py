# validation-py

Inspired from Laravel's validation

Features:
- Custom rules
-  flask support


## Getting Started


```sh
pip intall https://github.com/jedymatt/validation-py@<tag>
```


## Basic Usage

```py
data = {'name': 'John Doe', 'age': 18}
```

```py
from validator.rules import Rules


validator = Validator(data, rules={
        "name": [Rules.required, Rules.string],
        "age": [Rules.required, Rules.integer],
    })

if validator.fails():
    errors = validator.errors() # error messages

validated = validator.validated() # validated data

```

```py
from validator.rules import Rules


validated = Validator(data, rules={
        "name": [Rules.required, Rules.string],
        "age": [Rules.required, Rules.integer],
    }).validate() # immediately raise ValidationError when fails 

```


## Custom Rules

As function

```py
def validate_age(field, value, fail):
    if value is None or isinstance(value, str):
            return

    if value < 18:
        fail(f"The {field} must be 18 or above")

```

As class

```py
from validation.validation_rule import ValidationRule


class AgeRule(ValidationRule):
    def passes(self, field, value):
        self._field = field

        if value is None or isinstance(value, str):
            return

        return value >= 18

    def message(self):
        return f"The {self._field} must be 18 or above"
```


## How to use with Flask

Go to `example/flask_app` for more info

```py
# ...
from validation import Rules
from flask_validation import (
    FlaskValidation,
    convert_empty_to_none,
    transform_to_primitive_types,
)
from validation.validation_rule import ValidationRule


app = Flask(__name__)
validation = FlaskValidation(app)

# set a secret key for session
app.secret_key = "secret" 

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        validated = validation.validate(
            rules={
                "name": [Rules.required, Rules.string, [Rules.min, 3]],
                "age": [Rules.required, Rules.integer, AgeRule], # AgeRule is a custom Rule class
            },
            before_validation=[
                lambda data: transform_to_primitive_types(["age"], data, int),
                convert_empty_to_none,
            ],
        )

        session['validated'] = validated

        return redirect("/sucess")

    return render_template("home.html")
```

To know how to access error messages, and old field values, check out `example/flask_app/templates/home.html`
```py
# to get all errors
error()
# to get value by key, defaults to "" empty string
error('name')


# get all old values, see the `example/flask_app/templates/home.html` on its uses
# same as above
old()
old('name')
```

To protect sensitive fields, you can add `exclude_from_session` decorator on your route method
```py
from validation.flask_validation


app = Flask(__name__)
validation = FlaskValidation(app)


@app.route('/home')
@validation.exclude_from_session("password", "token", "..")
def home():
    """perform validation here"""
```

## How to Contribute?

Since this package is new, you can contribute by adding validation for email, float, array, password, and so on. To make it rest API friendly, make the validation error, returned as json, customizable.


### To-Do Rules

- list
- dict
- float
