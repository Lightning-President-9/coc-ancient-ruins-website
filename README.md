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
- **5/8/24:** Changed the data fetching URL from the database API to a GitHub raw JSON file as the API was taking too long to fetch data, causing the web app to load infinitely. Now using [ClanDataRepo](https://github.com/Lightning-President-9/ClanDataRepo) repository, which provides CSV, JSON, XLS, and PDF files for Clan Members, Former Clan Members and Top Clan Contributors uploaded monthly. The JSON file is used for accessing data for graphs and Added port no 4000 in app.py .
- **30/9/24:** Added Dropdown for fetching data for respective given month in graphs.
- **31/10/24:** Added Navigation Bar.
- **3/1/25:** Moved from Replit to Pycharm Community 2024.3.1.1.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/Lightning-President-9/coc-ancient-ruins-website/blob/main/LICENSE) file for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/)