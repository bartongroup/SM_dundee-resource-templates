
from flask import Flask, render_template, request, send_from_directory, session, redirect, url_for
from wtforms.validators import DataRequired, ValidationError
from werkzeug.utils import secure_filename

import os
import uuid
from datetime import datetime, timedelta

from config import SESSIONS_FOLDER
from filters import datetime_parse, datetime_format
from forms import FastaForm
from logger_config import setup_logging
from session_db import initialize_db, fetch_results
from submission import SubmissionHandler
from utils.validation import is_valid_session_id, is_valid_submission_time

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
    # Validate session_id and submission_time
    if not is_valid_session_id(session_id) or not is_valid_submission_time(submission_time):
        return "Invalid input", 400

    # Sanitize filename
    sanitized_filename = secure_filename(filename)

    directory = os.path.join(SESSIONS_FOLDER, session_id, submission_time)
    file_path = os.path.join(directory, sanitized_filename)

    # Ensure the file_path is within the expected directory
    if not file_path.startswith(SESSIONS_FOLDER):
        return "Invalid file path", 400

    # Check if the file exists before sending it
    if os.path.exists(file_path):
        return send_from_directory(directory=directory, path=sanitized_filename, as_attachment=True)
    else:
        return "File not found", 404


@app.route('/results/<session_id>', methods=['GET'])
def results(session_id):
    # Fetch results based on the session ID
    results = fetch_results(session_id)
    return render_template('results.html', results=results, session_id=session_id,
                           current_time=datetime.now(), timedelta_24h=timedelta(days=1))


if __name__ == '__main__':
    app.run(debug=True)
