# Project Time Tracker


Project Time Tracker is a desktop application built with Python and PyQt5 that helps users efficiently manage their projects and track time spent on them. It provides a clean and intuitive interface to log hours, visualize project progress, and manage project details.

---

## Features

### 1. Add and Manage Projects
- Create new projects with details like project name, account number, and comments.
- View all projects and their details in a consolidated display.


### 2. Log Hours
- Select a project and log hours for specific days.
- Use a slider to input the number of hours worked (1-10 hours).
- Choose a date using a calendar widget or quick-select a weekday.


### 3. View Hours Overview
- Get an overview of the hours worked per project, categorized by week.
- See the percentage distribution of hours worked on each project.


### 4. Weekly Hours Display
- View the hours worked for a specific week.
- Get a day-by-day breakdown of hours logged.


### 5. Visualize Data
- Dynamic charts showing hours logged per day.
- Days with excessive hours (over 8) are highlighted for easy identification.

### 6. Clear Weekly Data
- Clear all logged hours for a selected week with a single click.


---

## Installation

1. Clone the repository or download the source code:
   ```bash
   git clone https://github.com/CodingWithCobots/ProjectTimetracker.git
   cd ProjectTimetracker
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python timeplannerv5.py
   ```

---

## How to Use

### 1. Adding a New Project
- Click on the "Add New Project" button in the **Project Control** section.
- Enter the project name, account number, and comments.
- Click "Add Project" to save.

### 2. Logging Hours
- Select a project from the dropdown menu in the **Add Hours** section.
- Use the slider to set the hours worked.
- Choose a date using the calendar button or quick-select a weekday.
- Click "Add Hours" to save the entry.

### 3. Viewing Hours
- Click "Show Hours" to view an overview of hours worked for all projects.
- Select a week in the **Weekly Hours Overview** section to see detailed hours per day.

### 4. Clearing Weekly Data
- Choose a week from the dropdown in the **Clear Week** section.
- Click "Clear Week" to delete all logged hours for that week.

---

## File Management
The application saves project data in a `projects.json` file located in the same directory as the script.

---

## Technical Details

- **UI Framework**: PyQt5
- **Charting Library**: Matplotlib
- **Data Storage**: JSON file
- **Programming Language**: Python
- **Styling**: Custom CSS-like styles for PyQt5 widgets

---

## Future Improvements
- Add the ability to export data to Excel or CSV.
- Implement user authentication for multi-user support.
- Add support for recurring tasks or projects.

---

## Contributing
Contributions are welcome! Feel free to submit a pull request or open an issue to suggest features or report bugs.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments
Special thanks to the open-source community for providing tools like PyQt5 and Matplotlib that made this project possible.
