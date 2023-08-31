# Web Service Templates for the Dundee Resource

## Overview

This project serves as a template for building web-based bioinformatics tools. It provides essential functionalities common to our web servers, such as user input, job submission, and results provision. The template is built on Flask and integrates with Slivka for running bioinformatics tools. This project aims to be a starting point that can be extended and customized for various bioinformatics applications.

## Features

- **User Interface**: A simple interface for file or text-based submissions.
- **Job Submission**: Integration with the Slivka backend for job management.
- **Session Management**: Keeps track of user sessions for job tracking and results provisioning.
- **Extensibility**: Designed to be easily extendable for custom functionalities.

## Project Structure

This project follows a standard Flask application structure and plus the following key components:

- **`config.py`**: Contains all the configuration variables that the app needs. This includes settings like where to find the database and other services.

- **`submission.py`**: Responsible for handling job submissions and processing. It integrates with the Slivka backend for running bioinformatics tools.

- **`session_db.py`**: Manages the database interactions required for session management.

- **`scripts/`**: Contains scripts for maintaining the service in production.

## Prerequisites

- Python 3.11
- Flask
- Slivka
- Other dependencies are listed in `requirements.txt`

## Configuration

Configurations like session storage and logging can be adjusted in `config.py`. Environment variables can also be used to override these settings. Refer to the file for more details.

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/SM_dundee-resource-templates.git
   ```

2. Navigate to the project directory:

   ```bash
   cd SM_dundee-resource-templates
   ```

3. Create a virtual environment:

   ```bash
   python3 -m venv .venv
   ```

4. Activate the virtual environment:

   ```bash
   source .venv/bin/activate
   ```

5. Install the requirements:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the Flask app:

   ```bash
   python app.py
   ```

2. Open your web browser and navigate to `http://localhost:5000`.

3. Follow the interface to submit your bioinformatics job.

## Customization

To add custom functionalities:

1. Extend the classes provided in `submission.py`.
2. Add your processing logic.
3. Update the forms and templates as needed.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Authors

- [**Stuart MacGowan**](https://www.github.com/stuartmac)

## Acknowledgments

- Geoff Barton, [Jim Procter](https://github.com/foreveremain), [Mateusz Warowny](https://www.github.com/warownia1), [James Abbott](https://www.github.com/jamesabbott), Ben Soares and [Javier Sanchez Utges](https://www.github.com/JavierSanchez-Utges) for their contributions to this project and the Dundee Resource.

- This project was developed as part of the [BBSRC](https://www.ukri.org/councils/bbsrc/) funded [Dundee Resource for Protein Structure Prediction and Sequence Analysis](https://gow.bbsrc.ukri.org/grants/AwardDetails.aspx?FundingReference=BB%2fR014752%2f1) (grant number 208391/Z/17/Z).
