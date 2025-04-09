import sys
import json
from datetime import datetime, timedelta
from collections import defaultdict
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QComboBox, QSlider, QPushButton, 
                            QFrame, QDialog, QLineEdit, QTextEdit, QMessageBox,
                            QCalendarWidget, QGroupBox, QGridLayout)
from PyQt5.QtCore import Qt, QDate
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class CalendarDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Date")
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Create calendar widget
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        
        # Set the minimum date to 30 days ago and maximum date to today
        today = QDate.currentDate()
        self.calendar.setMaximumDate(today)
        self.calendar.setMinimumDate(today.addDays(-30))
        
        # Highlight current week
        self.highlight_current_week()
        
        # Button layout
        button_layout = QHBoxLayout()
        select_btn = QPushButton("Select")
        cancel_btn = QPushButton("Cancel")
        
        select_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(select_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addWidget(self.calendar)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def highlight_current_week(self):
        # Get the current date
        current_date = QDate.currentDate()
        
        # Get the first day of the week (Monday)
        start_of_week = current_date.addDays(-(current_date.dayOfWeek() - 1))
        
        # Set a format for the current week
        format = self.calendar.dateTextFormat(QDate())
        format.setBackground(Qt.darkGray)
        
        # Apply the format to each day of the current week
        for i in range(7):
            self.calendar.setDateTextFormat(start_of_week.addDays(i), format)
    
    def get_selected_date(self):
        return self.calendar.selectedDate().toString("yyyy-MM-dd")

class NewProjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Project")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Project Name
        name_layout = QHBoxLayout()
        self.name_label = QLabel("Project Name:")
        self.name_label.setStyleSheet("color: black;")
        self.name_input = QLineEdit()
        name_layout.addWidget(self.name_label)
        name_layout.addWidget(self.name_input)
        
        # Account Number
        account_layout = QHBoxLayout()
        self.account_label = QLabel("Account Number:")
        self.account_label.setStyleSheet("color: black;")
        self.account_input = QLineEdit()
        account_layout.addWidget(self.account_label)
        account_layout.addWidget(self.account_input)
        
        # Comments
        comments_layout = QHBoxLayout()
        self.comments_label = QLabel("Comments:")
        self.comments_label.setStyleSheet("color: black;")
        self.comments_input = QLineEdit()
        comments_layout.addWidget(self.comments_label)
        comments_layout.addWidget(self.comments_input)
        
        # Add Project Button
        self.add_button = QPushButton("Add Project")
        self.add_button.setStyleSheet("color: black;")
        self.add_button.clicked.connect(self.accept)
        
        # Add all layouts to main layout
        layout.addLayout(name_layout)
        layout.addLayout(account_layout)
        layout.addLayout(comments_layout)
        layout.addWidget(self.add_button)
        
        self.setLayout(layout)

    def get_project_data(self):
        return {
            "name": self.name_input.text(),
            "account_number": self.account_input.text(),
            "comments": self.comments_input.text()
        }

class ProjectDetailsDialog(QDialog):
    def __init__(self, projects, parent=None):
        super().__init__(parent)
        self.setWindowTitle("All Projects")
        self.projects = projects
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        
        # Add project details to text display
        details_text = ""
        for project, details in self.projects.items():
            details_text += f"Project Name: {project}\n"
            details_text += f"  Account Number: {details.get('account_number', 'N/A')}\n"
            details_text += f"  Comments: {details.get('comments', 'N/A')}\n\n"
        
        self.text_display.setText(details_text)
        
        layout.addWidget(self.text_display)
        self.setLayout(layout)

class HoursDialog(QDialog):
    def __init__(self, projects, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Hours Overview")
        self.projects = projects
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        
        # Calculate hours data
        week_data = defaultdict(lambda: defaultdict(float))
        total_hours_per_week = defaultdict(float)

        for project, details in self.projects.items():
            if "hours" in details:
                for date_str, hours in details["hours"].items():
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    iso_year, iso_week, _ = date_obj.isocalendar()
                    week_num = f"{iso_year}-W{iso_week:02d}"
                    week_data[week_num][project] += hours
                    total_hours_per_week[week_num] += hours

        # Create display text
        hours_display = "Hours Worked per Project:\n\n"
        for week, projects_in_week in week_data.items():
            hours_display += f"Week: {week}\n"
            week_total = total_hours_per_week[week]
            for project, hours in projects_in_week.items():
                percentage = (hours / week_total) * 100 if week_total > 0 else 0
                hours_display += f"  - {project}: {hours} hours ({percentage:.2f}%)\n"
            hours_display += f"  Total hours in week: {week_total}\n\n"

        if not week_data:
            hours_display = "No hours have been recorded yet."

        self.text_display.setText(hours_display)
        layout.addWidget(self.text_display)
        self.setLayout(layout)

class TimeTrackerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Project Time Tracker")
        self.projects = self.load_projects()
        self.setup_ui()
        self.setStyleSheet(self.load_stylesheet())  # Apply custom styles

    def setup_ui(self):
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Project selection section
        project_group = QGroupBox("Add Hours")
        project_layout = QVBoxLayout(project_group)
        
        # Project selection combo
        project_label = QLabel("Select Project:")
        self.project_combo = QComboBox()
        self.project_combo.addItems(self.projects.keys())
        
        # Hours slider
        hours_label = QLabel("Enter Hours Worked:")
        self.hours_slider = QSlider(Qt.Horizontal)
        self.hours_slider.setMinimum(1)
        self.hours_slider.setMaximum(10)
        self.hours_value_label = QLabel("Hours: 1")
        self.hours_slider.valueChanged.connect(
            lambda v: self.hours_value_label.setText(f"Hours: {v}")
        )
        
        # Date selection with calendar
        date_layout = QHBoxLayout()
        date_label = QLabel("Selected Date:")
        self.date_display = QLabel(datetime.now().strftime('%Y-%m-%d'))
        self.select_date_btn = QPushButton("Select Date")
        self.select_date_btn.clicked.connect(self.show_calendar)
        
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_display)
        date_layout.addWidget(self.select_date_btn)
        
        # Weekday buttons
        weekday_layout = QHBoxLayout()
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.weekday_buttons = []
        for day in days:
            btn = QPushButton(day)
            btn.clicked.connect(self.select_weekday)
            self.weekday_buttons.append(btn)
            weekday_layout.addWidget(btn)
        
        # Add Hours button
        add_hours_btn = QPushButton("Add Hours")
        add_hours_btn.clicked.connect(self.add_hours)
        
        # Add widgets to project frame
        project_layout.addWidget(project_label)
        project_layout.addWidget(self.project_combo)
        project_layout.addWidget(hours_label)
        project_layout.addWidget(self.hours_slider)
        project_layout.addWidget(self.hours_value_label)
        project_layout.addLayout(date_layout)  # Add the new date layout
        project_layout.addLayout(weekday_layout)  # Add the weekday buttons
        project_layout.addWidget(add_hours_btn)
        
        # Button section for showing hours
        show_hours_group = QGroupBox("Show Hours")
        show_hours_layout = QVBoxLayout(show_hours_group)
        
        show_hours_btn = QPushButton("Show Hours")
        show_hours_btn.clicked.connect(self.show_hours)
        
        show_hours_layout.addWidget(show_hours_btn)
        
        # Button section for project control
        project_control_group = QGroupBox("Project Control")
        project_control_layout = QVBoxLayout(project_control_group)
        
        add_project_btn = QPushButton("Add New Project")
        add_project_btn.clicked.connect(self.add_new_project)
        show_projects_btn = QPushButton("Show Projects")
        show_projects_btn.clicked.connect(self.show_projects)
        
        project_control_layout.addWidget(add_project_btn)
        project_control_layout.addWidget(show_projects_btn)
        
        # Week clear section
        week_group = QGroupBox("Clear Week")
        week_layout = QVBoxLayout(week_group)
        
        week_label = QLabel("Select Week to Clear:")
        self.week_combo = QComboBox()
        self.update_week_combo()
        clear_week_btn = QPushButton("Clear Week")
        clear_week_btn.clicked.connect(self.clear_week)
        
        week_layout.addWidget(week_label)
        week_layout.addWidget(self.week_combo)
        week_layout.addWidget(clear_week_btn)
        
        # Chart frame
        self.chart_frame = QFrame()
        self.chart_layout = QVBoxLayout(self.chart_frame)
        self.update_chart()
        
        # Add all sections to main layout
        main_layout.addWidget(project_group)
        main_layout.addWidget(show_hours_group)
        main_layout.addWidget(project_control_group)
        main_layout.addWidget(week_group)
        main_layout.addWidget(self.chart_frame)
        
        # Week hours section
        week_hours_group = QGroupBox("Weekly Hours Overview")
        week_hours_layout = QVBoxLayout(week_hours_group)
        
        self.week_hours_combo = QComboBox()
        self.week_hours_combo.currentIndexChanged.connect(self.update_week_hours_display)
        
        self.week_hours_display = QTextEdit()
        self.week_hours_display.setReadOnly(True)
        
        week_hours_layout.addWidget(self.week_hours_combo)
        week_hours_layout.addWidget(self.week_hours_display)
        
        main_layout.addWidget(week_hours_group)
        self.update_week_hours_combo()

    def load_projects(self):
        try:
            with open("projects.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_projects(self):
        with open("projects.json", "w") as file:
            json.dump(self.projects, file, indent=4)

    def add_hours(self):
        project_name = self.project_combo.currentText()
        date = self.date_display.text()  # Using the new date display
        hours = self.hours_slider.value()

        if hours == 0:
            QMessageBox.critical(self, "Error", "Please enter hours worked greater than 0.")
            return

        if project_name not in self.projects:
            self.projects[project_name] = {"hours": {}}

        if "hours" not in self.projects[project_name]:
            self.projects[project_name]["hours"] = {}

        if date not in self.projects[project_name]["hours"]:
            self.projects[project_name]["hours"][date] = 0

        self.projects[project_name]["hours"][date] += hours
        self.save_projects()
        self.update_chart()
        self.update_week_hours_combo()
        QMessageBox.information(self, "Success", 
                              f"Added {hours} hours for {project_name} on {date}.")

    def add_new_project(self):
        dialog = NewProjectDialog(self)
        if dialog.exec_():
            project_data = dialog.get_project_data()
            project_name = project_data["name"]
            
            if project_name and project_name not in self.projects:
                self.projects[project_name] = {
                    "account_number": project_data["account_number"],
                    "comments": project_data["comments"],
                    "hours": {}
                }
                self.save_projects()
                self.project_combo.addItem(project_name)
                QMessageBox.information(self, "Success", 
                                      f"New project '{project_name}' added.")
            else:
                QMessageBox.critical(self, "Error", 
                                   "Please enter a valid project name or project already exists.")

    def show_projects(self):
        dialog = ProjectDetailsDialog(self.projects, self)
        dialog.exec_()

    def show_hours(self):
        dialog = HoursDialog(self.projects, self)
        dialog.exec_()

    def show_calendar(self):
        dialog = CalendarDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            selected_date = dialog.get_selected_date()
            self.date_display.setText(selected_date)

    def select_weekday(self):
        sender = self.sender()
        day_name = sender.text()
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        day_index = days.index(day_name)
        
        selected_date = start_of_week + timedelta(days=day_index)
        self.date_display.setText(selected_date.strftime('%Y-%m-%d'))

    def update_chart(self):
        # Clear existing chart
        for i in reversed(range(self.chart_layout.count())): 
            self.chart_layout.itemAt(i).widget().setParent(None)

        # Calculate hours per day
        hours_per_day = defaultdict(float)
        for project, details in self.projects.items():
            if "hours" in details:
                for date_str, hours in details["hours"].items():
                    hours_per_day[date_str] += hours

        if not hours_per_day:
            return

        # Create the plot
        fig, ax = plt.subplots(figsize=(8, 4))
        dates = sorted(hours_per_day.keys())
        hours = [hours_per_day[date] for date in dates]
        
        ax.plot(dates, hours, marker='o', color='b', label='Hours Worked')
        
        # Highlight days over 8 hours
        for i, h in enumerate(hours):
            if h > 8:
                ax.plot(dates[i], h, marker='o', color='r')
        
        ax.set_xlabel("Date")
        ax.set_ylabel("Total Hours")
        ax.set_title("Hours Worked Per Day")  # Corrected method name
        
        canvas = FigureCanvas(fig)
        self.chart_layout.addWidget(canvas)

    def update_week_combo(self):
        weeks = set()
        for project, details in self.projects.items():
            if "hours" in details:
                for date_str in details["hours"].keys():
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    iso_year, iso_week, _ = date_obj.isocalendar()
                    weeks.add(f"{iso_year}-W{iso_week:02d}")
        
        self.week_combo.clear()
        self.week_combo.addItems(sorted(weeks))

    def clear_week(self):
        selected_week = self.week_combo.currentText()
        
        if not selected_week:
            QMessageBox.critical(self, "Error", "Please select a week to clear.")
            return

        year, week = map(int, selected_week.split("-W"))
        week_start = datetime.strptime(f"{year}-W{week - 1}-1", "%Y-W%U-%w")
        week_end = week_start + timedelta(days=6)

        week_start_str = week_start.strftime("%Y-%m-%d")
        week_end_str = week_end.strftime("%Y-%m-%d")

        for project, details in self.projects.items():
            if "hours" in details:
                for date_str in list(details["hours"].keys()):
                    if week_start_str <= date_str <= week_end_str:
                        del self.projects[project]["hours"][date_str]

        self.save_projects()
        self.update_chart()
        self.update_week_combo()
        self.update_week_hours_combo()
        QMessageBox.information(self, "Success", 
                              f"All entries for week {selected_week} have been cleared.")
    
    def update_week_hours_combo(self):
        weeks = set()
        for project, details in self.projects.items():
            if "hours" in details:
                for date_str in details["hours"].keys():
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    iso_year, iso_week, _ = date_obj.isocalendar()
                    weeks.add(f"{iso_year}-W{iso_week:02d}")
        
        self.week_hours_combo.clear()
        self.week_hours_combo.addItems(sorted(weeks))
    
    def update_week_hours_display(self):
        selected_week = self.week_hours_combo.currentText()
        
        if not selected_week:
            self.week_hours_display.setText("")
            return
        
        year, week = map(int, selected_week.split("-W"))
        week_start = datetime.strptime(f"{year}-W{week - 1}-1", "%Y-W%U-%w")
        week_end = week_start + timedelta(days=6)

        week_hours_display = f"Hours for Week {selected_week}:\n\n"
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        for day_index in range(7):
            current_date = week_start + timedelta(days=day_index)
            current_date_str = current_date.strftime("%Y-%m-%d")
            day_name = days[day_index]
            
            day_total_hours = 0
            for project, details in self.projects.items():
                if "hours" in details and current_date_str in details["hours"]:
                    day_total_hours += details["hours"][current_date_str]
                    
            week_hours_display += f"{day_name} ({current_date_str}): {day_total_hours} hours\n"
        
        week_hours_display += "\n"
        
        self.week_hours_display.setText(week_hours_display)
        
    def load_stylesheet(self):
        return """
        QMainWindow {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QGroupBox {
            background-color: #3a3a3a;
            border: 1px solid #555555;
            border-radius: 5px;
            margin-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 3px;
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QLabel {
            font-size: 14px;
            color: #ffffff;
        }
        QComboBox, QSlider, QLineEdit, QPushButton {
            font-size: 14px;
            padding: 5px;
            margin: 5px 0;
            background-color: #3a3a3a;
            border: 1px solid #555555;
            color: #ffffff;
        }
        QSlider::groove:horizontal {
            border: 1px solid #999999;
            height: 8px;
            background: #3a3a3a;
            margin: 2px 0;
        }
        QSlider::handle:horizontal {
            background: #4CAF50;
            border: 1px solid #4CAF50;
            width: 18px;
            height: 18px;
            margin: -4px 0;
            border-radius: 9px;
        }
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px;
            text-align: center;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QPushButton:pressed {
            background-color: #3e8e41;
        }
        QTextEdit {
            font-size: 14px;
            padding: 10px;
            background-color: #3a3a3a;
            color: #ffffff;
        }
        QCalendarWidget {
            font-size: 14px;
            background-color: #3a3a3a;
            color: #ffffff;
            border: 1px solid #555555;
        }
        """
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimeTrackerApp()
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec_())