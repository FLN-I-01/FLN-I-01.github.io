# Optimal Samples Selection System

This system allows users to select optimal sample combinations based on various parameters. It provides both a web interface and database storage for managing results.

## Features

- User-friendly web interface
- Parameter validation for m, n, k, j, and s
- Support for both random and manual number input
- Database storage for results
- View and delete saved results
- Responsive design that works on mobile devices

## Requirements

- Python 3.7 or higher
- Flask
- Flask-SQLAlchemy
- NumPy
- Pandas

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Unix/MacOS:
     ```bash
     source venv/bin/activate
     ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Make sure your virtual environment is activated
2. Run the Flask application:
   ```bash
   python app.py
   ```
3. Open your web browser and navigate to `http://localhost:5000`

## Usage

1. Enter the required parameters:
   - m (45-54): Total number of samples
   - n (7-25): Number of samples to select
   - k (4-7): Size of groups to form
   - j: Number of samples to consider (must be ≥s and ≤k)
   - s (3-7): Number of samples that must be selected

2. Optionally enter custom numbers (comma-separated) or let the system generate random numbers

3. Click "Generate Results" to create optimal sample groups

4. View and manage saved results in the right panel

## File Naming Convention

Results are saved with the following format:
`m-n-k-j-s-x-y`
where:
- x is the run number
- y is the number of results obtained

## Database

Results are stored in an SQLite database (`samples.db`) with the following information:
- Parameters (m, n, k, j, s)
- Run number
- Result count
- Generated combinations
- Timestamp
