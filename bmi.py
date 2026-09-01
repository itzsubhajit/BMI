from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

app.secret_key = "bmi_project_secret_key"


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        username = request.form.get("username")
        age = request.form.get("age")

        # Store user information for the BMI page
        session["username"] = username
        session["age"] = age

        return redirect(url_for("bmi"))

    return render_template("home.html")


@app.route("/bmi", methods=["GET", "POST"])
def bmi():

    username = session.get("username", "User")
    age = session.get("age", "")

    bmi_score = None
    category = None
    diet = None
    exercise = None
    tips = []

    if request.method == "POST":

        try:
            weight = float(request.form.get("weight"))
            height_cm = float(request.form.get("height"))

            # Convert centimetres to metres
            height_m = height_cm / 100

            # BMI Formula
            bmi_score = weight / (height_m ** 2)

            # Round BMI to 2 decimal places
            bmi_score = round(bmi_score, 2)

            # BMI Categories
            if bmi_score < 18.5:

                category = "Underweight"

                diet = (
                    "Focus on nutrient-dense foods such as milk, eggs, "
                    "nuts, fruits, whole grains, pulses, lean meat, "
                    "and healthy fats."
                )

                exercise = (
                    "Focus on light strength training and resistance exercises "
                    "to build muscle. Allow sufficient recovery and rest."
                )

                tips = [
                    "Do not skip meals.",
                    "Eat nutrient-rich snacks such as nuts and fruits.",
                    "Include protein in your meals.",
                    "Maintain regular meal timings.",
                    "Get sufficient sleep and rest."
                ]

            elif bmi_score < 25:

                category = "Normal Weight"

                diet = (
                    "Maintain a balanced diet containing vegetables, fruits, "
                    "whole grains, lean protein, healthy fats, and sufficient water."
                )

                exercise = (
                    "Continue regular physical activity such as walking, cycling, "
                    "swimming, jogging, and strength training."
                )

                tips = [
                    "Maintain a balanced and varied diet.",
                    "Drink sufficient water throughout the day.",
                    "Exercise regularly.",
                    "Get adequate sleep.",
                    "Maintain a consistent healthy routine."
                ]

            elif bmi_score < 30:

                category = "Overweight"

                diet = (
                    "Focus on balanced portions and nutrient-rich foods such as "
                    "vegetables, fruits, whole grains, and lean protein. "
                    "Avoid extreme dieting."
                )

                exercise = (
                    "Try regular activities such as brisk walking, cycling, "
                    "swimming, and strength training according to your comfort level."
                )

                tips = [
                    "Avoid crash diets.",
                    "Increase your daily physical activity.",
                    "Take regular walks.",
                    "Reduce long periods of sitting.",
                    "Focus on gradual and sustainable lifestyle changes."
                ]

            else:

                category = "Obese"

                diet = (
                    "Focus on gradual and sustainable healthy eating habits. "
                    "Choose nutrient-rich foods and consider consulting a "
                    "qualified healthcare professional for personalised guidance."
                )

                exercise = (
                    "Begin with comfortable low-impact activities such as walking "
                    "or cycling. Increase intensity gradually according to your ability."
                )

                tips = [
                    "Make gradual lifestyle changes.",
                    "Avoid extreme diets and exercise programs.",
                    "Choose comfortable physical activities.",
                    "Prioritise good sleep.",
                    "Consider professional healthcare guidance."
                ]

        except (TypeError, ValueError):

            bmi_score = None
            category = "Invalid Input"

            diet = "Please enter valid numeric values for weight and height."

            exercise = ""

            tips = []

    return render_template(
        "bmi.html",
        username=username,
        age=age,
        bmi=bmi_score,
        category=category,
        diet=diet,
        exercise=exercise,
        tips=tips
    )


if __name__ == "__main__":
    app.run(debug=True)