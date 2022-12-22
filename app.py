from flask import Flask, render_template, redirect, flash, session, request
from surveys import satisfaction_survey as survey
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route('/')
def survey_start():

    return render_template("survey_start.html", survey=survey)


@app.route("/begin", methods=["POST"])
def start_survey():

    session[RESPONSES_KEY] = []

    return redirect("/questions/0")


@app.route('/answer', methods=["POST"])
def questions_handle():

    choice = request.form['answer']

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        
        return redirect("/complete")
    
    else:
        return redirect(f"/questions/{len(responses)}")


@app.route('/questions/<int:num>')
def question_pages(num):

    responses = session.get(RESPONSES_KEY)

    if(responses is None):
        return redirect('/')

    if(len(responses) >= len(survey.questions)):
        return redirect('/complete')
    
    if (len(responses) !=num):
        flash(f"Invalid question ID: {num}")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[num]
    return render_template("questions.html", question_count=num, question=question, survey=survey)


@app.route('/complete')
def survey_complete():

    return render_template('complete.html')
    
