# Clash of Clans (Ancient Ruins Clan) Website

## Overview
Welcome to the [Clash of Clans (Ancient Ruins Clan) Website](https://coc-ancient-ruins-website.onrender.com/) repository! This project aims to improve the clan experience through a complete platform for member data collection, planning, and engagement. Developed with HTML, CSS, Python, JavaScript, Flask, and PostgreSQL, this site provides a host of features that will assist our clan members in connecting and succeeding.

## Features
- **Member Data Collection:** Complete data on clan members and past members.
- **Clan Score Columns:** Shows performance measurements and scores.
- **Top Clan Contributors Table:** Indicates the most contributing or active members.
- **Search & Sort:** Simple search and ordering of data within tables.
- **Export Options:** HTML tables exportable to PDF, JSON, CSV, and Excel.
- **API Integration:** Programmatically access member data through API.
- **Graphs & Visualizations:** Offers graphical view of clan member and former member information.

## Website Link
Visit the [Clan Website](https://coc-ancient-ruins-website.onrender.com/)

## Updates
- **7/10/23:** Included link to view detailed information for every clan member on another website.
- **14/10/23:** Developed Clan Score Columns and Top Clan Contributors Table.
- **10/11/23:** Included background color for the War column.
- **16/11/23:** Added search feature to all tables.
- **9/1/24:** Added sorting feature for all tables.
- **17/2/24:** Added JavaScript functions to export HTML tables to:
  - PDF
  - JSON
  - CSV
  - Excel
- **19/5/24:** Included API links to access clan members and former members data:
  - [Clan Members API](https://coc-ancient-ruins-website.onrender.com/api/mem)
  - [Former Clan Members API](https://coc-ancient-ruins-website.onrender.com/api/fmem)
- **4/8/24:** Added some different graphs for viewing data:
  - Clan Members Graphs
  - Former Members Graphs
- **5/8/24:** Updated the URL fetching data from the database API to a GitHub raw JSON file because the API was taking too long to load data, making the web app take forever to load. Now using [ClanDataRepo repository](https://github.com/Lightning-President-9/ClanDataRepo), which offers CSV, JSON, XLS, and PDF files for Clan Members, Former Clan Members, and Top Clan Contributors uploaded monthly. The JSON file is used for data accessing for graphs and added port no 4000 in `app.py`.
- **30/9/24:** Added Dropdown to retrieve data for respective given month in graphs.
- **31/10/24:** Added Navigation Bar.
- **3/1/25:** Transferred from Replit to PyCharm Community 2024.3.1.1.
- **20/2/25:** Added 'Clan Member Month' and 'All Month Analysis' graphs, and updated the icons for nav-bar and graph-selection.
- **7/6/25:**  Added Heatmaps in 'All Month Analysis' graphs and AI Prediction visuals for performance trends and future forecasts across key metrics.
- **7/7/25:**  Added 404 and reusable navbar templates, included navbar.html to reduce redundancy, updated image URLs in CSS, adjusted min-height styling, and standardized all @app.route paths with trailing slashes

## License
This project is licensed under the [MIT License](https://github.com/Lightning-President-9/coc-ancient-ruins-website/blob/main/LICENSE). See the LICENSE file for details.

## Acknowledgements
- [Flask](https://flask.palletsprojects.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/)
- [Plotly Express](https://plotly.com/python/plotly-express/)