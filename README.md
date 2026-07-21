# Clash of Clans (Ancient Ruins Clan) Website

## Overview
Welcome to the [Clash of Clans (Ancient Ruins Clan) Website](https://coc-ancient-ruins-website.onrender.com/) repository! This project aims to improve the clan experience through a complete platform for member data collection, planning, and engagement. Developed with HTML, CSS, Python, JavaScript, Flask, and PostgreSQL, this site provides a host of features that will assist our clan members in connecting and succeeding.

## Features

- **Member & Former Member Data**: Complete records of clan members with historical tracking
- **Performance Metrics**: Clan score columns and contribution-based rankings
- **Top Contributors**: Table highlighting most active and valuable players
- **Search & Sort**: Easy filtering and ordering across all tables
- **Export Options**: Download data as PDF, JSON, CSV, or Excel
- **API Access**: Endpoints for members and former members with Swagger docs and rate limiting
- **Graphs & Analytics**: Visual dashboards for trends, monthly analysis, and comparisons
- **Advanced Insights**: Heatmaps, AI-based predictions, and KMeans clustering
- **Player Reports**: Detailed individual performance reports across all game areas
- **Month-wise Filtering**: Dynamic selection for time-based analysis
- **UI Improvements**: Centralized navbar, reusable templates, and improved structure
- **System Enhancements**: Faster data loading via GitHub JSON, Redis support, and cleaner backend design
- **KARBS Chatbot**: Rule-based assistant for clan performance analysis


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
- **7/7/25:**  Added 404 and reusable navbar templates, included navbar.html to reduce redundancy, updated image URLs in CSS, adjusted min-height styling, and standardized all @app.route paths with trailing slashes.
- **7/8/25:**  Centralized head elements in `head.html`, added `graph.css` & `graph.js` for graph styles and logic, cleaned up templates, and removed all Replit-specific files.
- **1/9/25** Added player_report.html and player_report.py to provide a detailed look at a player’s performance across different Clash of Clans activities like War Attacks, Clan Capital, Clan Games, and more. The report includes helpful visuals and tables to track progress and highlight the player’s biggest contributions.
- **13/10/25:** Streamlined month selection for members, former members, and monthly analysis graphs, reducing redundancy. Handled missing data cases and added a Google Form for feedback.
- **1/1/26:** Added Documentation in all the .py files.
- **10/1/26:** Added KARBS a light weighted rule based chat/conversational bot for deep statistical analysis of Ancient Ruins Clan.
- **22/1/26:** Added KMeans-based member cluster analysis with discrete scatter plots to visualize performance groupings across key metrics.
- **21/4/26:** Integrated Clash of Clans data from the API, implemented Swagger for comprehensive API documentation, added rate limiting to enhance API security and performance, and improved overall code structure and formatting for better maintainability.
- **5/5/26:** Added UptimeRobot services for uptime monitoring and to keep the application running continuously.
- **19/5/26:** Added Redis URL support for rate limiting.
- **14/6/26:** Removed UptimeRobot services.
- **23/6/26:** Revised and improved the formula used to compute clan scores for more accurate and balanced player performance evaluation.
- **15/7/26:** Updated AI prediction graphs to start from the player's join month, fixed the `playerHouse` error, added functionality to capture whole screen image and added an interactive Player Dashboard with player statistics, rankings, graphs, heatmaps, clan comparison, and monthly history.

## Tree Structure
```
coc-ancient-ruins-website/
├── .gitignore
├── app.py
├── chatbot/
│   ├── __init__.py
│   ├── almost_hint.py
│   ├── chat_controller.py
│   ├── domain_router.py
│   ├── input_classifier.py
│   ├── month_normalizer.py
│   ├── operation_resolver.py
│   ├── raw_fetcher.py
│   └── response_builder.py
├── coc_data_persist.py
├── coc-data/
│   ├── capital_raid_seasons.json
│   ├── clan_details.json
│   ├── clan_members.json
│   ├── clan_players/
│   │   ├── arggggggah.json
│   │   ├── Chief.json
│   │   ├── COPY_KAKASHI.json
│   │   ├── Dewan.json
│   │   ├── Eleiken.json
│   │   ├── emnil007.json
│   │   ├── flameboy5050.json
│   │   ├── gautam.json
│   │   ├── Grandpa1.json
│   │   ├── JIREN.json
│   │   ├── Joyotri.json
│   │   ├── KAI_HIWATARI.json
│   │   ├── kindstonge17.json
│   │   ├── kking.json
│   │   ├── mare.json
│   │   ├── Noob3.json
│   │   ├── Prachit123.json
│   │   ├── pramod.json
│   │   ├── raful.json
│   │   ├── Rider_22.json
│   │   ├── sonu.json
│   │   ├── tejas.json
│   │   ├── TREX.json
│   │   ├── Yash.json
│   │   └── You.json
│   ├── clans_search.json
│   └── warlog.json
├── constants.py
├── dashboard/
│   ├── __init__.py
│   ├── player_dashboard.py
│   ├── player_data.py
│   ├── player_graphs.py
│   ├── player_rankings.py
│   ├── player_statistics.py
│   └── player_utils.py
├── data_file.pickle
├── data_persist.py
├── database.py
├── graphs/
│   ├── __init__.py
│   ├── ai_prediction_graph.py
│   ├── all_month_graph.py
│   ├── clan_member_graph.py
│   ├── former_member_graph.py
│   ├── member_cluster_graph.py
│   ├── monthly_analysis_graph.py
│   └── player_report.py
├── LICENSE
├── limiter_config.py
├── README.md
├── requirements.txt
├── routes/
│   ├── __init__.py
│   ├── ai_routes.py
│   ├── api_routes.py
│   ├── chatbot_routes.py
│   ├── coc_routes.py
│   ├── dashboard_routes.py
│   ├── error_handlers.py
│   ├── github_api_routes.py
│   ├── graph_routes.py
│   ├── report_routes.py
│   └── ui_routes.py
├── services/
│   ├── __init__.py
│   ├── ai_service.py
│   ├── dashboard_service.py
│   ├── github_service.py
│   ├── graph_service.py
│   └── report_service.py
├── static/
│   ├── bg_img.jpg
│   ├── clan-badge_18.png
│   ├── graph-icons/
│   │   ├── 3dscatterplot.png
│   │   ├── areagraph.png
│   │   ├── bar.png
│   │   ├── boxplot.png
│   │   ├── densityplot.png
│   │   ├── funnelchart.png
│   │   ├── heatmap.png
│   │   ├── histogram.png
│   │   ├── linechart.png
│   │   ├── piechart.png
│   │   ├── polarchart.png
│   │   ├── scatterplot.png
│   │   ├── sunburstchart.png
│   │   ├── treemap.png
│   │   ├── violinplot.png
│   │   └── waterfallchart.png
│   ├── home-page-icons/
│   │   ├── csv_icon_img_final.png
│   │   ├── export_img_final.png
│   │   ├── json_icon_img_final.png
│   │   ├── pdf_icon_img_final.png
│   │   ├── search_img_final.png
│   │   └── xls_icon_img_final.png
│   └── nav-bar-icons/
│       ├── ai_img.png
│       ├── api_img.png
│       ├── coc-data_img.png
│       ├── discord_img.png
│       ├── github_img.png
│       ├── graph_img.png
│       ├── home_img.png
│       ├── invite_img.png
│       ├── player-analytics_img.png
│       └── screenshot_img.png
└── templates/
    ├── chatbot-pages/
    │   ├── chat.css
    │   ├── chat.html
    │   └── chat.js
    ├── coc-data-index.html
    ├── coc-data-pages/
    │   ├── capital-raids-all-attacks.html
    │   ├── capital-raids-all-defences.html
    │   ├── capital-raids-latest-attacks.html
    │   ├── capital-raids-latest-defences.html
    │   ├── capital-raids.html
    │   ├── clan-details.html
    │   ├── clan-player-profile.html
    │   ├── clan-players.html
    │   ├── clan-search.html
    │   ├── table-utils.js
    │   └── war-log.html
    ├── dashboard/
    │   ├── components/
    │   │   ├── chart.html
    │   │   ├── monthly_table.html
    │   │   ├── player_header.html
    │   │   └── summary_cards.html
    │   ├── dashboard.html
    │   ├── player_dashboard.css
    │   ├── player_dashboard.html
    │   ├── player_dashboard.js
    │   └── player_history_table.js
    ├── error-pages/
    │   ├── 404.html
    │   ├── 405.html
    │   ├── 429.html
    │   └── 500.html
    ├── graph-pages/
    │   ├── all-month-graph.html
    │   ├── fmem-graph.html
    │   ├── graph.css
    │   ├── graph.html
    │   ├── graph.js
    │   ├── mem-graph.html
    │   ├── mem-month-analysis.html
    │   ├── mem-month-graph.html
    │   └── player-report.html
    ├── head.html
    ├── index.html
    ├── navbar.html
    ├── screenshot.js
    ├── script.js
    └── style.css
```

## License
This project is licensed under the [MIT License](https://github.com/Lightning-President-9/coc-ancient-ruins-website/blob/main/LICENSE). See the LICENSE file for details.

## Acknowledgements
- [Flask](https://flask.palletsprojects.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/)
- [Neon](https://neon.com/)
- [Plotly Express](https://plotly.com/python/plotly-express/)
- [Flasgger](https://github.com/flasgger/flasgger)
- [Clash of Clans API](https://developer.clashofclans.com)
- [Upstash](https://upstash.com/)
- [UptimeRobot](https://uptimerobot.com/)