
from flask import Flask, render_template, request, send_from_directory
from flask_wtf import FlaskForm
from wtforms import TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired, ValidationError

import datetime
import os
import uuid

from config import UPLOAD_PATH, DOWNLOAD_PATH
from logger_config import setup_logging
from session_db import initialize_db, insert_metadata

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_PATH
app.config['DOWNLOADS_FOLDER'] = DOWNLOAD_PATH

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DOWNLOADS_FOLDER'], exist_ok=True)

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
    form = FastaForm()
    output_file = None

    if form.validate_on_submit():
        # Generate a unique session ID using UUID
        session_id = str(uuid.uuid4())

        # Generate a unique filename using UUID
        unique_filename = str(uuid.uuid4()) + '.fasta'
        
        if form.fasta_file.data:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            form.fasta_file.data.save(file_path)
            with open(file_path, 'r') as f:
                fasta_content = f.read()
        else:
            fasta_content = form.sequence.data

        # Insert metadata into the database
        status = "uploaded"  # Or "processed" based on your logic.
        expiration_time = (datetime.datetime.now() + datetime.timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')  # 7 days from now.
        insert_metadata(session_id, unique_filename, status, expiration_time)
        
        output_content = process_fasta(fasta_content)
        output_file_path = os.path.join(app.config['DOWNLOADS_FOLDER'], unique_filename)
        with open(output_file_path, 'w') as f:
            f.write(output_content)
        
        output_file = unique_filename

    return render_template('index.html', form=form, output_file=output_file)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['DOWNLOADS_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
