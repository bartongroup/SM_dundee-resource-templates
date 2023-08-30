
from flask import Flask, render_template, request, send_from_directory, session, redirect, url_for
from wtforms.validators import DataRequired, ValidationError

import os
import uuid
from datetime import datetime, timedelta

from config import SESSIONS_FOLDER
from filters import datetime_parse, datetime_format
from forms import FastaForm
from logger_config import setup_logging
from session_db import initialize_db, fetch_results
from submission import SubmissionHandler

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

os.makedirs(SESSIONS_FOLDER, exist_ok=True)

initialize_db()

custom_logger = setup_logging(name='app')

# Register the filters
app.jinja_env.filters['datetime_parse'] = datetime_parse
app.jinja_env.filters['datetime_format'] = datetime_format

@app.route('/', methods=['GET', 'POST'])
def index():
    # Check if session_id exists, create one if not
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    
    session_id = session['session_id']

    form = FastaForm()
    output_file = None

    if form.validate_on_submit():
        submission_handler = SubmissionHandler(session_id, form)
        result = submission_handler.handle_submission()
        output_file = result['filename']

        # Redirect to the results page after processing
        return redirect(url_for('results', session_id=session_id))
    
    return render_template('index.html', form=form, output_file=output_file)

@app.route('/download/<session_id>/<submission_time>/<filename>')
def download(session_id, submission_time, filename):
    directory = os.path.join(SESSIONS_FOLDER, session_id, submission_time)
    return send_from_directory(directory=directory, path=filename, as_attachment=True)

@app.route('/results/<session_id>', methods=['GET'])
def results(session_id):
    # Fetch results based on the session ID
    results = fetch_results(session_id)
    return render_template('results.html', results=results, session_id=session_id,
                           current_time=datetime.now(), timedelta_24h=timedelta(days=1))


if __name__ == '__main__':
    app.run(debug=True)
