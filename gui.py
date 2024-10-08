import sys
import webbrowser
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QDialog, QPushButton, QVBoxLayout, QListWidget, QMessageBox, QScrollBar, QHBoxLayout)

class ApiForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.jobs = []  # Store job details and links
        self.current_page = 0  # Track pagination
        self.isDarkMode = False

    def initUI(self):
        layout = QVBoxLayout()

        # Theme Toggle Button
        self.theme_toggle_button = QPushButton('Toggle Theme', self)
        self.theme_toggle_button.setFixedSize(120, 40)
        self.theme_toggle_button.clicked.connect(self.toggleTheme)

        # Horizontal layout for the theme toggle button (optional)
        header_layout = QHBoxLayout()
        header_layout.addWidget(self.theme_toggle_button)
        header_layout.addStretch()

        # Role
        self.role_label = QLabel('Enter Role:')
        self.role_field = QLineEdit(self)
        
        # Location
        self.location_label = QLabel('Enter Location:')
        self.location_field = QLineEdit(self)

        # Submit Button
        self.submit_button = QPushButton('Submit', self)
        self.submit_button.clicked.connect(self.callApi)

        # List to display array from API
        self.result_list = QListWidget(self)
        self.result_list.itemClicked.connect(self.handleItemClick)  # Connect to item click event
        self.result_list.verticalScrollBar().valueChanged.connect(self.checkScrollPosition)

        # Add widgets to layout
        layout.addLayout(header_layout)  # Add the header layout with theme toggle button
        layout.addWidget(self.role_label)
        layout.addWidget(self.role_field)
        layout.addWidget(self.location_label)
        layout.addWidget(self.location_field)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.result_list)

        # Set layout
        self.setLayout(layout)
        self.setWindowTitle('API Caller')

        # Apply initial light mode stylesheet
        self.setLightMode()

    def setLightMode(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f4f4f4;
                font-family: Arial, sans-serif;
            }
            QLabel {
                font-size: 14px;
                color: #333;
                margin-bottom: 5px;
            }
            QLineEdit {
                padding: 8px;
                font-size: 14px;
                border: 2px solid #ccc;
                border-radius: 5px;
                margin-bottom: 10px;
            }
            QPushButton {
                background-color: #007BFF;
                color: white;
                padding: 10px;
                font-size: 14px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QListWidget {
                padding: 10px;
                border: 2px solid #ccc;
                border-radius: 5px;
                font-size: 14px;
                background-color: #fff;
                margin-top: 10px;
            }
            QListWidget::item {
                padding: 8px;
            }
            QListWidget::item:selected {
                background-color: #007BFF;
                color: white;
            }
        """)

    def setDarkMode(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                font-family: Arial, sans-serif;
            }
            QLabel {
                font-size: 14px;
                color: #f4f4f4;
                margin-bottom: 5px;
            }
            QLineEdit {
                padding: 8px;
                font-size: 14px;
                border: 2px solid #555;
                border-radius: 5px;
                background-color: #333;
                color: #fff;
                margin-bottom: 10px;
            }
            QPushButton {
                background-color: #3a7afe;
                color: white;
                padding: 10px;
                font-size: 14px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #295bc7;
            }
            QListWidget {
                padding: 10px;
                border: 2px solid #555;
                border-radius: 5px;
                font-size: 14px;
                background-color: #2c2c2c;
                color: #fff;
                margin-top: 10px;
            }
            QListWidget::item {
                padding: 8px;
            }
            QListWidget::item:selected {
                background-color: #3a7afe;
                color: white;
            }
        """)

    # Toggle theme between light and dark
    def toggleTheme(self):
        if not self.isDarkMode:
            self.isDarkMode = True
            self.setDarkMode()
        else:
            self.isDarkMode = False
            self.setLightMode()

    def callApi(self): 
        role = self.role_field.text()
        location = self.location_field.text()

        if not role or not location:
            QMessageBox.warning(self, "Input Error", "Please enter both role and location")
            return

        # Call the API with pagination
        try:
            response = requests.get(f'http://127.0.0.1:8000/api/jobs?role={role}&location={location}&page={self.current_page+1}')
            if response.status_code == 200:
                data = response.json()  # Assume the API returns a JSON response
                new_jobs = data if isinstance(data, list) else data.get('result', [])
                if new_jobs:
                    self.jobs.extend(new_jobs)  # Append new job data
                    self.displayResults(new_jobs)
                    self.current_page+=1
                else:
                    QMessageBox.information(self, "No More Results", "No more jobs found.")
            else:
                QMessageBox.warning(self, "API Error", f"Error: {response.status_code}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to call API: {str(e)}")

    def displayResults(self, results):
        # Append new results to the existing list
        for item in results:
            job_title = item.get('title', 'Unknown Job')
            job_company = item.get('company', 'Unknown Company')
            job_location = item.get('location', 'Unknown Location')
            self.result_list.addItem(f'{job_title} By {job_company} At Location {job_location}')  # Add each job title to the list

    def checkScrollPosition(self):
        # Check if the scroll bar has reached the bottom
        scroll_bar = self.result_list.verticalScrollBar()
        if scroll_bar.value() == scroll_bar.maximum():
            self.loadMoreData()

    def loadMoreData(self):
        # Load next page of results
        self.callApi()

    def handleItemClick(self, item):
        selected_job = item.text()  # Get the clicked item text (job title)
        # Find the corresponding job in the jobs list to get the link
        for job in self.jobs:
            if job.get('title') == selected_job.split(' By ')[0]:
                job_link = job.get('link')
                if job_link:
                    self.openDetails(job_link)
                else:
                    QMessageBox.warning(self, "Error", "No link available for this job")
                break

    def openDetails(self, link):
        try:
            response = requests.get(f'http://127.0.0.1:8000/api/jobs/description?url={link}')
            if response.status_code == 200:
                job_details = response.json()  # Parse the JSON response
                self.displayJobDetails(job_details)
            else:
                QMessageBox.warning(self, "API Error", f"Error: {response.status_code}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to get job details: {str(e)}")

    def displayJobDetails(self, job_details):
        details_dialog = QDialog(self)
        details_dialog.setWindowTitle("Job Details")
        details_layout = QVBoxLayout(details_dialog)

        skills = job_details.get('skills required', [])
        seniority = job_details.get('seniority level', 'N/A')
        employment_type = job_details.get('employment type', 'N/A')
        job_function = job_details.get('job function', 'N/A')
        industries = job_details.get('industries', 'N/A')
        job_link = job_details.get('link')

        details_layout.addWidget(QLabel(f"Skills Required: {', '.join(skills)}"))
        details_layout.addWidget(QLabel(f"Seniority Level: {seniority}"))
        details_layout.addWidget(QLabel(f"Employment Type: {employment_type}"))
        details_layout.addWidget(QLabel(f"Job Function: {job_function}"))
        details_layout.addWidget(QLabel(f"Industries: {industries}"))

        button_layout = QHBoxLayout()
        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(lambda: webbrowser.open(job_link))
        button_layout.addWidget(apply_button)

        close_button = QPushButton("Close")
        close_button.clicked.connect(details_dialog.accept)
        button_layout.addWidget(close_button)

        details_layout.addLayout(button_layout)

        details_dialog.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    api_form = ApiForm()
    api_form.show()
    sys.exit(app.exec_())
