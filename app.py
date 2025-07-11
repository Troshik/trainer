from flask import Flask, render_template, request, redirect, url_for, session
from training_plan import generate_training_plan


app = Flask(__name__)
app.secret_key = '1234'


@app.route("/", methods=["GET", "POST"])
def index():
    plan = None
    show_form = True
    history = session.get("history", [])

    if request.method == "POST":
        user_profile = {
            "goal": request.form["goal"],
            "fitness_level": request.form["level"],
            "available_time_min": int(request.form["time"])
        }
        plan = generate_training_plan(user_profile, history)
        show_form = False

    return render_template("index.html", plan=plan, show_form=show_form)


@app.route("/checkin", methods=["GET", "POST"])
def checkin():
    if request.method == "POST":
        completed = request.form.getlist("completed")
        history = session.get("history", [])
        history.extend(completed)
        session["history"] = history
        return render_template("index.html", plan=None, show_form=True, completed=completed)
    else:
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
