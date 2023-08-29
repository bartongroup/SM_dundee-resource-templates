from datetime import datetime, timedelta
from time import sleep

import os

from config import SESSIONS_FOLDER
from logger_config import setup_logging
from session_db import insert_metadata, update_status

custom_logger = setup_logging(name='submission')

class SubmissionHandler:

    def __init__(self, session_id, form):
        self.session_id = session_id
        self.form = form
        self.session_directory = self.create_directory()
    
    def create_directory(self):
        # Create a directory for the submission
        session_directory = os.path.join(SESSIONS_FOLDER, self.session_id)
        os.makedirs(session_directory, exist_ok=True)
        custom_logger.debug(f"Directory created for session {self.session_id}.")
        return session_directory
    
    def save_fasta_file(self):
        if self.form.fasta_file.data:
            fasta_filename = self.form.fasta_file.data.filename
            file_path = os.path.join(self.session_directory, fasta_filename)
            self.form.fasta_file.data.save(file_path)
            custom_logger.info(f"FASTA file uploaded for session {self.session_id}.")
        else:
            fasta_filename = 'sequence.fasta'
            file_path = os.path.join(self.session_directory, fasta_filename)
            with open(file_path, 'w') as f:
                f.write(self.form.sequence.data)
            custom_logger.info(f"Sequence data saved for session {self.session_id}.")
        return fasta_filename, file_path

    def insert_db_metadata(self, fasta_filename):
        insert_metadata(self.session_id, fasta_filename, 'output.fasta', 'uploaded', 
                            (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S'))
        custom_logger.info(f"Metadata inserted into database for session {self.session_id}.")

    def read_fasta_file(self, file_path):
        with open(file_path, 'r') as f:
            fasta_content = f.read()
        return fasta_content

    def process_and_save_results(self, fasta_content):
        output_content = process_fasta(fasta_content)
        output_file_path = os.path.join(self.session_directory, 'output.fasta')
            
        with open(output_file_path, 'w') as f:
            f.write(output_content)

    def update_db_status(self, fasta_filename):
        update_status(self.session_id, fasta_filename, "processed")
        custom_logger.info(f"FASTA file processed and status updated for session {self.session_id}.")

    def handle_submission(self):        
        result = {'status': 'failed', 'message': '', 'filename': None}
        
        try:
            fasta_filename, file_path = self.save_fasta_file()

            self.insert_db_metadata(fasta_filename)

            fasta_content = self.read_fasta_file(file_path)

            self.process_and_save_results(fasta_content)
            
            self.update_db_status(fasta_filename)

            # Return the result
            result['status'] = 'success'
            result['message'] = 'File processed successfully.'
            result['directory'] = self.session_directory
            result['filename'] = fasta_filename
            
        except Exception as e:
            custom_logger.error(f"An error occurred while handling submission for session {self.session_id}: {str(e)}")
            result['status'] = 'failed'
            result['message'] = str(e)
        
        return result


def process_fasta(fasta_content):
    # Dummy function: you can replace this with any processing function you need
    delay = 5
    custom_logger.info(f"Processing FASTA file. This will take {delay} seconds.")
    sleep(delay)
    return fasta_content.lower()
