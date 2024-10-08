# Skillscraper - How to Run the Application

## Prerequisites

Before running the application, ensure you have Python installed on your machine. The application includes a FastAPI backend and a PyQt5 GUI, which you'll need to run in separate terminals.

## Step 1: Set Up a Virtual Environment

1. Open your terminal and navigate to the project directory.
2. Create a virtual environment by running the following command:

   ```bash
   python -m venv venv
   ```
Activate the virtual environment:

Windows:
```bash
venv\Scripts\activate
```
macOS/Linux:

```bash
source venv/bin/activate
```
## Step 2: Install Required Libraries
Once the virtual environment is activated, install the necessary libraries:

```bash
pip install beautifulsoup4 fastapi spacy pyqt5 requests webbrowser
```
## Step 3: Run the Application
1. Start the API
In the first terminal, start the FastAPI server by running:

```bash
uvicorn api:app --reload
```
This will start the FastAPI server at http://127.0.0.1:8000.

2. Run the GUI
In a new terminal (with the virtual environment still activated), run the PyQt5 GUI:

```bash
python gui.py
```
This will launch the Skillscraper application's graphical interface.