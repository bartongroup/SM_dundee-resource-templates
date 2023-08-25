
from flask import Flask, render_template, request, send_from_directory, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired, ValidationError

import datetime
import os
import uuid

from config import SESSIONS_FOLDER
from logger_config import setup_logging
from session_db import initialize_db, insert_metadata, update_status, fetch_results

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSIONS_FOLDER'] = SESSIONS_FOLDER

os.makedirs(app.config['SESSIONS_FOLDER'], exist_ok=True)

initialize_db()

custom_logger = setup_logging()

class FastaForm(FlaskForm):
    sequence = TextAreaField('Enter FASTA Sequence')
    fasta_file = FileField('Or Upload a FASTA File')
    submit = SubmitField('Submit')

    # Custom validator
    def validate(self, extra_validators=None):
        # Use the default validate method first
        initial_validation = super(FastaForm, self).validate(extra_validators=extra_validators)
        
        # If the initial validation passes and either sequence or fasta_file has data, return True
        if initial_validation and (self.sequence.data or self.fasta_file.data):
            return True
        
        # If neither field has data, add a form-wide error
        if not self.sequence.data and not self.fasta_file.data:
            self.sequence.errors.append('Either enter a FASTA sequence or upload a FASTA file.')
            return False
        
        return False

def process_fasta(fasta_content):
    # Dummy function: you can replace this with any processing function you need
    return fasta_content.lower()

@app.route('/', methods=['GET', 'POST'])
def index():
    # Check if session_id exists, create one if not
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    
    session_id = session['session_id']

    form = FastaForm()
    output_file = None

    if form.validate_on_submit():
        # Generate a unique session ID using UUID
        session_directory = os.path.join(app.config['SESSIONS_FOLDER'], session_id)
        os.makedirs(session_directory, exist_ok=True)
        
        if form.fasta_file.data:
            # Save the uploaded file to the session folder
            fasta_filename = form.fasta_file.data.filename
            file_path = os.path.join(session_directory, fasta_filename)
            form.fasta_file.data.save(file_path)
        else:
            # Save the sequence input to a file in the session folder
            fasta_filename = 'sequence.fasta'
            file_path = os.path.join(session_directory, fasta_filename)
            with open(file_path, 'w') as f:
                f.write(form.sequence.data)

        # Insert metadata into the database
        status = "uploaded"  # Or "processed" based on your logic.
        expiration_time = (datetime.datetime.now() + datetime.timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')  # 7 days from now.
        insert_metadata(session_id, fasta_filename, status, expiration_time)

        # Read the FASTA file
        with open(file_path, 'r') as f:
            fasta_content = f.read()
        
        # Process the FASTA file and save the output to the downloads folder
        output_content = process_fasta(fasta_content)
        output_file_path = os.path.join(session_directory, 'output.fasta')
        with open(output_file_path, 'w') as f:
            f.write(output_content)

        # Update the status in the database
        update_status(session_id, fasta_filename, "processed")
        
        output_file = fasta_filename

        # Redirect to the results page after processing
        return redirect(url_for('results'))
    
    return render_template('index.html', form=form, output_file=output_file)

@app.route('/download/<session_id>/<filename>')
def download(session_id, filename):
    directory = os.path.join(app.config['SESSIONS_FOLDER'], session_id)
    return send_from_directory(directory=directory, path=filename, as_attachment=True)

@app.route('/results', methods=['GET'])
def results():
    # Fetch results based on the current session ID
    results = fetch_results(session['session_id'])

    # Render the results page
    return render_template('results.html', results=results, session_id=session['session_id'])

if __name__ == '__main__':
    app.run(debug=True)
