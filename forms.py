from flask_wtf import FlaskForm
from wtforms import TextAreaField, FileField, SubmitField

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
