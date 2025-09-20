from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
Bootstrap(app)
app.config["SECRET_KEY"] = "dev"

class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    email = EmailField("What is your UofT Email address?", validators=[DataRequired(), Email()])
    submit = SubmitField("Submit")

@app.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        name  = form.name.data.strip()
        email = form.email.data.strip()

        old_name  = session.get("name")
        old_email = session.get("email")
        if old_name and old_name != name:
            flash("Looks like you have changed your name!")
        if old_email and old_email != email:
            flash("Looks like you have changed your email!")

        session["name"] = name 

        if "utoronto" in email.lower():
            session["email"] = email          
            return redirect(url_for("index"))  
        else:
            session.pop("email", None)      
            return render_template(
                "index.html",
                form=form,
                name=session.get("name"),
                email=None,               
                non_uoft=True,
            )

    # GET or invalid form
    return render_template(
        "index.html",
        form=form,
        name=session.get("name"),
        email=session.get("email"),
        non_uoft=False,
    )