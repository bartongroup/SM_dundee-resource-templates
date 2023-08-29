from datetime import datetime, timedelta
from time import sleep

import os

from config import SESSIONS_FOLDER
from logger_config import setup_logging
from session_db import insert_metadata, update_status

custom_logger = setup_logging(name='submission')

class SubmissionHandler:
    """Handles FASTA file submissions and associated processing."""

    def __init__(self, session_id, form):
        """Initialize a SubmissionHandler instance.

        Args:
            session_id (str): Unique identifier for the submission session.
            form (FlaskForm): Form object containing the submission details.
        """
        self.session_id = session_id
        self.form = form
        self.session_directory = self.create_directory()
        self.fasta_filename = None
        self.file_path = None

    def create_directory(self):
        """Create a directory for the submission session.

        Returns:
            str: The path to the created directory.
        """
        session_directory = os.path.join(SESSIONS_FOLDER, self.session_id)
        os.makedirs(session_directory, exist_ok=True)
        custom_logger.debug(f"Directory created for session {self.session_id}.")
        return session_directory
    
    def save_submission_data(self):
        """Save the uploaded FASTA file or the input sequence."""
        if self.form.fasta_file.data:
            self.fasta_filename = self.form.fasta_file.data.filename
            self.file_path = os.path.join(self.session_directory, self.fasta_filename)
            self.form.fasta_file.data.save(self.file_path)
        else:
            self.fasta_filename = 'sequence.fasta'
            self.file_path = os.path.join(self.session_directory, self.fasta_filename)
            with open(self.file_path, 'w') as f:
                f.write(self.form.sequence.data)
        custom_logger.info(f"FASTA data saved for session {self.session_id}.")

    def store_submission_metadata(self):
        """Insert metadata related to the submission into the database."""
        expiration_time = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
        insert_metadata(self.session_id, self.fasta_filename, 'output.fasta', 'uploaded', expiration_time)
        custom_logger.info(f"Metadata inserted into database for session {self.session_id}.")

    def read_cached_submission(self):
        """Read the saved FASTA file.

        Returns:
            str: The content of the FASTA file.
        """
        with open(self.file_path, 'r') as f:
            return f.read()

    def process_and_save_results(self, fasta_content):
        """Process the FASTA file content and save the results."""
        output_content = process_fasta(fasta_content)
        output_file_path = os.path.join(self.session_directory, 'output.fasta')
        with open(output_file_path, 'w') as f:
            f.write(output_content)

    def update_db_status(self):
        """Update the processing status in the database."""
        update_status(self.session_id, self.fasta_filename, "processed")
        custom_logger.info(f"FASTA file processed and status updated for session {self.session_id}.")

    def handle_submission(self):
        """Handle the submission by orchestrating the various steps.

        Returns:
            dict: A dictionary containing the status, message, and other details of the submission.
        """
        result = {'status': 'failed', 'message': '', 'filename': None}

        try:
            self.save_submission_data()
            self.store_submission_metadata()
            fasta_content = self.read_cached_submission()
            self.process_and_save_results(fasta_content)
            self.update_db_status()
            result.update({
                'status': 'success',
                'message': 'File processed successfully.',
                'directory': self.session_directory,
                'filename': self.fasta_filename
            })
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
