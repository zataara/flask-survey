from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []
RESPONSES_KEY = "responses"

@app.route('/')
def show_surveys():
    '''select a survey to complete'''
    return render_template('index.html', survey=survey)


@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the session of responses."""

    session[RESPONSES_KEY] = []

    return redirect("/questions/0")

@app.route('/questions/<int:qid>')
def show_questions(qid):
    '''Display the current questions'''
    responses = session.get(RESPONSES_KEY)

    if(responses is None):
        # stops user from trying to access question manually through url
        return redirect('/')

    if(len(responses) == len(survey.questions)):
        # stops user from tyring to access questions after survey is complete
        return redirect('/complete')

    if(len(responses) != qid):
        # stops user from accessing questions out of order
        flash(f"Invalid QuestionID:{qid}")
        return redirect(f'questions/{len(responses)}')
    
    question = survey.questions[qid]
    return render_template('questions.html', question_num=qid, question=question)


@app.route('/answer', methods=['POST'])
def handle_questions():
    '''renders next question after current one is answered'''
    choice = request.form['answer']

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        return redirect('/complete')

    else:
        return redirect(f'/questions/{len(responses)}')


@app.route('/complete')
def done():
    return render_template('complete.html')
