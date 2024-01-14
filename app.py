import os
import numpy, random
import json

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///art.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# home/landing page
@app.route("/")
def homepage():
    return render_template("homepage.html")


# a lucky draw for artworks using a random number generator
@app.route("/lucky")
def lucky():
    # extract list containing artwork ids from db
    num_set = db.execute("SELECT artwork_id FROM artworks")
    if not num_set:
        return apology("artwork not found", 400)

    # translate into array of integers
    numbers = [row['artwork_id'] for row in num_set]

    # set range and generate random integer within range
    lowest = min(numbers)
    highest = max(numbers)
    random_id = random.randint(lowest, highest)

    # render the page for the work with that integer ID
    return redirect(url_for("artwork", id=random_id))


# catalog page
@app.route("/catalog")
def catalog():
    # extract information from db, present alphabetically
    list = db.execute("SELECT * FROM artworks ORDER BY name")
    # pass LIST to html page
    return render_template("catalog.html", list=list)


# artwork page(s), generated & rendered based on artwork id
@app.route("/artwork/<int:id>")
@login_required
def artwork(id):
    # extract information for the specified artwork from db
    artwork = db.execute(
        "SELECT * FROM artworks WHERE artwork_id = ?",
        id,
    )
    if not artwork:
        return apology("artwork not found", 400)

    # extract existing user rating for the user in session, if any
    my_rating = db.execute(
        "SELECT rating FROM reviews WHERE user_id = ? AND artwork_id = ? AND rating IS NOT NULL",
        session["user_id"],
        id,
    )
    if not my_rating:
        my_stars = None
    # users are not allowed duplicate reviews, so we can get the unique value we want like so:
    else:
        my_stars = my_rating[0]["rating"]

    # calculate average rating from all users, based on db information
    calc_rating = db.execute(
        "SELECT rating FROM reviews WHERE artwork_id = ? AND rating IS NOT NULL",
        id,
    )
    if not calc_rating:
        avg_rating = None
    else:
        # since the db query returns a list of dicts, we need to translate it to an array of numbers like so:
        array = list(map(lambda d: d["rating"], calc_rating))
        # and then calculate the average, and round to an integer:
        avg_rating = round(numpy.mean(array))

    # extract existing user comment for the user in session, if any
    my_comment = db.execute(
        "SELECT comment FROM reviews WHERE user_id = ? AND artwork_id = ? AND comment IS NOT NULL",
        session["user_id"],
        id,
    )
    if not my_comment:
        show_comment = None
    else:
        show_comment = my_comment

    # extract comments from other users from db, associated with usernames, if any
    other_comment = db.execute(
        "SELECT comment, username FROM reviews JOIN users ON reviews.user_id = users.id WHERE user_id IS NOT ? AND artwork_id = ? AND comment IS NOT NULL",
        session["user_id"],
        id,
    )
    if not other_comment:
        show_other_comment = None
    else:
        show_other_comment = other_comment

    # render template, passing all variables into HTML template
    return render_template(
        "artwork.html",
        artwork=artwork[0],
        my_stars=my_stars,
        avg_rating=avg_rating,
        show_comment=show_comment,
        show_other_comment=show_other_comment,
        # nb this boolean variable will control the status of form buttons
        disable_rating_button=my_stars is not None,
    )


# for users to submit reviews (forms)
@app.route("/review", methods=["GET", "POST"])
@login_required
def review():
    if request.method == "POST":
        # retrieve values from html
        artwork_id = request.form.get("artwork")
        rating = request.form.get("rating")

        # ensure that comment is submitted
        if not request.form.get("comment"):
            flash("please comment")

        # ensure that rating is submitted:
        elif not rating or not (1 <= int(rating) <= 5):
            return apology("please provide rating", 400)

        # store rating and comment in db
        else:
            db.execute(
                "INSERT INTO reviews (user_id, artwork_id, rating, comment) VALUES (?, ?, ?, ?)",
                session["user_id"],
                artwork_id,
                rating,
                request.form.get("comment"),
            )

        return redirect(url_for("artwork", id=artwork_id))

    # if accessed via GET
    else:
        return render_template("artwork.html")


# for users to delete reviews (forms)
@app.route("/deletereview", methods=["GET", "POST"])
@login_required
def deletereview():
    if request.method == "POST":
        # retrieve values from html
        artwork_id = request.form.get("artwork_for_delete")

        # find review via user + artwork in session, delete
        db.execute(
            "DELETE FROM reviews WHERE user_id = ? AND artwork_id = ?",
            session["user_id"],
            artwork_id,
        )

        return redirect(url_for("artwork", id=artwork_id))

    # if accessed via GET
    else:
        return render_template("artwork.html")


# for each user, a page displaying log of reviews
@app.route("/mycollection")
@login_required
def mycollection():
    # extract all reviews for user in session from reviews table, join on artworks table to display artwork information
    log = db.execute(
        "SELECT * FROM reviews JOIN artworks ON reviews.artwork_id = artworks.artwork_id WHERE user_id = ? ORDER BY timestamp",
        session["user_id"],
    )

    # render, passing in the list of dicts
    return render_template("mycollection.html", log=log)


# login
@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/catalog")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


# logout
@app.route("/logout")
@login_required
def logout():
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# register
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure username does not already exist
        elif (
            len(
                db.execute(
                    "SELECT * FROM users WHERE username = ?",
                    request.form.get("username"),
                )
            )
            != 0
        ):
            return apology("username already taken", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password was re-entered
        elif not request.form.get("confirmation"):
            return apology("must provide password", 400)

        # Ensure re-entered password matches first password
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("password must match", 400)

        # Hash password
        hashed = generate_password_hash(
            request.form.get("password"), method="scrypt", salt_length=16
        )
        # Insert new user into users database
        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            request.form.get("username"),
            hashed,
        )

        # Automatically log new user in
        # Retrieve user
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/catalog")

    # User reached route via GET (as in by clicking a link or via redirect)
    else:
        return render_template("register.html")


# change password
@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure old password was submitted
        elif not request.form.get("old_password"):
            return apology("must provide old password", 400)

        # Ensure new password was submitted
        elif not request.form.get("new_password"):
            return apology("must provide new password", 400)

        # Find information of current user in preparation for verification
        user_info = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        if not user_info:
            return apology("incorrect username", 400)

        # Ensure the proclaimed username is in session
        if not user_info[0]["id"] == session["user_id"]:
            return apology("incorrect username", 400)

        # Ensure old password is correct
        elif not check_password_hash(
            user_info[0]["hash"], request.form.get("old_password")
        ):
            return apology("incorrect password", 400)

        # Ensure new password is different
        elif request.form.get("new_password") == request.form.get("old_password"):
            return apology("new password must be different", 400)

        # Hash new password
        hashed = generate_password_hash(
            request.form.get("new_password"), method="scrypt", salt_length=16
        )

        # Update password in users db
        db.execute("UPDATE users SET hash = ? WHERE id = ?", hashed, session["user_id"])

        # Redirect user to home page
        flash("Password change successful")
        return redirect("/catalog")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("password.html")
