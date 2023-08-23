
from flask import Flask, render_template, request, send_from_directory
from flask_wtf import FlaskForm
from wtforms import TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads/'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

class FastaForm(FlaskForm):
    sequence = TextAreaField('Enter FASTA Sequence', validators=[DataRequired()])
    fasta_file = FileField('Or Upload a FASTA File')
    submit = SubmitField('Submit')

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
        output_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.fasta')
        with open(output_file_path, 'w') as f:
            f.write(output_content)
        
        output_file = 'output.fasta'

    return render_template('index.html', form=form, output_file=output_file)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
