from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from utils.image_api import get_place_image

app = Flask(__name__)

# Load Tourist Dataset
df = pd.read_csv("database/final_tourist_places.csv")


# ---------------- Login ----------------
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # Fixed Login Credentials
        if username == "rithika" and password == "AITourist@2026":
            return redirect(url_for("dashboard"))

        else:
            return render_template(
                "login.html",
                error="Invalid Username or Password"
            )

    return render_template("login.html")


# ---------------- Dashboard ----------------
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# ---------------- Recommendation ----------------
@app.route("/recommend")
def recommend():

    # Get unique states
    states = sorted(df["State"].dropna().unique())

    # Get unique tourist categories
    categories = sorted(df["Type"].dropna().unique())

    return render_template(
        "recommend.html",
        states=states,
        categories=categories
    )


# ---------------- Result ----------------
@app.route("/result", methods=["POST"])
def result():

    state = request.form["state"]
    category = request.form["category"]
    season = request.form["best_time"]

    print("Selected State:", state)
    print("Selected Category:", category)
    print("Selected Season:", season)

    # 1. Search by State + Category + Best Time
    filtered_df = df[
        (df["State"] == state) &
        (df["Type"] == category) &
        (df["Best Time to visit"] == season)
    ]

    # 2. If no result, search by State + Category
    if filtered_df.empty:
       filtered_df = df[
          (df["State"] == state) &
          (df["Type"] == category)
        ]

    # 3. If still no result, search only by State
    if filtered_df.empty:
       filtered_df = df[
         df["State"] == state
       ]

    print(filtered_df)
    print("Number of rows:", len(filtered_df))

    # If no exact match, search only by state
    if filtered_df.empty:
        filtered_df = df[df["State"] == state]

    # Default values
    place = None
    image_url = None

    # If a place is found
    if not filtered_df.empty:
      place = filtered_df.iloc[0]

    # Get tourist image from Pexels
    image_url = get_place_image(place["Name"])

    print("Place:", place["Name"])
    print("Image URL:", image_url)

    return render_template(
        "result.html",
        place=place,
        state=state,
        category=category,
        season=season,
        image_url=image_url
    )

# ---------------- About ----------------
@app.route("/about")
def about():
    return render_template("about.html")

# ---------------- Contact ----------------
@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)