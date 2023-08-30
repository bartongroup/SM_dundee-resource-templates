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
        self.submission_time = datetime.now()
        self.session_directory = self.create_directory()
        self.submission_directory = self.create_submission_directory()
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
    
    def create_submission_directory(self):
        """Create a unique directory for each submission."""
        timestamp = self.submission_time.strftime('%Y%m%d%H%M%S')
        submission_directory = os.path.join(self.session_directory, f"{timestamp}")
        os.makedirs(submission_directory, exist_ok=True)
        custom_logger.debug(f"Directory created for submission {self.session_id}/{timestamp}.")
        return submission_directory
    
    def save_submission_data(self):
        """Save the uploaded FASTA file or the input sequence."""
        if self.form.fasta_file.data:
            self.fasta_filename = self.form.fasta_file.data.filename
            self.file_path = os.path.join(self.submission_directory, self.fasta_filename)
            self.form.fasta_file.data.save(self.file_path)
        else:
            self.fasta_filename = 'sequence.fasta'
            self.file_path = os.path.join(self.submission_directory, self.fasta_filename)
            with open(self.file_path, 'w') as f:
                f.write(self.form.sequence.data)
        custom_logger.info(f"FASTA data saved for session {self.session_id}.")

    def store_submission_metadata(self):
        """Insert metadata related to the submission into the database."""
        expiration_time = (self.submission_time + timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
        insert_metadata(self.session_id, self.fasta_filename, 'output.fasta', self.submission_time.strftime('%Y-%m-%d %H:%M:%S'), 'uploaded', expiration_time)
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
        processor = FastaProcessor()
        output_file_path = os.path.join(self.submission_directory, 'output.fasta')
        success = processor.process(self.file_path, output_file_path)


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


class FastaProcessor:
    """Handles the processing of FASTA files."""

    @staticmethod
    def process(input_file_path, output_file_path):
        """Process the given FASTA file.

        Args:
            input_file_path (str): The path to the input FASTA file.
            output_file_path (str): The path where the output should be saved.

        Returns:
            bool: True if processing was successful, False otherwise.
        """
        try:
            # Dummy function: Replace this with your actual processing logic
            delay = 0
            custom_logger.info(f"Processing FASTA file. This will take {delay} seconds.")
            sleep(delay)

            with open(input_file_path, 'r') as infile:
                content = infile.read()

            processed_content = content.lower()

            with open(output_file_path, 'w') as outfile:
                outfile.write(processed_content)
            
            return True
        except Exception as e:
            custom_logger.error(f"An error occurred while processing the FASTA file: {str(e)}")
            return False
