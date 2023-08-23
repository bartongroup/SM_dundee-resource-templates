
from flask import Flask, render_template, request, send_from_directory
from flask_wtf import FlaskForm
from wtforms import TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired, ValidationError
import os

from config import UPLOAD_PATH, DOWNLOAD_PATH
from logger_config import setup_logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_PATH
app.config['DOWNLOADS_FOLDER'] = UPLOAD_PATH

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['DOWNLOADS_FOLDER']):
    os.makedirs(app.config['DOWNLOADS_FOLDER'])

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
        if form.fasta_file.data:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], form.fasta_file.data.filename)
            form.fasta_file.data.save(file_path)
            with open(file_path, 'r') as f:
                fasta_content = f.read()
        else:
            fasta_content = form.sequence.data
        
        output_content = process_fasta(fasta_content)
        output_file_path = os.path.join(app.config['DOWNLOADS_FOLDER'], 'output.fasta')
        with open(output_file_path, 'w') as f:
            f.write(output_content)
        
        output_file = 'output.fasta'

    return render_template('index.html', form=form, output_file=output_file)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['DOWNLOADS_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
