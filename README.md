# Clash of Clans Clan Website

## Overview

Welcome to the Clash of Clans Clan Website repository! This project is dedicated to enhancing the clan experience by providing a comprehensive hub for member data collection, strategic planning, and interaction. Built with HTML, CSS, Python, JavaScript, Flask, and PostgreSQL, this website offers a variety of features to help our clan members connect and excel.

## Features

- **Member Data Collection:** Detailed information about clan members and former members.
- **Clan Score Columns:** Displays performance metrics and scores.
- **Top Clan Contributors Table:** Highlights the most active or influential members.
- **Search & Sort:** Easily find and organize data across tables.
- **Export Options:** Convert HTML tables to PDF, JSON, CSV, and Excel formats.
- **API Integration:** Access member data programmatically via API.
- **Graphs & Visualizations:** Provides graphical insights into clan member and former member data.

## Website Link

[Visit the Clan Website](https://coc-ancient-ruins-website.onrender.com/)

## Updates

- **7/10/23:** Added link to view detailed information for each clan member on another website.
- **14/10/23:** Created Clan Score Columns and Top Clan Contributors Table.
- **10/11/23:** Added background color for the War column.
- **16/11/23:** Implemented search feature across all tables.
- **9/1/24:** Added sorting functionality for all tables.
- **17/2/24:** Introduced JavaScript functions to export HTML tables to:
  - PDF
  - JSON
  - CSV
  - Excel
- **19/5/24:** Added API links for accessing clan members and former members data:
  - [Clan Members API](https://coc-ancient-ruins-website.onrender.com/api/mem)
  - [Former Clan Members API](https://coc-ancient-ruins-website.onrender.com/api/fmem)
- **4/8/24:** Added various graphs for visualizing data:
  - [Clan Members Graphs](https://coc-ancient-ruins-website.onrender.com/graph/mem)
  - [Former Members Graphs](https://coc-ancient-ruins-website.onrender.com/graph/fmem)

## Getting Started

To run this project locally, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Lightning-President-9/coc-ancient-ruins-website.git
   ```

2. **Navigate to the project directory:**

   ```bash
   cd coc-ancient-ruins-website
   ```

3. **Set up a virtual environment (recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Configure the database:**
   - Update the `config.py` file with your database credentials.

6. **Run the application:**

   ```bash
   python app.py
   ```

   By default, the application will be accessible at `http://127.0.0.1:5000/`.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/Lightning-President-9/coc-ancient-ruins-website/blob/main/LICENSE) file for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/)
