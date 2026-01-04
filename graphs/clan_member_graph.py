# graphs/clan_member_graph.py

"""
Generates detailed visual analytics for current clan members for a
selected month in the Clash of Clans – Ancient Ruins Clan Website.

This module:
- Loads monthly clan member data from a GitHub-hosted JSON source
- Preprocesses and categorizes member performance metrics
- Produces a wide variety of Plotly visualizations, including:
  bar, pie, line, scatter, histogram, box, violin, heatmap, treemap,
  sunburst, density, 3D scatter, area, polar, funnel, and waterfall charts

It serves as the primary visualization engine for member-level analysis.
"""

# Importing Libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import warnings
from constants import LATEST_MONTH

warnings.simplefilter(action='ignore', category=FutureWarning)

class ClanMemberGraph:
    """
    ClanMemberGraph

    Handles data loading, preprocessing, and visualization generation
    for current clan members.

    The class supports:
    - Dynamic month-based data loading
    - Separation of war participation status (IN / OUT)
    - Generation of multiple chart types from the same dataset
    - Graceful fallback to latest available data when requested data is missing
    """

    def __init__(self):
        """
        Initialize the ClanMemberGraph instance.

        Sets default placeholders for:
        - Data source URL
        - Loaded DataFrame
        - Informational message for missing or fallback data
        """

        self.data_url = ''
        self.df = None
        self.message = ""

    def update_and_load_data(self, month_year):
        """
        Load and preprocess clan member data for a given month.

        This method:
        - Dynamically builds the data source URL
        - Fetches JSON data from GitHub
        - Falls back to the latest available month if data is missing
        - Converts performance fields to numeric types
        - Separates members by war participation status
        - Extracts numerical columns for analytics

        Args:
            month_year (str): Month identifier (e.g., 'DEC_2025')
        """

        # Update the data URL dynamically based on month and year
        self.data_url = f'https://raw.githubusercontent.com/Lightning-President-9/ClanDataRepo/main/Clan%20Members/JSON/{month_year}.json'

        # Fetch the updated data
        self.response = requests.get(self.data_url)
        try:
            self.json_data = self.response.json()
        except requests.exceptions.RequestException:
            self.message = f"No data available for {month_year}. Showing {LATEST_MONTH} (Latest)"
            self.update_and_load_data(LATEST_MONTH)

        # Load JSON data into a DataFrame
        self.df = pd.DataFrame(self.json_data)

        # Convert string columns to numeric
        for column in ['warattack', 'clancapital', 'clangames', 'clangamesmaxed', 'clanscore']:
            self.df[column] = pd.to_numeric(self.df[column], errors='coerce')

        # Filter data
        self.df_in = self.df[self.df['war'] == 'IN']
        self.df_out = self.df[self.df['war'] == 'OUT']
        self.numerical_df = self.df.select_dtypes(include=['number'])

    def create_bar_graphs(self):
        """
        Generate bar chart visualizations for clan member performance.

        Includes:
        - Grouped bar charts for IN vs OUT war participation
        - Stacked bar charts for aggregated numerical metrics
        - Distribution counts for war and player status

        Returns:
            list[plotly.graph_objects.Figure]: Bar chart figures
        """

        # 1. Vertical Bar Chart of War Attack
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(x=self.df_in['name'], y=self.df_in['warattack'], name='War IN'))
        fig1.add_trace(go.Bar(x=self.df_out['name'], y=self.df_out['warattack'], name='War OUT'))
        fig1.update_layout(barmode='group', title='Vertical Bar Chart of Clan War Attack', xaxis_title='Name', yaxis_title='War Attack')

        # 2. Vertical Bar Chart of Clan Capital
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=self.df_in['name'], y=self.df_in['clancapital'], name='War IN'))
        fig2.add_trace(go.Bar(x=self.df_out['name'], y=self.df_out['clancapital'], name='War OUT'))
        fig2.update_layout(barmode='group', title='Vertical Bar Chart of Clan Capital', xaxis_title='Name', yaxis_title='Clan Capital')

        # 3. Vertical Bar Chart of Clan Games
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=self.df_in['name'], y=self.df_in['clangames'], name='War IN'))
        fig3.add_trace(go.Bar(x=self.df_out['name'], y=self.df_out['clangames'], name='War OUT'))
        fig3.update_layout(barmode='group', title='Vertical Bar Chart of Clan Games', xaxis_title='Name', yaxis_title='Clan Games')

        # 4. Vertical Bar Chart of Clan Games Maxed
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(x=self.df_in['name'], y=self.df_in['clangamesmaxed'], name='War IN'))
        fig4.add_trace(go.Bar(x=self.df_out['name'], y=self.df_out['clangamesmaxed'], name='War OUT'))
        fig4.update_layout(barmode='group', title='Vertical Bar Chart of Clan Games Maxed', xaxis_title='Name', yaxis_title='Clan Games Maxed')

        # 5. Vertical Bar Chart of Clan Score
        fig5 = go.Figure()
        fig5.add_trace(go.Bar(x=self.df_in['name'], y=self.df_in['clanscore'], name='War IN'))
        fig5.add_trace(go.Bar(x=self.df_out['name'], y=self.df_out['clanscore'], name='War OUT'))
        fig5.update_layout(barmode='group', title='Vertical Bar Chart of Clan Score', xaxis_title='Name', yaxis_title='Clan Score')

        # 6. Stacked Bar Chart of Numerical Values
        fig6 = go.Figure()
        for column in self.numerical_df.columns:
            if column not in ['srno']:  # Exclude 'srno'
                fig6.add_trace(go.Bar(name=column, x=self.df['name'], y=self.df[column]))
        fig6.update_layout(barmode='stack', title='Stacked Bar Chart of Numerical Values', xaxis_title='Names', yaxis_title='Values')

        # 7. Count of War Status and Status Count
        fig7 = go.Figure()
        war_counts = self.df['war'].value_counts()
        fig7.add_trace(go.Bar(name='War Status', x=war_counts.index, y=war_counts.values))
        status_counts = self.df['status'].value_counts()
        fig7.add_trace(go.Bar(name='Status Count', x=status_counts.index, y=status_counts.values))
        fig7.update_layout(barmode='stack', title='Count of War Status and Status Count', xaxis_title='Category', yaxis_title='Count')

        return [fig1, fig2, fig3, fig4, fig5, fig6, fig7]

    def create_pie_charts(self):
        """
        Generate pie chart visualizations for categorical distributions.

        Covers:
        - Player status and war participation
        - Binned distributions for clan capital, clan games,
          clan games maxed, clan score, and war attacks

        Returns:
            list[plotly.graph_objects.Figure]: Pie chart figures
        """

        # 1. Player Status Distribution
        fig1 = px.pie(self.df, names='status', title='Player Status Distribution')

        # 2. War Participation Status
        war_status = self.df['war'].value_counts()
        fig2 = go.Figure(data=[go.Pie(labels=war_status.index, values=war_status.values)])
        fig2.update_layout(title_text='War Participation Status')

        # 3. Clan Capital Contribution
        self.df['clancapital_range'] = pd.cut(
            self.df['clancapital'],
            bins=[-1, 50, 100, 200, 300, float('inf')],
            labels=['0-50', '51-100', '101-200', '201-300', '300+']
        )
        fig3 = px.pie(self.df, names='clancapital_range', title='Clan Capital Contribution')

        # 4. Clan Games Participation
        self.df['clangames_range'] = pd.cut(
            self.df['clangames'],
            bins=[-1, 5, 10, 15, 20, float('inf')],
            labels=['0-5', '6-10', '11-15', '16-20', '20+']
        )
        fig4 = px.pie(self.df, names='clangames_range', title='Clan Games Participation')

        # 5. Maxed Clan Games
        maxed_games = self.df['clangamesmaxed'].value_counts()
        fig5 = go.Figure(data=[go.Pie(labels=maxed_games.index, values=maxed_games.values)])
        fig5.update_layout(title_text='Maxed Clan Games')

        # 6. Clan Score Distribution
        self.df['clanscore_range'] = pd.cut(
            self.df['clanscore'],
            bins=[-1, 100, 300, 500, 700, float('inf')],
            labels=['0-100', '101-300', '301-500', '501-700', '700+']
        )
        fig6 = px.pie(self.df, names='clanscore_range', title='Clan Score Distribution')

        # 7. War Attacks Distribution
        self.df['warattack_range'] = pd.cut(
            self.df['warattack'],
            bins=[-1, 50, 100, 200, 300, float('inf')],
            labels=['0-50', '51-100', '101-200', '201-300', '300+']
        )
        fig7 = px.pie(self.df, names='warattack_range', title='War Attacks Distribution')

        return [fig1, fig2, fig3, fig4, fig5, fig6, fig7]

    def create_line_charts(self):
        """
        Generate line chart visualizations for numerical metrics.

        Includes:
        - Individual metric trends by player
        - Combined multi-metric line chart

        Returns:
            list[plotly.graph_objects.Figure]: Line chart figures
        """

        line_charts = []
        numerical_columns = self.numerical_df.columns.drop('srno', errors='ignore')

        # 1. Line Chart for Each Numerical Column Over Names
        for column in numerical_columns:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=self.df['name'], y=self.df[column], mode='lines+markers', name=column))
            fig.update_layout(title=f'Line Chart of {column} by Name', xaxis_title='Name', yaxis_title=column)
            line_charts.append(fig)

        # 2. Line Chart with Multiple Metrics for Each Name
        fig_combined = go.Figure()
        for column in numerical_columns:
            fig_combined.add_trace(go.Scatter(x=self.df['name'], y=self.df[column], mode='lines+markers', name=column))
        fig_combined.update_layout(title='Line Chart of Multiple Metrics by Name', xaxis_title='Name', yaxis_title='Values')
        line_charts.append(fig_combined)

        return line_charts

    def create_scatter_plots(self):
        """
        Generate scatter plot visualizations for metric comparisons.

        Includes:
        - Pairwise numerical comparisons
        - Color encoding by war participation
        - Size encoding by clan score
        - Combined color and size encodings

        Returns:
            list[plotly.graph_objects.Figure]: Scatter plot figures
        """

        scatter_plots = []
        numerical_columns = self.numerical_df.columns.drop('srno', errors='ignore')

        # 1. Pairwise Scatter Plots with Hover Data
        for i, col1 in enumerate(numerical_columns):
            for col2 in numerical_columns[i+1:]:
                fig = px.scatter(
                    self.df, x=col1, y=col2, hover_name='name',
                    title=f'Scatter Plot of {col1} vs {col2}',
                    labels={col1: col1.capitalize(), col2: col2.capitalize()}
                )
                scatter_plots.append(fig)

        # 2. Scatter Plot with Color by 'war' and Hover Data
        for col1 in numerical_columns:
            for col2 in numerical_columns:
                if col1 != col2:
                    fig = px.scatter(
                        self.df, x=col1, y=col2, color='war', hover_name='name',
                        title=f'Scatter Plot of {col1} vs {col2} by War Status',
                        labels={col1: col1.capitalize(), col2: col2.capitalize(), 'war': 'War Status'},
                        color_continuous_scale=px.colors.qualitative.Safe
                    )
                    scatter_plots.append(fig)

        # 3. Scatter Plot with Size by 'clanscore' and Hover Data
        for col1 in numerical_columns:
            for col2 in numerical_columns:
                if col1 != col2:
                    fig = px.scatter(
                        self.df, x=col1, y=col2, size='clanscore', hover_name='name',
                        title=f'Scatter Plot of {col1} vs {col2} (Size by Clan Score)',
                        labels={col1: col1.capitalize(), col2: col2.capitalize(), 'clanscore': 'Clan Score'},
                        color_continuous_scale=px.colors.sequential.Plasma
                    )
                    scatter_plots.append(fig)

        # 4. Combined Scatter Plot with Color and Size Distinctions
        for col1 in numerical_columns:
            for col2 in numerical_columns:
                if col1 != col2:
                    fig = px.scatter(
                        self.df, x=col1, y=col2, color='war', size='clanscore', hover_name='name',
                        title=f'Scatter Plot of {col1} vs {col2} by War Status and Clan Score',
                        labels={col1: col1.capitalize(), col2: col2.capitalize(), 'war': 'War Status', 'clanscore': 'Clan Score'},
                        color_continuous_scale=px.colors.qualitative.Safe,
                        size_max=15
                    )
                    scatter_plots.append(fig)

        return scatter_plots

    def create_histograms(self):
        """
        Generate histogram visualizations for numerical metrics.

        Includes:
        - Plain distributions
        - Distributions segmented by war status
        - Distributions segmented by player status

        Returns:
            list[plotly.graph_objects.Figure]: Histogram figures
        """

        histograms = []
        numerical_columns = self.numerical_df.columns.drop(['srno'], errors='ignore')

        # 1. Histogram for each numerical column
        for col in numerical_columns:
            fig = px.histogram(self.df, x=col, hover_data=['name'],
                               title=f'Histogram of {col}',
                               labels={col: col, 'count': 'Player Count'})
            histograms.append(fig)

        # 2. Histogram with color differentiation by 'war' status
        for col in numerical_columns:
            fig = px.histogram(self.df, x=col, color='war', hover_data=['name'],
                               title=f'Histogram of {col} by War Status',
                               labels={col: col, 'war': 'War Status', 'count': 'Player Count'})
            histograms.append(fig)

        # 3. Histogram with color differentiation by 'status'
        for col in numerical_columns:
            fig = px.histogram(self.df, x=col, color='status', hover_data=['name'],
                               title=f'Histogram of {col} by Status',
                               labels={col: col, 'status': 'Player Status', 'count': 'Player Count'})
            histograms.append(fig)

        return histograms

    def create_box_plots(self):
        """
        Generate box plot visualizations for statistical distribution analysis.

        Includes:
        - Overall distributions
        - Distributions segmented by war participation
        - Distributions segmented by player status

        Returns:
            list[plotly.graph_objects.Figure]: Box plot figures
        """

        box_plots = []
        numerical_columns = self.numerical_df.columns.drop(['srno'], errors='ignore')

        # 1. Box Plot for each numerical column
        for col in numerical_columns:
            fig = px.box(self.df, y=col, points="all", hover_data=['name'],
                         title=f'Box Plot of {col}',
                         labels={col: col, 'name': 'Player Name'})
            box_plots.append(fig)

        # 2. Box Plot with color differentiation by 'war' status
        for col in numerical_columns:
            fig = px.box(self.df, y=col, color='war', points="all", hover_data=['name'],
                         title=f'Box Plot of {col} by War Status',
                         labels={col: col, 'war': 'War Status', 'name': 'Player Name'})
            box_plots.append(fig)

        # 3. Box Plot with color differentiation by 'status'
        for col in numerical_columns:
            fig = px.box(self.df, y=col, color='status', points="all", hover_data=['name'],
                         title=f'Box Plot of {col} by Status',
                         labels={col: col, 'status': 'Player Status', 'name': 'Player Name'})
            box_plots.append(fig)

        return box_plots

    def create_violin_plots(self):
        """
        Generate violin plot visualizations for density and distribution insights.

        Includes:
        - Overall metric distributions
        - Distributions segmented by war participation
        - Distributions segmented by player status

        Returns:
            list[plotly.graph_objects.Figure]: Violin plot figures
        """

        violin_plots = []
        numerical_columns = self.numerical_df.columns.drop(['srno'], errors='ignore')

        # 1. Violin Plot for each numerical column
        for col in numerical_columns:
            fig = px.violin(self.df, y=col, box=True, points="all", hover_data=['name'],
                            title=f'Violin Plot of {col}',
                            labels={col: col, 'name': 'Player Name'})
            violin_plots.append(fig)

        # 2. Violin Plot with color differentiation by 'war' status
        for col in numerical_columns:
            fig = px.violin(self.df, y=col, color='war', box=True, points="all", hover_data=['name'],
                            title=f'Violin Plot of {col} by War Status',
                            labels={col: col, 'war': 'War Status', 'name': 'Player Name'})
            violin_plots.append(fig)

        # 3. Violin Plot with color differentiation by 'status'
        for col in numerical_columns:
            fig = px.violin(self.df, y=col, color='status', box=True, points="all", hover_data=['name'],
                            title=f'Violin Plot of {col} by Status',
                            labels={col: col, 'status': 'Player Status', 'name': 'Player Name'})
            violin_plots.append(fig)

        return violin_plots

    def create_heatmaps(self):
        """
        Generate heatmap visualizations for relationship intensity analysis.

        Includes:
        - Metric-to-metric density heatmaps
        - Categorical heatmap of war status vs player status

        Returns:
            list[plotly.graph_objects.Figure]: Heatmap figures
        """

        heatmaps = []

        # 1. Heatmap of warattack vs clancapital
        heatmap1 = px.density_heatmap(self.df, x='warattack', y='clancapital', nbinsx=20, nbinsy=20,
                                      title='Heatmap of War Attack vs Clan Capital',
                                      labels={'warattack': 'War Attack', 'clancapital': 'Clan Capital'})
        heatmaps.append(heatmap1)

        # 2. Heatmap of clangames vs clangamesmaxed
        heatmap2 = px.density_heatmap(self.df, x='clangames', y='clangamesmaxed', nbinsx=20, nbinsy=20,
                                      title='Heatmap of Clan Games vs Clan Games Maxed',
                                      labels={'clangames': 'Clan Games', 'clangamesmaxed': 'Clan Games Maxed'})
        heatmaps.append(heatmap2)

        # 3. Heatmap of warattack vs clanscore
        heatmap3 = px.density_heatmap(self.df, x='warattack', y='clanscore', nbinsx=20, nbinsy=20,
                                      title='Heatmap of War Attack vs Clan Score',
                                      labels={'warattack': 'War Attack', 'clanscore': 'Clan Score'})
        heatmaps.append(heatmap3)

        # 4. Heatmap of clancapital vs clanscore
        heatmap4 = px.density_heatmap(self.df, x='clancapital', y='clanscore', nbinsx=20, nbinsy=20,
                                      title='Heatmap of Clan Capital vs Clan Score',
                                      labels={'clancapital': 'Clan Capital', 'clanscore': 'Clan Score'})
        heatmaps.append(heatmap4)

        # 5. Heatmap with categorical variables, using war and status as categories
        # Categorical heatmap example (using counts)
        war_status_counts = pd.crosstab(self.df['war'], self.df['status'])
        heatmap5 = go.Figure(data=go.Heatmap(
            z=war_status_counts.values,
            x=war_status_counts.columns,
            y=war_status_counts.index,
            colorscale='Viridis'))
        heatmap5.update_layout(
            title='Heatmap of War Status vs Player Status',
            xaxis_title='Player Status',
            yaxis_title='War Status')
        heatmaps.append(heatmap5)

        return heatmaps

    def create_treemaps(self):
        """
        Generate treemap visualizations for hierarchical contribution analysis.

        Maps performance metrics by:
        - Player status
        - War participation status

        Returns:
            list[plotly.graph_objects.Figure]: Treemap figures
        """

        treemaps = []

        # Ensure there are no NaN or zero values in the values column
        def filter_non_zero(df, column):
            return df[df[column].fillna(0) != 0]

        # 1. Treemap based on 'status' and 'warattack'
        df_filtered = filter_non_zero(self.df, 'warattack')
        if not df_filtered.empty:
            treemap1 = px.treemap(df_filtered, path=['status', 'name'], values='warattack',
                                  title='Treemap of War Attack by Player Status',
                                  labels={'warattack': 'War Attack', 'name': 'Player Name'},
                                  color='warattack', hover_data=['warattack'],
                                  color_continuous_scale='Viridis')
            treemaps.append(treemap1)

        # 2. Treemap based on 'war' and 'clancapital'
        df_filtered = filter_non_zero(self.df, 'clancapital')
        if not df_filtered.empty:
            treemap2 = px.treemap(df_filtered, path=['war', 'name'], values='clancapital',
                                  title='Treemap of Clan Capital by War Status',
                                  labels={'clancapital': 'Clan Capital', 'name': 'Player Name'},
                                  color='clancapital', hover_data=['clancapital'],
                                  color_continuous_scale='Viridis')
            treemaps.append(treemap2)

        # 3. Treemap based on 'status' and 'clanscore'
        df_filtered = filter_non_zero(self.df, 'clanscore')
        if not df_filtered.empty:
            treemap3 = px.treemap(df_filtered, path=['status', 'name'], values='clanscore',
                                  title='Treemap of Clan Score by Player Status',
                                  labels={'clanscore': 'Clan Score', 'name': 'Player Name'},
                                  color='clanscore', hover_data=['clanscore'],
                                  color_continuous_scale='Viridis')
            treemaps.append(treemap3)

        # 4. Treemap based on 'war' and 'clangames'
        df_filtered = filter_non_zero(self.df, 'clangames')
        if not df_filtered.empty:
            treemap4 = px.treemap(df_filtered, path=['war', 'name'], values='clangames',
                                  title='Treemap of Clan Games by War Status',
                                  labels={'clangames': 'Clan Games', 'name': 'Player Name'},
                                  color='clangames', hover_data=['clangames'],
                                  color_continuous_scale='Viridis')
            treemaps.append(treemap4)

        # 5. Treemap based on 'war' and 'clangamesmaxed'
        df_filtered = filter_non_zero(self.df, 'clangamesmaxed')
        if not df_filtered.empty:
            treemap5 = px.treemap(df_filtered, path=['war', 'name'], values='clangamesmaxed',
                                  title='Treemap of Clan Games Maxed by War Status',
                                  labels={'clangamesmaxed': 'Clan Games Maxed', 'name': 'Player Name'},
                                  color='clangamesmaxed', hover_data=['clangamesmaxed'],
                                  color_continuous_scale='Viridis')
            treemaps.append(treemap5)

        return treemaps

    def create_sunburst_charts(self):
        """
        Generate sunburst visualizations for hierarchical metric breakdowns.

        Shows how individual players contribute to totals
        across status and war participation dimensions.

        Returns:
            list[plotly.graph_objects.Figure]: Sunburst chart figures
        """

        sunbursts = []

        # 1. Sunburst chart based on 'status' and 'warattack'
        df_filtered = self.df[self.df['warattack'].notna() & (self.df['warattack'] != 0)]
        if not df_filtered.empty:
            sunburst1 = px.sunburst(df_filtered, path=['status', 'name'], values='warattack',
                                    title='Sunburst of War Attack by Player Status',
                                    labels={'warattack': 'War Attack', 'name': 'Player Name'},
                                    color='warattack', hover_data=['warattack'],
                                    color_continuous_scale='Viridis')
            sunbursts.append(sunburst1)

        # 2. Sunburst chart based on 'war' and 'clancapital'
        df_filtered = self.df[self.df['clancapital'].notna() & (self.df['clancapital'] != 0)]
        if not df_filtered.empty:
            sunburst2 = px.sunburst(df_filtered, path=['war', 'name'], values='clancapital',
                                    title='Sunburst of Clan Capital by War Status',
                                    labels={'clancapital': 'Clan Capital', 'name': 'Player Name'},
                                    color='clancapital', hover_data=['clancapital'],
                                    color_continuous_scale='Viridis')
            sunbursts.append(sunburst2)

        # 3. Sunburst chart based on 'status' and 'clanscore'
        df_filtered = self.df[self.df['clanscore'].notna() & (self.df['clanscore'] != 0)]
        if not df_filtered.empty:
            sunburst3 = px.sunburst(df_filtered, path=['status', 'name'], values='clanscore',
                                    title='Sunburst of Clan Score by Player Status',
                                    labels={'clanscore': 'Clan Score', 'name': 'Player Name'},
                                    color='clanscore', hover_data=['clanscore'],
                                    color_continuous_scale='Viridis')
            sunbursts.append(sunburst3)

        # 4. Sunburst chart based on 'war' and 'clangames'
        df_filtered = self.df[self.df['clangames'].notna() & (self.df['clangames'] != 0)]
        if not df_filtered.empty:
            sunburst4 = px.sunburst(df_filtered, path=['war', 'name'], values='clangames',
                                    title='Sunburst of Clan Games by War Status',
                                    labels={'clangames': 'Clan Games', 'name': 'Player Name'},
                                    color='clangames', hover_data=['clangames'],
                                    color_continuous_scale='Viridis')
            sunbursts.append(sunburst4)

        # 5. Sunburst chart based on 'war' and 'clangamesmaxed'
        df_filtered = self.df[self.df['clangamesmaxed'].notna() & (self.df['clangamesmaxed'] != 0)]
        if not df_filtered.empty:
            sunburst5 = px.sunburst(df_filtered, path=['war', 'name'], values='clangamesmaxed',
                                    title='Sunburst of Clan Games Maxed by War Status',
                                    labels={'clangamesmaxed': 'Clan Games Maxed', 'name': 'Player Name'},
                                    color='clangamesmaxed', hover_data=['clangamesmaxed'],
                                    color_continuous_scale='Viridis')
            sunbursts.append(sunburst5)

        return sunbursts

    def create_density_plots(self):
        """
        Generate density contour plots for bivariate metric distributions.

        Analyzes concentration patterns between key performance metrics.

        Returns:
            list[plotly.graph_objects.Figure]: Density plot figures
        """

        density_plots = []

        # 1. Density plot of Clan Capital vs. Clan Games
        density1 = go.Figure()
        density1.add_trace(go.Histogram2dContour(
            x=self.df['clancapital'],
            y=self.df['clangames'],
            colorscale='Viridis',
            contours=dict(showlabels=True)
        ))
        density1.update_layout(
            title='Density Plot of Clan Capital vs. Clan Games',
            xaxis_title='Clan Capital',
            yaxis_title='Clan Games',
        )
        density_plots.append(density1)

        # 2. Density plot of Clan Score vs. War Attack
        density2 = go.Figure()
        density2.add_trace(go.Histogram2dContour(
            x=self.df['clanscore'],
            y=self.df['warattack'],
            colorscale='Viridis',
            contours=dict(showlabels=True)
        ))
        density2.update_layout(
            title='Density Plot of Clan Score vs. War Attack',
            xaxis_title='Clan Score',
            yaxis_title='War Attack',
        )
        density_plots.append(density2)

        # 3. Density plot of Clan Games vs. War Attack
        density3 = go.Figure()
        density3.add_trace(go.Histogram2dContour(
            x=self.df['clangames'],
            y=self.df['warattack'],
            colorscale='Viridis',
            contours=dict(showlabels=True)
        ))
        density3.update_layout(
            title='Density Plot of Clan Games vs. War Attack',
            xaxis_title='Clan Games',
            yaxis_title='War Attack',
        )
        density_plots.append(density3)

        # 4. Density plot of Clan Capital vs. Clan Score
        density4 = go.Figure()
        density4.add_trace(go.Histogram2dContour(
            x=self.df['clancapital'],
            y=self.df['clanscore'],
            colorscale='Viridis',
            contours=dict(showlabels=True)
        ))
        density4.update_layout(
            title='Density Plot of Clan Capital vs. Clan Score',
            xaxis_title='Clan Capital',
            yaxis_title='Clan Score',
        )
        density_plots.append(density4)

        return density_plots

    def create_3d_scatter_plots(self):
        """
        Generate 3D scatter plots for multi-metric comparison.

        Visualizes combinations of three numerical performance metrics
        with war participation as a categorical dimension.

        Returns:
            list[plotly.graph_objects.Figure]: 3D scatter plot figures
        """

        numerical_columns = ['warattack', 'clancapital', 'clangames', 'clangamesmaxed', 'clanscore']
        scatter_plots_3d = []

        # Generate 3D scatter plots for combinations of three different numerical columns
        for i, x_col in enumerate(numerical_columns):
            for j, y_col in enumerate(numerical_columns):
                for k, z_col in enumerate(numerical_columns):
                    if i < j < k:  # Ensure unique combinations
                        fig = px.scatter_3d(
                            self.df,
                            x=x_col,
                            y=y_col,
                            z=z_col,
                            color='war',  # Color by a categorical variable
                            hover_name='name',  # Display 'name' on hover
                            title=f'3D Scatter Plot: {x_col}, {y_col}, {z_col}'
                        )
                        scatter_plots_3d.append(fig)

        return scatter_plots_3d

    def create_area_graphs(self):
        """
        Generate area chart visualizations for cumulative comparisons.

        Includes:
        - IN vs OUT participation comparisons
        - Stacked area charts for numerical metrics

        Returns:
            list[plotly.graph_objects.Figure]: Area chart figures
        """

        # 1. Area Chart of Clan Capital Over Players (IN/OUT)
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=self.df_in['name'], y=self.df_in['clancapital'], fill='tozeroy', name='War IN'))
        fig1.add_trace(go.Scatter(x=self.df_out['name'], y=self.df_out['clancapital'], fill='tozeroy', name='War OUT'))
        fig1.update_layout(title='Area Chart of Clan Capital Over Players (IN/OUT)', xaxis_title='Name', yaxis_title='Clan Capital')

        # 2. Area Chart of Clan Games Over Players (IN/OUT)
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=self.df_in['name'], y=self.df_in['clangames'], fill='tozeroy', name='War IN'))
        fig2.add_trace(go.Scatter(x=self.df_out['name'], y=self.df_out['clangames'], fill='tozeroy', name='War OUT'))
        fig2.update_layout(title='Area Chart of Clan Games Over Players (IN/OUT)', xaxis_title='Name', yaxis_title='Clan Games')

        # 3. Area Chart of Clan Games Maxed Over Players (IN/OUT)
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=self.df_in['name'], y=self.df_in['clangamesmaxed'], fill='tozeroy', name='War IN'))
        fig3.add_trace(go.Scatter(x=self.df_out['name'], y=self.df_out['clangamesmaxed'], fill='tozeroy', name='War OUT'))
        fig3.update_layout(title='Area Chart of Clan Games Maxed Over Players (IN/OUT)', xaxis_title='Name', yaxis_title='Clan Games Maxed')

        # 4. Area Chart of Clan Score Over Players (IN/OUT)
        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(x=self.df_in['name'], y=self.df_in['clanscore'], fill='tozeroy', name='War IN'))
        fig4.add_trace(go.Scatter(x=self.df_out['name'], y=self.df_out['clanscore'], fill='tozeroy', name='War OUT'))
        fig4.update_layout(title='Area Chart of Clan Score Over Players (IN/OUT)', xaxis_title='Name', yaxis_title='Clan Score')

        # 5. Area Chart of War Attack Over Players (IN/OUT)
        fig5 = go.Figure()
        fig5.add_trace(go.Scatter(x=self.df_in['name'], y=self.df_in['warattack'], fill='tozeroy', name='War IN'))
        fig5.add_trace(go.Scatter(x=self.df_out['name'], y=self.df_out['warattack'], fill='tozeroy', name='War OUT'))
        fig5.update_layout(title='Area Chart of War Attack Over Players (IN/OUT)', xaxis_title='Name', yaxis_title='War Attack')

        # 6. Stacked Area Chart of Numerical Values
        fig6 = go.Figure()
        for column in self.numerical_df.columns:
            if column not in ['srno']:  # Exclude 'srno'
                fig6.add_trace(go.Scatter(x=self.df['name'], y=self.df[column], fill='tonexty', name=column))
        fig6.update_layout(title='Stacked Area Chart of Numerical Values', xaxis_title='Name', yaxis_title='Values')

        return [fig1, fig2, fig3, fig4, fig5, fig6]

    def create_polar_charts(self):
        """
        Generate polar chart visualizations for radial comparisons.

        Includes:
        - Metric comparisons by war participation
        - Stacked polar charts
        - Clan score distribution by player status

        Returns:
            list[plotly.graph_objects.Figure]: Polar chart figures
        """

        # 1. Polar Chart of Clan Capital Over Players (IN/OUT)
        fig1 = go.Figure()
        fig1.add_trace(go.Scatterpolar(r=self.df_in['clancapital'], theta=self.df_in['name'], fill='toself', name='War IN'))
        fig1.add_trace(go.Scatterpolar(r=self.df_out['clancapital'], theta=self.df_out['name'], fill='toself', name='War OUT'))
        fig1.update_layout(title='Polar Chart of Clan Capital Over Players (IN/OUT)', polar=dict(radialaxis=dict(visible=True)))

        # 2. Polar Chart of Clan Games Over Players (IN/OUT)
        fig2 = go.Figure()
        fig2.add_trace(go.Scatterpolar(r=self.df_in['clangames'], theta=self.df_in['name'], fill='toself', name='War IN'))
        fig2.add_trace(go.Scatterpolar(r=self.df_out['clangames'], theta=self.df_out['name'], fill='toself', name='War OUT'))
        fig2.update_layout(title='Polar Chart of Clan Games Over Players (IN/OUT)', polar=dict(radialaxis=dict(visible=True)))

        # 3. Polar Chart of Clan Games Maxed Over Players (IN/OUT)
        fig3 = go.Figure()
        fig3.add_trace(go.Scatterpolar(r=self.df_in['clangamesmaxed'], theta=self.df_in['name'], fill='toself', name='War IN'))
        fig3.add_trace(go.Scatterpolar(r=self.df_out['clangamesmaxed'], theta=self.df_out['name'], fill='toself', name='War OUT'))
        fig3.update_layout(title='Polar Chart of Clan Games Maxed Over Players (IN/OUT)', polar=dict(radialaxis=dict(visible=True)))

        # 4. Polar Chart of Clan Score Over Players (IN/OUT)
        fig4 = go.Figure()
        fig4.add_trace(go.Scatterpolar(r=self.df_in['clanscore'], theta=self.df_in['name'], fill='toself', name='War IN'))
        fig4.add_trace(go.Scatterpolar(r=self.df_out['clanscore'], theta=self.df_out['name'], fill='toself', name='War OUT'))
        fig4.update_layout(title='Polar Chart of Clan Score Over Players (IN/OUT)', polar=dict(radialaxis=dict(visible=True)))

        # 5. Polar Chart of War Attack Over Players (IN/OUT)
        fig5 = go.Figure()
        fig5.add_trace(go.Scatterpolar(r=self.df_in['warattack'], theta=self.df_in['name'], fill='toself', name='War IN'))
        fig5.add_trace(go.Scatterpolar(r=self.df_out['warattack'], theta=self.df_out['name'], fill='toself', name='War OUT'))
        fig5.update_layout(title='Polar Chart of War Attack Over Players (IN/OUT)', polar=dict(radialaxis=dict(visible=True)))

        # 6. Stacked Polar Chart of Numerical Values
        fig6 = go.Figure()
        for column in self.numerical_df.columns:
            if column not in ['srno']:  # Exclude 'srno'
                fig6.add_trace(go.Scatterpolar(r=self.df[column], theta=self.df['name'], fill='toself', name=column))
        fig6.update_layout(title='Stacked Polar Chart of Numerical Values', polar=dict(radialaxis=dict(visible=True)))

        # Clan Score by Status in a Polar Chart
        fig7 = go.Figure()
        fig7.add_trace(go.Scatterpolar(r=self.df['clanscore'], theta=self.df['status'], fill='toself', name='Clan Score by Status'))
        fig7.update_layout(title='Clan Score by Status', polar=dict(radialaxis=dict(visible=True)))

        return [fig1, fig2, fig3, fig4, fig5, fig6, fig7]

    def create_funnel_charts(self):
        """
        Generate funnel chart visualizations for ranked performance analysis.

        Includes:
        - Individual funnels per metric
        - Stacked funnels across numerical metrics

        Returns:
            list[plotly.graph_objects.Figure]: Funnel chart figures
        """

        figures = []

        # 1. Funnel Chart for Clan Capital
        df_sorted = self.df.sort_values(by='clancapital', ascending=False)
        fig1 = go.Figure()
        fig1.add_trace(go.Funnel(y=df_sorted['name'], x=df_sorted['clancapital'], textinfo="value+percent initial"))
        fig1.update_layout(title='Funnel Chart for Clan Capital', yaxis_title='Name', xaxis_title='Clan Capital')
        figures.append(fig1)

        # 2. Funnel Chart for Clan Games
        df_sorted = self.df.sort_values(by='clangames', ascending=False)
        fig2 = go.Figure()
        fig2.add_trace(go.Funnel(y=df_sorted['name'], x=df_sorted['clangames'], textinfo="value+percent initial"))
        fig2.update_layout(title='Funnel Chart for Clan Games', yaxis_title='Name', xaxis_title='Clan Games')
        figures.append(fig2)

        # 3. Funnel Chart for Clan Games Maxed
        df_sorted = self.df.sort_values(by='clangamesmaxed', ascending=False)
        fig3 = go.Figure()
        fig3.add_trace(go.Funnel(y=df_sorted['name'], x=df_sorted['clangamesmaxed'], textinfo="value+percent initial"))
        fig3.update_layout(title='Funnel Chart for Clan Games Maxed', yaxis_title='Name',
                           xaxis_title='Clan Games Maxed')
        figures.append(fig3)

        # 4. Funnel Chart for Clan Score
        df_sorted = self.df.sort_values(by='clanscore', ascending=False)
        fig4 = go.Figure()
        fig4.add_trace(go.Funnel(y=df_sorted['name'], x=df_sorted['clanscore'], textinfo="value+percent initial"))
        fig4.update_layout(title='Funnel Chart for Clan Score', yaxis_title='Name', xaxis_title='Clan Score')
        figures.append(fig4)

        # 5. Funnel Chart for War Attack
        df_sorted = self.df.sort_values(by='warattack', ascending=False)
        fig5 = go.Figure()
        fig5.add_trace(go.Funnel(y=df_sorted['name'], x=df_sorted['warattack'], textinfo="value+percent initial"))
        fig5.update_layout(title='Funnel Chart for War Attack', yaxis_title='Name', xaxis_title='War Attack')
        figures.append(fig5)

        # 6. Stacked Funnel Chart of Numerical Values
        fig6 = go.Figure()
        for column in self.numerical_df.columns:
            if column != 'srno':
                df_sorted = self.df.sort_values(by=column, ascending=False)
                fig6.add_trace(
                    go.Funnel(name=column, y=df_sorted['name'], x=df_sorted[column], textinfo="value+percent initial"))
        fig6.update_layout(title='Stacked Funnel Chart of Numerical Values', yaxis_title='Name', xaxis_title='Values')
        figures.append(fig6)

        return figures

    def create_waterfall_charts(self):
        """
        Generate waterfall chart visualizations for incremental contribution analysis.

        Includes:
        - Metric contribution per player
        - Stacked metric waterfalls
        - Aggregated changes by player status

        Returns:
            list[plotly.graph_objects.Figure]: Waterfall chart figures
        """

        # 1. Waterfall Chart for Clan Capital
        fig1 = go.Figure()
        fig1.add_trace(go.Waterfall(x=self.df['name'], y=self.df['clancapital'], textposition="outside"))
        fig1.update_layout(title='Waterfall Chart for Clan Capital', xaxis_title='Name', yaxis_title='Clan Capital')

        # 2. Waterfall Chart for Clan Games
        fig2 = go.Figure()
        fig2.add_trace(go.Waterfall(x=self.df['name'], y=self.df['clangames'], textposition="outside"))
        fig2.update_layout(title='Waterfall Chart for Clan Games', xaxis_title='Name', yaxis_title='Clan Games')

        # 3. Waterfall Chart for Clan Games Maxed
        fig3 = go.Figure()
        fig3.add_trace(go.Waterfall(x=self.df['name'], y=self.df['clangamesmaxed'], textposition="outside"))
        fig3.update_layout(title='Waterfall Chart for Clan Games Maxed', xaxis_title='Name', yaxis_title='Clan Games Maxed')

        # 4. Waterfall Chart for Clan Score
        fig4 = go.Figure()
        fig4.add_trace(go.Waterfall(x=self.df['name'], y=self.df['clanscore'], textposition="outside"))
        fig4.update_layout(title='Waterfall Chart for Clan Score', xaxis_title='Name', yaxis_title='Clan Score')

        # 5. Waterfall Chart for War Attack
        fig5 = go.Figure()
        fig5.add_trace(go.Waterfall(x=self.df['name'], y=self.df['warattack'], textposition="outside"))
        fig5.update_layout(title='Waterfall Chart for War Attack', xaxis_title='Name', yaxis_title='War Attack')

        # 6. Stacked Waterfall Chart of Numerical Values
        fig6 = go.Figure()
        for column in self.numerical_df.columns:
            if column not in ['srno']:  # Exclude 'srno'
                fig6.add_trace(go.Waterfall(name=column, x=self.df['name'], y=self.df[column], textposition="outside"))
        fig6.update_layout(title='Stacked Waterfall Chart of Numerical Values', xaxis_title='Name', yaxis_title='Values')

        # Incremental Changes in War Attack by Status
        fig7 = go.Figure()
        fig7.add_trace(go.Waterfall(x=self.df['status'], y=self.df.groupby('status')['warattack'].sum(), textposition="outside"))
        fig7.update_layout(title='Incremental Changes in War Attack by Status', xaxis_title='Status', yaxis_title='Total War Attack')

        return [fig1, fig2, fig3, fig4, fig5, fig6, fig7]