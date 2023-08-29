from datetime import datetime, timedelta
from time import sleep

import os

from config import SESSIONS_FOLDER
from logger_config import setup_logging
from session_db import insert_metadata, update_status

custom_logger = setup_logging()

class SubmissionHandler:

    def __init__(self, session_id, form):
        self.session_id = session_id
        self.form = form
    
    def create_directory(self):
        # Create a directory for the submission
        session_directory = os.path.join(SESSIONS_FOLDER, self.session_id)
        os.makedirs(session_directory, exist_ok=True)
        self.session_directory = session_directory

    def handle_submission(self):
        
        self.create_directory()

        if self.form.fasta_file.data:
            # Save the uploaded file to the session folder
            fasta_filename = self.form.fasta_file.data.filename
            file_path = os.path.join(self.session_directory, fasta_filename)
            self.form.fasta_file.data.save(file_path)
        else:
            # Save the sequence input to a file in the session folder
            fasta_filename = 'sequence.fasta'
            file_path = os.path.join(self.session_directory, fasta_filename)
            with open(file_path, 'w') as f:
                f.write(self.form.sequence.data)

        # Insert metadata into the database
        status = "uploaded"  # Or "processed" based on your logic.
        expiration_time = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')  # 7 days from now.
        results_filename = 'output.fasta'
        insert_metadata(self.session_id, fasta_filename, results_filename, status, expiration_time)

        # Read the FASTA file
        with open(file_path, 'r') as f:
            fasta_content = f.read()
            
        # Process the FASTA file and save the output to the downloads folder
        output_content = process_fasta(fasta_content)
        output_file_path = os.path.join(self.session_directory, results_filename)
        with open(output_file_path, 'w') as f:
            f.write(output_content)

        # Update the status in the database
        update_status(self.session_id, fasta_filename, "processed")
        return fasta_filename


def process_fasta(fasta_content):
    # Dummy function: you can replace this with any processing function you need
    delay = 5
    custom_logger.info(f"Processing FASTA file. This will take {delay} seconds.")
    sleep(delay)
    return fasta_content.lower()
