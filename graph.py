import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import warnings
import re
from datetime import datetime

from sklearn.linear_model import LinearRegression

warnings.simplefilter(action='ignore', category=FutureWarning)

LATEST_MONTH = "OCT_2025"
LATEST_MONTH_RANGE = "SEP-OCT_2025"
PREDICTED_MONTH = "OCT-NOV_2025"
CLAN_MONTHLY_PERFORMANCE_RANGE = "JUL_2024_to_OCT_2025"

class ClanMemberGraph:
    def __init__(self):
        self.data_url = ''
        self.df = None
        self.message = ""

    def update_data_url(self, month_year):
        # Update the data URL dynamically based on month and year
        self.data_url = f'https://raw.githubusercontent.com/Lightning-President-9/ClanDataRepo/main/Clan%20Members/JSON/{month_year}.json'

        # Fetch the updated data
        self.response = requests.get(self.data_url)
        try:
            self.json_data = self.response.json()
        except requests.exceptions.RequestException:
            self.message = f"No data available for {month_year}. Showing {LATEST_MONTH} (Latest)"
            self.update_data_url(LATEST_MONTH)

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

class FormerMemberGraph:
    def __init__(self):
        self.data_url = ''
        self.df = None
        self.message = ""

    def update_data_url(self, month_year):
        # Update the data URL dynamically based on the selected month and year
        self.data_url = f'https://raw.githubusercontent.com/Lightning-President-9/ClanDataRepo/main/Former%20Clan%20Members/JSON/{month_year}.json'

        # Fetch JSON data from the updated URL
        self.response = requests.get(self.data_url)
        try:
            self.json_data = self.response.json()
        except requests.exceptions.RequestException:
            self.message = f"No data available for {month_year}. Showing {LATEST_MONTH} (Latest)"
            self.update_data_url(LATEST_MONTH)

        # Load JSON data into a DataFrame
        self.df = pd.DataFrame(self.json_data)

        # Convert string columns to numeric where necessary
        for column in ['warattack', 'clancapital', 'clangames', 'clangamesmaxed', 'clanscore']:
            self.df[column] = pd.to_numeric(self.df[column], errors='coerce')

        # Select numerical columns for later use
        self.numerical_df = self.df.select_dtypes(include=['number'])

    def create_bar_graphs(self):
        # 1. Vertical Bar Chart of War Attack
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(x=self.df['name'], y=self.df['warattack'], name='War Attack'))
        fig1.update_layout(barmode='group', title='Vertical Bar Chart of War Attack', xaxis_title='Name', yaxis_title='War Attack')

        # 2. Vertical Bar Chart of Clan Capital
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=self.df['name'], y=self.df['clancapital'], name='Clan Capital'))
        fig2.update_layout(barmode='group', title='Vertical Bar Chart of Clan Capital', xaxis_title='Name', yaxis_title='Clan Capital')

        # 3. Vertical Bar Chart of Clan Games
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=self.df['name'], y=self.df['clangames'], name='Clan Games'))
        fig3.update_layout(barmode='group', title='Vertical Bar Chart of Clan Games', xaxis_title='Name', yaxis_title='Clan Games')

        # 4. Vertical Bar Chart of Clan Games Maxed
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(x=self.df['name'], y=self.df['clangamesmaxed'], name='Clan Games Maxed'))
        fig4.update_layout(barmode='group', title='Vertical Bar Chart of Clan Games Maxed', xaxis_title='Name', yaxis_title='Clan Games Maxed')

        # 5. Vertical Bar Chart of Clan Score
        fig5 = go.Figure()
        fig5.add_trace(go.Bar(x=self.df['name'], y=self.df['clanscore'], name='Clan Score'))
        fig5.update_layout(barmode='group', title='Vertical Bar Chart of Clan Score', xaxis_title='Name', yaxis_title='Clan Score')

        # 6. Stacked Bar Chart of Numerical Values
        fig6 = go.Figure()
        for column in self.numerical_df.columns:
            if column != 'srno':  # Exclude 'srno'
                fig6.add_trace(go.Bar(name=column, x=self.df['name'], y=self.df[column]))
        fig6.update_layout(barmode='stack', title='Stacked Bar Chart of Numerical Values', xaxis_title='Names', yaxis_title='Values')

        return [fig1, fig2, fig3, fig4, fig5, fig6]

    def create_pie_charts(self):
        # 1. Clan Capital Contribution
        self.df['clancapital_range'] = pd.cut(
            self.df['clancapital'],
            bins=[-1, 50, 100, 200, 300, float('inf')],
            labels=['0-50', '51-100', '101-200', '201-300', '300+']
        )
        fig1 = px.pie(self.df, names='clancapital_range', title='Clan Capital Contribution')

        # 2. Clan Games Participation
        self.df['clangames_range'] = pd.cut(self.df['clangames'], bins=[-1, 5, 10, 15, 20], labels=['0-5', '6-10', '11-15', '16-20'])
        fig2 = px.pie(self.df, names='clangames_range', title='Clan Games Participation')

        # 3. Maxed Clan Games
        maxed_games = self.df['clangamesmaxed'].value_counts()
        fig3 = go.Figure(data=[go.Pie(labels=maxed_games.index, values=maxed_games.values)])
        fig3.update_layout(title_text='Maxed Clan Games')

        # 4. Clan Score Distribution
        self.df['clanscore_range'] = pd.cut(self.df['clanscore'], bins=[-1, 100, 300, 500, 700], labels=['0-100', '101-300', '301-500', '501-700'])
        fig4 = px.pie(self.df, names='clanscore_range', title='Clan Score Distribution')

        # 5. War Attacks Distribution
        self.df['warattack_range'] = pd.cut(self.df['warattack'], bins=[-1, 50, 100, 200, 300], labels=['0-50', '51-100', '101-200', '201-300'])
        fig5 = px.pie(self.df, names='warattack_range', title='War Attacks Distribution')

        return [fig1, fig2, fig3, fig4, fig5]

    def create_line_charts(self):
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
        scatter_plots = []
        numerical_columns = self.numerical_df.columns.drop('srno', errors='ignore')

        # 1. Pairwise Scatter Plots with Hover Data
        for i, col1 in enumerate(numerical_columns):
            for col2 in numerical_columns[i + 1:]:
                fig = px.scatter(
                    self.df, x=col1, y=col2, hover_name='name',
                    title=f'Scatter Plot of {col1} vs {col2}',
                    labels={col1: col1.capitalize(), col2: col2.capitalize()}
                )
                scatter_plots.append(fig)

        # 2. Scatter Plot with Size by 'clanscore' and Hover Data
        if 'clanscore' in numerical_columns:
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

        return scatter_plots

    def create_histograms(self):
        histograms = []
        numerical_columns = self.numerical_df.columns.drop(['srno'], errors='ignore')

        # 1. Histogram for each numerical column
        for col in numerical_columns:
            fig = px.histogram(self.df, x=col, hover_data=['name'],
                               title=f'Histogram of {col}',
                               labels={col: col, 'count': 'Player Count'})
            histograms.append(fig)

        return histograms

    def create_box_plots(self):
        box_plots = []
        numerical_columns = self.numerical_df.columns.drop(['srno'], errors='ignore')

        # Box Plot for each numerical column
        for col in numerical_columns:
            fig = px.box(self.df, y=col, points="all", hover_data=['name'],
                         title=f'Box Plot of {col}',
                         labels={col: col, 'name': 'Player Name'})
            box_plots.append(fig)

        return box_plots

    def create_violin_plots(self):
        violin_plots = []
        numerical_columns = self.numerical_df.columns.drop(['srno'], errors='ignore')

        # Violin Plot for each numerical column
        for col in numerical_columns:
            fig = px.violin(self.df, y=col, box=True, points="all", hover_data=['name'],
                            title=f'Violin Plot of {col}',
                            labels={col: col, 'name': 'Player Name'})
            violin_plots.append(fig)

        return violin_plots

    def create_heatmaps(self):
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

        return heatmaps

    def create_treemaps(self):
        treemaps = []

        # Ensure there are no NaN or zero values in the values column
        def filter_non_zero(df, column):
            return df[df[column].fillna(0) != 0]

        # 1. Treemap based on 'warattack'
        df_filtered = filter_non_zero(self.df, 'warattack')
        if not df_filtered.empty:
            treemap1 = px.treemap(df_filtered, path=['name'], values='warattack',
                                  title='Treemap of War Attack by Player Name',
                                  labels={'warattack': 'War Attack', 'name': 'Player Name'},
                                  color='warattack', hover_data=['warattack'],
                                  color_continuous_scale='Viridis')
            treemaps.append(treemap1)

        # 2. Treemap based on 'clancapital'
        df_filtered = filter_non_zero(self.df, 'clancapital')
        if not df_filtered.empty:
            treemap2 = px.treemap(df_filtered, path=['name'], values='clancapital',
                                  title='Treemap of Clan Capital by Player Name',
                                  labels={'clancapital': 'Clan Capital', 'name': 'Player Name'},
                                  color='clancapital', hover_data=['clancapital'],
                                  color_continuous_scale='Viridis')
            treemaps.append(treemap2)

        # 3. Treemap based on 'clanscore'
        df_filtered = filter_non_zero(self.df, 'clanscore')
        if not df_filtered.empty:
            treemap3 = px.treemap(df_filtered, path=['name'], values='clanscore',
                                  title='Treemap of Clan Score by Player Name',
                                  labels={'clanscore': 'Clan Score', 'name': 'Player Name'},
                                  color='clanscore', hover_data=['clanscore'],
                                  color_continuous_scale='Viridis')
            treemaps.append(treemap3)

        # 4. Treemap based on 'clangames'
        df_filtered = filter_non_zero(self.df, 'clangames')
        if not df_filtered.empty:
            treemap4 = px.treemap(df_filtered, path=['name'], values='clangames',
                                  title='Treemap of Clan Games by Player Name',
                                  labels={'clangames': 'Clan Games', 'name': 'Player Name'},
                                  color='clangames', hover_data=['clangames'],
                                  color_continuous_scale='Viridis')
            treemaps.append(treemap4)

        # 5. Treemap based on 'clangamesmaxed'
        df_filtered = filter_non_zero(self.df, 'clangamesmaxed')
        if not df_filtered.empty:
            treemap5 = px.treemap(df_filtered, path=['name'], values='clangamesmaxed',
                                  title='Treemap of Clan Games Maxed by Player Name',
                                  labels={'clangamesmaxed': 'Clan Games Maxed', 'name': 'Player Name'},
                                  color='clangamesmaxed', hover_data=['clangamesmaxed'],
                                  color_continuous_scale='Viridis')
            treemaps.append(treemap5)

        return treemaps

    def create_sunburst_charts(self):
        sunbursts = []

        # Ensure there are no NaN or zero values in the values column
        def filter_non_zero(df, column):
            return df[df[column].fillna(0) != 0]

        # 1. Sunburst chart based on 'warattack'
        df_filtered = filter_non_zero(self.df, 'warattack')
        if not df_filtered.empty:
            sunburst1 = px.sunburst(df_filtered, path=['name'], values='warattack',
                                    title='Sunburst of War Attack by Player Name',
                                    labels={'warattack': 'War Attack', 'name': 'Player Name'},
                                    color='warattack', hover_data=['warattack'],
                                    color_continuous_scale='Viridis')
            sunbursts.append(sunburst1)

        # 2. Sunburst chart based on 'clancapital'
        df_filtered = filter_non_zero(self.df, 'clancapital')
        if not df_filtered.empty:
            sunburst2 = px.sunburst(df_filtered, path=['name'], values='clancapital',
                                    title='Sunburst of Clan Capital by Player Name',
                                    labels={'clancapital': 'Clan Capital', 'name': 'Player Name'},
                                    color='clancapital', hover_data=['clancapital'],
                                    color_continuous_scale='Viridis')
            sunbursts.append(sunburst2)

        # 3. Sunburst chart based on 'clanscore'
        df_filtered = filter_non_zero(self.df, 'clanscore')
        if not df_filtered.empty:
            sunburst3 = px.sunburst(df_filtered, path=['name'], values='clanscore',
                                    title='Sunburst of Clan Score by Player Name',
                                    labels={'clanscore': 'Clan Score', 'name': 'Player Name'},
                                    color='clanscore', hover_data=['clanscore'],
                                    color_continuous_scale='Viridis')
            sunbursts.append(sunburst3)

        # 4. Sunburst chart based on 'clangames'
        df_filtered = filter_non_zero(self.df, 'clangames')
        if not df_filtered.empty:
            sunburst4 = px.sunburst(df_filtered, path=['name'], values='clangames',
                                    title='Sunburst of Clan Games by Player Name',
                                    labels={'clangames': 'Clan Games', 'name': 'Player Name'},
                                    color='clangames', hover_data=['clangames'],
                                    color_continuous_scale='Viridis')
            sunbursts.append(sunburst4)

        # 5. Sunburst chart based on 'clangamesmaxed'
        df_filtered = filter_non_zero(self.df, 'clangamesmaxed')
        if not df_filtered.empty:
            sunburst5 = px.sunburst(df_filtered, path=['name'], values='clangamesmaxed',
                                    title='Sunburst of Clan Games Maxed by Player Name',
                                    labels={'clangamesmaxed': 'Clan Games Maxed', 'name': 'Player Name'},
                                    color='clangamesmaxed', hover_data=['clangamesmaxed'],
                                    color_continuous_scale='Viridis')
            sunbursts.append(sunburst5)

        return sunbursts

    def create_density_plots(self):
        density_plots = []

        # 1. Density plot of Clan Capital vs. Clan Games
        density1 = go.Figure()
        density1.add_trace(go.Histogram2dContour(
            x=self.df['clancapital'],
            y=self.df['clangames'],
            colorscale='Viridis',
            contours=dict(showlabels=True)  # Show labels on contours
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
                            # Replace 'war' with another column or remove the color parameter
                            hover_name='name',  # Display 'name' on hover
                            title=f'3D Scatter Plot: {x_col}, {y_col}, {z_col}'
                        )
                        scatter_plots_3d.append(fig)

        return scatter_plots_3d

    def create_area_graphs(self):
        # 1. Area Chart of Clan Capital Over Players
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=self.df['name'], y=self.df['clancapital'], fill='tozeroy', name='Clan Capital'))
        fig1.update_layout(title='Area Chart of Clan Capital Over Players', xaxis_title='Name', yaxis_title='Clan Capital')

        # 2. Area Chart of Clan Games Over Players
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=self.df['name'], y=self.df['clangames'], fill='tozeroy', name='Clan Games'))
        fig2.update_layout(title='Area Chart of Clan Games Over Players', xaxis_title='Name', yaxis_title='Clan Games')

        # 3. Area Chart of Clan Games Maxed Over Players
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=self.df['name'], y=self.df['clangamesmaxed'], fill='tozeroy', name='Clan Games Maxed'))
        fig3.update_layout(title='Area Chart of Clan Games Maxed Over Players', xaxis_title='Name', yaxis_title='Clan Games Maxed')

        # 4. Area Chart of Clan Score Over Players
        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(x=self.df['name'], y=self.df['clanscore'], fill='tozeroy', name='Clan Score'))
        fig4.update_layout(title='Area Chart of Clan Score Over Players', xaxis_title='Name', yaxis_title='Clan Score')

        # 5. Area Chart of War Attack Over Players
        fig5 = go.Figure()
        fig5.add_trace(go.Scatter(x=self.df['name'], y=self.df['warattack'], fill='tozeroy', name='War Attack'))
        fig5.update_layout(title='Area Chart of War Attack Over Players', xaxis_title='Name', yaxis_title='War Attack')

        # 6. Stacked Area Chart of Numerical Values
        fig6 = go.Figure()
        for column in self.numerical_df.columns:
            if column not in ['srno']:  # Exclude 'srno'
                fig6.add_trace(go.Scatter(x=self.df['name'], y=self.df[column], fill='tonexty', name=column))
        fig6.update_layout(title='Stacked Area Chart of Numerical Values', xaxis_title='Name', yaxis_title='Values')

        return [fig1, fig2, fig3, fig4, fig5, fig6]

    def create_polar_charts(self):
        # 1. Polar Chart of Clan Capital Over Players
        fig1 = go.Figure()
        fig1.add_trace(go.Scatterpolar(r=self.df['clancapital'], theta=self.df['name'], fill='toself', name='Clan Capital'))
        fig1.update_layout(title='Polar Chart of Clan Capital Over Players', polar=dict(radialaxis=dict(visible=True)))

        # 2. Polar Chart of Clan Games Over Players
        fig2 = go.Figure()
        fig2.add_trace(go.Scatterpolar(r=self.df['clangames'], theta=self.df['name'], fill='toself', name='Clan Games'))
        fig2.update_layout(title='Polar Chart of Clan Games Over Players', polar=dict(radialaxis=dict(visible=True)))

        # 3. Polar Chart of Clan Games Maxed Over Players
        fig3 = go.Figure()
        fig3.add_trace(go.Scatterpolar(r=self.df['clangamesmaxed'], theta=self.df['name'], fill='toself', name='Clan Games Maxed'))
        fig3.update_layout(title='Polar Chart of Clan Games Maxed Over Players', polar=dict(radialaxis=dict(visible=True)))

        # 4. Polar Chart of Clan Score Over Players
        fig4 = go.Figure()
        fig4.add_trace(go.Scatterpolar(r=self.df['clanscore'], theta=self.df['name'], fill='toself', name='Clan Score'))
        fig4.update_layout(title='Polar Chart of Clan Score Over Players', polar=dict(radialaxis=dict(visible=True)))

        # 5. Polar Chart of War Attack Over Players
        fig5 = go.Figure()
        fig5.add_trace(go.Scatterpolar(r=self.df['warattack'], theta=self.df['name'], fill='toself', name='War Attack'))
        fig5.update_layout(title='Polar Chart of War Attack Over Players', polar=dict(radialaxis=dict(visible=True)))

        # 6. Stacked Polar Chart of Numerical Values
        fig6 = go.Figure()
        for column in self.numerical_df.columns:
            if column not in ['srno']:  # Exclude 'srno'
                fig6.add_trace(go.Scatterpolar(r=self.df[column], theta=self.df['name'], fill='toself', name=column))
        fig6.update_layout(title='Stacked Polar Chart of Numerical Values', polar=dict(radialaxis=dict(visible=True)))

        return [fig1, fig2, fig3, fig4, fig5, fig6]

    def create_funnel_charts(self):
        # 1. Funnel Chart for Clan Capital
        sorted_df1 = self.df.sort_values(by='clancapital', ascending=False)
        fig1 = go.Figure()
        fig1.add_trace(go.Funnel(y=sorted_df1['name'], x=sorted_df1['clancapital'], textinfo="value+percent initial"))
        fig1.update_layout(title='Funnel Chart for Clan Capital', yaxis_title='Name', xaxis_title='Clan Capital')

        # 2. Funnel Chart for Clan Games
        sorted_df2 = self.df.sort_values(by='clangames', ascending=False)
        fig2 = go.Figure()
        fig2.add_trace(go.Funnel(y=sorted_df2['name'], x=sorted_df2['clangames'], textinfo="value+percent initial"))
        fig2.update_layout(title='Funnel Chart for Clan Games', yaxis_title='Name', xaxis_title='Clan Games')

        # 3. Funnel Chart for Clan Games Maxed
        sorted_df3 = self.df.sort_values(by='clangamesmaxed', ascending=False)
        fig3 = go.Figure()
        fig3.add_trace(
            go.Funnel(y=sorted_df3['name'], x=sorted_df3['clangamesmaxed'], textinfo="value+percent initial"))
        fig3.update_layout(title='Funnel Chart for Clan Games Maxed', yaxis_title='Name',
                           xaxis_title='Clan Games Maxed')

        # 4. Funnel Chart for Clan Score
        sorted_df4 = self.df.sort_values(by='clanscore', ascending=False)
        fig4 = go.Figure()
        fig4.add_trace(go.Funnel(y=sorted_df4['name'], x=sorted_df4['clanscore'], textinfo="value+percent initial"))
        fig4.update_layout(title='Funnel Chart for Clan Score', yaxis_title='Name', xaxis_title='Clan Score')

        # 5. Funnel Chart for War Attack
        sorted_df5 = self.df.sort_values(by='warattack', ascending=False)
        fig5 = go.Figure()
        fig5.add_trace(go.Funnel(y=sorted_df5['name'], x=sorted_df5['warattack'], textinfo="value+percent initial"))
        fig5.update_layout(title='Funnel Chart for War Attack', yaxis_title='Name', xaxis_title='War Attack')

        # 6. Stacked Funnel Chart of Numerical Values
        fig6 = go.Figure()
        for column in self.numerical_df.columns:
            if column not in ['srno']:  # Exclude 'srno'
                sorted_df_col = self.df.sort_values(by=column, ascending=False)
                fig6.add_trace(go.Funnel(name=column, y=sorted_df_col['name'], x=sorted_df_col[column],
                                         textinfo="value+percent initial"))
        fig6.update_layout(title='Stacked Funnel Chart of Numerical Values', yaxis_title='Name', xaxis_title='Values')

        return [fig1, fig2, fig3, fig4, fig5, fig6]

    def create_waterfall_charts(self):
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

        return [fig1, fig2, fig3, fig4, fig5, fig6]

class MonthlyAnalysisGraph:
    def __init__(self):
        self.data_url = ''
        self.df = None
        self.message = ""

    def update_data_url(self, month_year):
        # Update the data URL dynamically based on month and year
        self.data_url = f'https://raw.githubusercontent.com/Lightning-President-9/ClanDataRepo/refs/heads/main/Clan%20Members/Monthly%20Analysis%20JSON/data_{month_year}.json'

        # Fetch the updated data
        self.response = requests.get(self.data_url)
        try:
            self.json_data = self.response.json()
        except requests.exceptions.RequestException:
            self.message = f"No data available for {month_year}. Showing {LATEST_MONTH_RANGE} (Latest)"
            self.update_data_url(LATEST_MONTH_RANGE)

        # Load JSON data into a DataFrame
        self.df = pd.DataFrame(self.json_data)

        # Convert string columns to numeric
        for column in ['warattack', 'clancapital', 'clangames', 'clangamesmaxed', 'clanscore']:
            self.df[column] = pd.to_numeric(self.df[column], errors='coerce')

        self.numerical_df = self.df.select_dtypes(include=['number'])

    def create_bar_graphs(self):
        # 1. Vertical Bar Chart of War Attack
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(x=self.df['name'], y=self.df['warattack'], name='War Attack'))
        fig1.update_layout(barmode='group', title='Vertical Bar Chart of War Attack', xaxis_title='Name', yaxis_title='War Attack')

        # 2. Vertical Bar Chart of Clan Capital
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=self.df['name'], y=self.df['clancapital'], name='Clan Capital'))
        fig2.update_layout(barmode='group', title='Vertical Bar Chart of Clan Capital', xaxis_title='Name', yaxis_title='Clan Capital')

        # 3. Vertical Bar Chart of Clan Games
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=self.df['name'], y=self.df['clangames'], name='Clan Games'))
        fig3.update_layout(barmode='group', title='Vertical Bar Chart of Clan Games', xaxis_title='Name', yaxis_title='Clan Games')

        # 4. Vertical Bar Chart of Clan Games Maxed
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(x=self.df['name'], y=self.df['clangamesmaxed'], name='Clan Games Maxed'))
        fig4.update_layout(barmode='group', title='Vertical Bar Chart of Clan Games Maxed', xaxis_title='Name', yaxis_title='Clan Games Maxed')

        # 5. Vertical Bar Chart of Clan Score
        fig5 = go.Figure()
        fig5.add_trace(go.Bar(x=self.df['name'], y=self.df['clanscore'], name='Clan Score'))
        fig5.update_layout(barmode='group', title='Vertical Bar Chart of Clan Score', xaxis_title='Name', yaxis_title='Clan Score')

        # 6. Stacked Bar Chart of Numerical Values
        fig6 = go.Figure()
        for column in self.numerical_df.columns:
            if column != 'srno':  # Exclude 'srno'
                fig6.add_trace(go.Bar(name=column, x=self.df['name'], y=self.df[column]))
        fig6.update_layout(barmode='stack', title='Stacked Bar Chart of Numerical Values', xaxis_title='Names', yaxis_title='Values')

        return [fig1, fig2, fig3, fig4, fig5, fig6]

    def create_pie_charts(self):
        # 1. Clan Capital Contribution
        self.df['clancapital_range'] = pd.cut(self.df['clancapital'], bins=[-1, 50, 100, 200, 300], labels=['0-50', '51-100', '101-200', '201-300'])
        fig1 = px.pie(self.df, names='clancapital_range', title='Clan Capital Contribution')

        # 2. Clan Games Participation
        self.df['clangames_range'] = pd.cut(self.df['clangames'], bins=[-1, 5, 10, 15, 20], labels=['0-5', '6-10', '11-15', '16-20'])
        fig2 = px.pie(self.df, names='clangames_range', title='Clan Games Participation')

        # 3. Maxed Clan Games
        maxed_games = self.df['clangamesmaxed'].value_counts()
        fig3 = go.Figure(data=[go.Pie(labels=maxed_games.index, values=maxed_games.values)])
        fig3.update_layout(title_text='Maxed Clan Games')

        # 4. Clan Score Distribution
        self.df['clanscore_range'] = pd.cut(self.df['clanscore'], bins=[-1, 100, 300, 500, 700], labels=['0-100', '101-300', '301-500', '501-700'])
        fig4 = px.pie(self.df, names='clanscore_range', title='Clan Score Distribution')

        # 5. War Attacks Distribution
        self.df['warattack_range'] = pd.cut(self.df['warattack'], bins=[-1, 50, 100, 200, 300], labels=['0-50', '51-100', '101-200', '201-300'])
        fig5 = px.pie(self.df, names='warattack_range', title='War Attacks Distribution')

        return [fig1, fig2, fig3, fig4, fig5]

    def create_line_charts(self):
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
        scatter_plots = []
        numerical_columns = self.numerical_df.columns.drop('srno', errors='ignore')

        # 1. Pairwise Scatter Plots with Hover Data
        for i, col1 in enumerate(numerical_columns):
            for col2 in numerical_columns[i + 1:]:
                fig = px.scatter(
                    self.df, x=col1, y=col2, hover_name='name',
                    title=f'Scatter Plot of {col1} vs {col2}',
                    labels={col1: col1.capitalize(), col2: col2.capitalize()}
                )
                scatter_plots.append(fig)

        # 2. Scatter Plot with Size by 'clanscore' and Hover Data
        if 'clanscore' in numerical_columns:
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

        return scatter_plots

    def create_histograms(self):
        histograms = []
        numerical_columns = self.numerical_df.columns.drop(['srno'], errors='ignore')

        # 1. Histogram for each numerical column
        for col in numerical_columns:
            fig = px.histogram(self.df, x=col, hover_data=['name'],
                               title=f'Histogram of {col}',
                               labels={col: col, 'count': 'Player Count'})
            histograms.append(fig)

        return histograms

    def create_box_plots(self):
        box_plots = []
        numerical_columns = self.numerical_df.columns.drop(['srno'], errors='ignore')

        # Box Plot for each numerical column
        for col in numerical_columns:
            fig = px.box(self.df, y=col, points="all", hover_data=['name'],
                         title=f'Box Plot of {col}',
                         labels={col: col, 'name': 'Player Name'})
            box_plots.append(fig)

        return box_plots

    def create_violin_plots(self):
        violin_plots = []
        numerical_columns = self.numerical_df.columns.drop(['srno'], errors='ignore')

        # Violin Plot for each numerical column
        for col in numerical_columns:
            fig = px.violin(self.df, y=col, box=True, points="all", hover_data=['name'],
                            title=f'Violin Plot of {col}',
                            labels={col: col, 'name': 'Player Name'})
            violin_plots.append(fig)

        return violin_plots

    def create_heatmaps(self):
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

        return heatmaps

    def create_treemaps(self):
        treemaps = []

        # Ensure there are no NaN or zero values in the values column
        def filter_non_zero(df, column):
            return df[df[column].fillna(0) != 0]

        # 1. Treemap based on 'warattack'
        df_filtered = filter_non_zero(self.df, 'warattack')
        if not df_filtered.empty:
            treemap1 = px.treemap(df_filtered, path=['name'], values='warattack',
                                  title='Treemap of War Attack by Player Name',
                                  labels={'warattack': 'War Attack', 'name': 'Player Name'},
                                  color='warattack', hover_data=['warattack'],
                                  color_continuous_scale='Viridis')
            treemaps.append(treemap1)

        # 2. Treemap based on 'clancapital'
        df_filtered = filter_non_zero(self.df, 'clancapital')
        if not df_filtered.empty:
            treemap2 = px.treemap(df_filtered, path=['name'], values='clancapital',
                                  title='Treemap of Clan Capital by Player Name',
                                  labels={'clancapital': 'Clan Capital', 'name': 'Player Name'},
                                  color='clancapital', hover_data=['clancapital'],
                                  color_continuous_scale='Viridis')
            treemaps.append(treemap2)

        # 3. Treemap based on 'clanscore'
        df_filtered = filter_non_zero(self.df, 'clanscore')
        if not df_filtered.empty:
            treemap3 = px.treemap(df_filtered, path=['name'], values='clanscore',
                                  title='Treemap of Clan Score by Player Name',
                                  labels={'clanscore': 'Clan Score', 'name': 'Player Name'},
                                  color='clanscore', hover_data=['clanscore'],
                                  color_continuous_scale='Viridis')
            treemaps.append(treemap3)

        # 4. Treemap based on 'clangames'
        df_filtered = filter_non_zero(self.df, 'clangames')
        if not df_filtered.empty:
            treemap4 = px.treemap(df_filtered, path=['name'], values='clangames',
                                  title='Treemap of Clan Games by Player Name',
                                  labels={'clangames': 'Clan Games', 'name': 'Player Name'},
                                  color='clangames', hover_data=['clangames'],
                                  color_continuous_scale='Viridis')
            treemaps.append(treemap4)

        # 5. Treemap based on 'clangamesmaxed'
        df_filtered = filter_non_zero(self.df, 'clangamesmaxed')
        if not df_filtered.empty:
            treemap5 = px.treemap(df_filtered, path=['name'], values='clangamesmaxed',
                                  title='Treemap of Clan Games Maxed by Player Name',
                                  labels={'clangamesmaxed': 'Clan Games Maxed', 'name': 'Player Name'},
                                  color='clangamesmaxed', hover_data=['clangamesmaxed'],
                                  color_continuous_scale='Viridis')
            treemaps.append(treemap5)

        return treemaps

    def create_sunburst_charts(self):
        sunbursts = []

        # Ensure there are no NaN or zero values in the values column
        def filter_non_zero(df, column):
            return df[df[column].fillna(0) != 0]

        # 1. Sunburst chart based on 'warattack'
        df_filtered = filter_non_zero(self.df, 'warattack')
        if not df_filtered.empty:
            sunburst1 = px.sunburst(df_filtered, path=['name'], values='warattack',
                                    title='Sunburst of War Attack by Player Name',
                                    labels={'warattack': 'War Attack', 'name': 'Player Name'},
                                    color='warattack', hover_data=['warattack'],
                                    color_continuous_scale='Viridis')
            sunbursts.append(sunburst1)

        # 2. Sunburst chart based on 'clancapital'
        df_filtered = filter_non_zero(self.df, 'clancapital')
        if not df_filtered.empty:
            sunburst2 = px.sunburst(df_filtered, path=['name'], values='clancapital',
                                    title='Sunburst of Clan Capital by Player Name',
                                    labels={'clancapital': 'Clan Capital', 'name': 'Player Name'},
                                    color='clancapital', hover_data=['clancapital'],
                                    color_continuous_scale='Viridis')
            sunbursts.append(sunburst2)

        # 3. Sunburst chart based on 'clanscore'
        df_filtered = filter_non_zero(self.df, 'clanscore')
        if not df_filtered.empty:
            sunburst3 = px.sunburst(df_filtered, path=['name'], values='clanscore',
                                    title='Sunburst of Clan Score by Player Name',
                                    labels={'clanscore': 'Clan Score', 'name': 'Player Name'},
                                    color='clanscore', hover_data=['clanscore'],
                                    color_continuous_scale='Viridis')
            sunbursts.append(sunburst3)

        # 4. Sunburst chart based on 'clangames'
        df_filtered = filter_non_zero(self.df, 'clangames')
        if not df_filtered.empty:
            sunburst4 = px.sunburst(df_filtered, path=['name'], values='clangames',
                                    title='Sunburst of Clan Games by Player Name',
                                    labels={'clangames': 'Clan Games', 'name': 'Player Name'},
                                    color='clangames', hover_data=['clangames'],
                                    color_continuous_scale='Viridis')
            sunbursts.append(sunburst4)

        # 5. Sunburst chart based on 'clangamesmaxed'
        df_filtered = filter_non_zero(self.df, 'clangamesmaxed')
        if not df_filtered.empty:
            sunburst5 = px.sunburst(df_filtered, path=['name'], values='clangamesmaxed',
                                    title='Sunburst of Clan Games Maxed by Player Name',
                                    labels={'clangamesmaxed': 'Clan Games Maxed', 'name': 'Player Name'},
                                    color='clangamesmaxed', hover_data=['clangamesmaxed'],
                                    color_continuous_scale='Viridis')
            sunbursts.append(sunburst5)

        return sunbursts

    def create_density_plots(self):
        density_plots = []

        # 1. Density plot of Clan Capital vs. Clan Games
        density1 = go.Figure()
        density1.add_trace(go.Histogram2dContour(
            x=self.df['clancapital'],
            y=self.df['clangames'],
            colorscale='Viridis',
            contours=dict(showlabels=True)  # Show labels on contours
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
                            # Replace 'war' with another column or remove the color parameter
                            hover_name='name',  # Display 'name' on hover
                            title=f'3D Scatter Plot: {x_col}, {y_col}, {z_col}'
                        )
                        scatter_plots_3d.append(fig)

        return scatter_plots_3d

    def create_area_graphs(self):
        # 1. Area Chart of Clan Capital Over Players
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=self.df['name'], y=self.df['clancapital'], fill='tozeroy', name='Clan Capital'))
        fig1.update_layout(title='Area Chart of Clan Capital Over Players', xaxis_title='Name', yaxis_title='Clan Capital')

        # 2. Area Chart of Clan Games Over Players
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=self.df['name'], y=self.df['clangames'], fill='tozeroy', name='Clan Games'))
        fig2.update_layout(title='Area Chart of Clan Games Over Players', xaxis_title='Name', yaxis_title='Clan Games')

        # 3. Area Chart of Clan Games Maxed Over Players
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=self.df['name'], y=self.df['clangamesmaxed'], fill='tozeroy', name='Clan Games Maxed'))
        fig3.update_layout(title='Area Chart of Clan Games Maxed Over Players', xaxis_title='Name', yaxis_title='Clan Games Maxed')

        # 4. Area Chart of Clan Score Over Players
        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(x=self.df['name'], y=self.df['clanscore'], fill='tozeroy', name='Clan Score'))
        fig4.update_layout(title='Area Chart of Clan Score Over Players', xaxis_title='Name', yaxis_title='Clan Score')

        # 5. Area Chart of War Attack Over Players
        fig5 = go.Figure()
        fig5.add_trace(go.Scatter(x=self.df['name'], y=self.df['warattack'], fill='tozeroy', name='War Attack'))
        fig5.update_layout(title='Area Chart of War Attack Over Players', xaxis_title='Name', yaxis_title='War Attack')

        # 6. Stacked Area Chart of Numerical Values
        fig6 = go.Figure()
        for column in self.numerical_df.columns:
            if column not in ['srno']:  # Exclude 'srno'
                fig6.add_trace(go.Scatter(x=self.df['name'], y=self.df[column], fill='tonexty', name=column))
        fig6.update_layout(title='Stacked Area Chart of Numerical Values', xaxis_title='Name', yaxis_title='Values')

        return [fig1, fig2, fig3, fig4, fig5, fig6]

    def create_polar_charts(self):
        # 1. Polar Chart of Clan Capital Over Players
        fig1 = go.Figure()
        fig1.add_trace(go.Scatterpolar(r=self.df['clancapital'], theta=self.df['name'], fill='toself', name='Clan Capital'))
        fig1.update_layout(title='Polar Chart of Clan Capital Over Players', polar=dict(radialaxis=dict(visible=True)))

        # 2. Polar Chart of Clan Games Over Players
        fig2 = go.Figure()
        fig2.add_trace(go.Scatterpolar(r=self.df['clangames'], theta=self.df['name'], fill='toself', name='Clan Games'))
        fig2.update_layout(title='Polar Chart of Clan Games Over Players', polar=dict(radialaxis=dict(visible=True)))

        # 3. Polar Chart of Clan Games Maxed Over Players
        fig3 = go.Figure()
        fig3.add_trace(go.Scatterpolar(r=self.df['clangamesmaxed'], theta=self.df['name'], fill='toself', name='Clan Games Maxed'))
        fig3.update_layout(title='Polar Chart of Clan Games Maxed Over Players', polar=dict(radialaxis=dict(visible=True)))

        # 4. Polar Chart of Clan Score Over Players
        fig4 = go.Figure()
        fig4.add_trace(go.Scatterpolar(r=self.df['clanscore'], theta=self.df['name'], fill='toself', name='Clan Score'))
        fig4.update_layout(title='Polar Chart of Clan Score Over Players', polar=dict(radialaxis=dict(visible=True)))

        # 5. Polar Chart of War Attack Over Players
        fig5 = go.Figure()
        fig5.add_trace(go.Scatterpolar(r=self.df['warattack'], theta=self.df['name'], fill='toself', name='War Attack'))
        fig5.update_layout(title='Polar Chart of War Attack Over Players', polar=dict(radialaxis=dict(visible=True)))

        # 6. Stacked Polar Chart of Numerical Values
        fig6 = go.Figure()
        for column in self.numerical_df.columns:
            if column not in ['srno']:  # Exclude 'srno'
                fig6.add_trace(go.Scatterpolar(r=self.df[column], theta=self.df['name'], fill='toself', name=column))
        fig6.update_layout(title='Stacked Polar Chart of Numerical Values', polar=dict(radialaxis=dict(visible=True)))

        return [fig1, fig2, fig3, fig4, fig5, fig6]

    def create_funnel_charts(self):
        # 1. Funnel Chart for Clan Capital
        df1 = self.df.sort_values(by='clancapital', ascending=False)
        fig1 = go.Figure()
        fig1.add_trace(go.Funnel(y=df1['name'], x=df1['clancapital'], textinfo="value+percent initial"))
        fig1.update_layout(title='Funnel Chart for Clan Capital', yaxis_title='Name', xaxis_title='Clan Capital')

        # 2. Funnel Chart for Clan Games
        df2 = self.df.sort_values(by='clangames', ascending=False)
        fig2 = go.Figure()
        fig2.add_trace(go.Funnel(y=df2['name'], x=df2['clangames'], textinfo="value+percent initial"))
        fig2.update_layout(title='Funnel Chart for Clan Games', yaxis_title='Name', xaxis_title='Clan Games')

        # 3. Funnel Chart for Clan Games Maxed
        df3 = self.df.sort_values(by='clangamesmaxed', ascending=False)
        fig3 = go.Figure()
        fig3.add_trace(go.Funnel(y=df3['name'], x=df3['clangamesmaxed'], textinfo="value+percent initial"))
        fig3.update_layout(title='Funnel Chart for Clan Games Maxed', yaxis_title='Name',
                           xaxis_title='Clan Games Maxed')

        # 4. Funnel Chart for Clan Score
        df4 = self.df.sort_values(by='clanscore', ascending=False)
        fig4 = go.Figure()
        fig4.add_trace(go.Funnel(y=df4['name'], x=df4['clanscore'], textinfo="value+percent initial"))
        fig4.update_layout(title='Funnel Chart for Clan Score', yaxis_title='Name', xaxis_title='Clan Score')

        # 5. Funnel Chart for War Attack
        df5 = self.df.sort_values(by='warattack', ascending=False)
        fig5 = go.Figure()
        fig5.add_trace(go.Funnel(y=df5['name'], x=df5['warattack'], textinfo="value+percent initial"))
        fig5.update_layout(title='Funnel Chart for War Attack', yaxis_title='Name', xaxis_title='War Attack')

        # 6. Stacked Funnel Chart of Numerical Values
        fig6 = go.Figure()
        for column in self.numerical_df.columns:
            if column not in ['srno']:  # Exclude 'srno'
                df_sorted = self.df.sort_values(by=column, ascending=False)
                fig6.add_trace(
                    go.Funnel(name=column, y=df_sorted['name'], x=df_sorted[column], textinfo="value+percent initial"))
        fig6.update_layout(title='Stacked Funnel Chart of Numerical Values', yaxis_title='Name', xaxis_title='Values')

        return [fig1, fig2, fig3, fig4, fig5, fig6]

    def create_waterfall_charts(self):
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

        return [fig1, fig2, fig3, fig4, fig5, fig6]

class AllMonthGraph:
    def __init__(self):
        self.base_url = (
            "https://raw.githubusercontent.com/Lightning-President-9/"
            "ClanDataRepo/refs/heads/main/Clan%20Members/Monthly%20Analysis%20JSON/"
        )
        self.folder_url = (
            "https://github.com/Lightning-President-9/"
            "ClanDataRepo/tree/main/Clan%20Members/Monthly%20Analysis%20JSON"
        )
        self.months = self.get_available_months()   # Dynamic month loading

    def get_available_months(self):
        """Scrape GitHub HTML page to list JSON files."""
        response = requests.get(self.folder_url)
        response.raise_for_status()
        html = response.text

        # Extract filenames data_XXX.json
        files = re.findall(r"data_([A-Z\-0-9_]+)\.json", html)

        # 🔥 Remove duplicates while preserving order
        files = list(dict.fromkeys(files))

        # Proper sort
        files = self.sort_month_pairs(files)

        # Start from JUN-JUL_2024
        START = "JUN-JUL_2024"
        if START in files:
            files = files[files.index(START):]

        return files

    def sort_month_pairs(self, pairs):
        MONTH_MAP = {
            'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4,
            'MAY': 5, 'JUN': 6, 'JUL': 7, 'AUG': 8,
            'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12
        }

        def pair_to_date(pair):
            # Example: NOV-DEC_2024
            part, year = pair.split("_")
            s, e = part.split("-")

            year = int(year)
            if s == "DEC" and e == "JAN":
                year -= 1  # DEC-JAN belongs to previous year

            return datetime(year, MONTH_MAP[s], 1)

        return sorted(pairs, key=pair_to_date)

    def fetch_data(self):
        all_data = {}
        for month in self.months:
            url = f"{self.base_url}data_{month}.json"
            response = requests.get(url)
            response.raise_for_status()
            all_data[month] = response.json()
        return all_data

    def process_data(self, all_data):
        monthly_totals = []

        for month, records in all_data.items():
            totals = {
                "month": month,
                "warattack": 0,
                "clancapital": 0,
                "clangames": 0,
                "clangamesmaxed": 0,
                "clanscore": 0,
            }

            for r in records:
                totals["warattack"] += int(r.get("warattack", 0))
                totals["clancapital"] += int(r.get("clancapital", 0))
                totals["clangames"] += int(r.get("clangames", 0))
                totals["clangamesmaxed"] += int(r.get("clangamesmaxed", 0))
                totals["clanscore"] += int(r.get("clanscore", 0))

            monthly_totals.append(totals)

        df = pd.DataFrame(monthly_totals)

        # Maintain sorted month order
        df["month"] = pd.Categorical(df["month"], categories=self.months, ordered=True)
        df = df.sort_values("month")

        return df

    def generate_heatmap_figures(self):
        url = (
            "https://raw.githubusercontent.com/Lightning-President-9/ClanDataRepo/"
            "refs/heads/main/Clan%20Members/Clan%20Monthly%20Performance%20JSON/"
            "clan_monthly_performance_"+CLAN_MONTHLY_PERFORMANCE_RANGE+".json"
        )
        response = requests.get(url)
        response.raise_for_status()

        df = pd.DataFrame(response.json())

        metrics = ['warattack', 'clancapital', 'clangames', 'clangamesmaxed', 'clanscore']
        figures = []

        for metric in metrics:
            heatmap_df = df.set_index("name")[
                [col for col in df.columns if col.startswith(metric + "_")]
            ]
            heatmap_df.replace(-1, None, inplace=True)

            fig = px.imshow(
                heatmap_df,
                labels=dict(
                    x="Month",
                    y="Player",
                    color=metric.replace("clangamesmaxed", "Clan Games Maxed")
                          .capitalize().replace("_", " ")
                ),
                x=[col.replace(f"{metric}_", "") for col in heatmap_df.columns],
                y=heatmap_df.index,
                title=f"Heatmap of {metric.replace('clangamesmaxed', 'Clan Games Maxed').capitalize()} per Month",
                aspect="auto",
                color_continuous_scale='Plasma'
            )

            fig.update_yaxes(tickfont=dict(size=10))
            figures.append(fig)

        return figures

    def plot_graphs(self, df):
        df_long = df.melt(id_vars=["month"], var_name="Category", value_name="Total")

        fig1 = px.line(
            df_long, x="month", y="Total", color="Category", markers=True,
            title="Monthly Clan Performance"
        )

        fig2 = px.bar(
            df_long, x="month", y="Total", color="Category", barmode="group",
            title="Monthly Clan Performance (Bar Graph)"
        )

        fig3 = px.treemap(
            df_long, path=["month", "Category"], values="Total",
            title="Hierarchical Clan Performance Breakdown"
        )

        fig4 = px.area(
            df_long, x="month", y="Total", color="Category",
            title="Monthly Clan Performance (Area Chart)"
        )

        return [fig1, fig2, fig3, fig4]

class AI_PRED:
    def __init__(self):
        self.main_data_url = "https://raw.githubusercontent.com/Lightning-President-9/ClanDataRepo/refs/heads/main/Clan%20Members/Clan%20Monthly%20Performance%20JSON/clan_monthly_performance_"+CLAN_MONTHLY_PERFORMANCE_RANGE+".json"
        self.filter_names_url = "https://raw.githubusercontent.com/Lightning-President-9/ClanDataRepo/refs/heads/main/Clan%20Members/JSON/"+LATEST_MONTH+".json"

        self.month_map = {
            "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
            "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12
        }

        self.df_filtered = self._load_and_filter_data()

    def _load_and_filter_data(self):
        main_data = requests.get(self.main_data_url).json()
        df = pd.DataFrame(main_data)
        df.replace(-1, 0, inplace=True)

        may_data = requests.get(self.filter_names_url).json()
        valid_names_upper = {entry['name'].strip().upper() for entry in may_data}

        df_filtered = df[df['name'].str.strip().str.upper().isin(valid_names_upper)].copy()
        df_filtered.reset_index(drop=True, inplace=True)
        return df_filtered

    def _period_sort_key(self, col_name, prefix):
        """
        Converts 'dec-jan_2025' into a sortable tuple.
        """
        period = col_name.replace(prefix, "").lower()   # e.g., "dec-jan_2025"
        range_part, year_str = period.split("_")        # "dec-jan", "2025"
        start_m, end_m = range_part.split("-")

        # Year correction:
        # "dec-jan_2025" means Dec 2024 to Jan 2025
        y_end = int(year_str)
        y_start = y_end if self.month_map[start_m] < self.month_map[end_m] else y_end - 1

        return (y_start, self.month_map[start_m], y_end, self.month_map[end_m])

    def forecast_plot(self, prefix):
        df = self.df_filtered
        metric_cols = [col for col in df.columns if col.startswith(prefix)]

        # Sort columns chronologically using the FIXED sort key
        sorted_cols = sorted(
            metric_cols,
            key=lambda col: self._period_sort_key(col, prefix)
        )

        periods = [col.replace(prefix, "").upper() for col in sorted_cols]

        fig = go.Figure()
        buttons = []

        for i, name in enumerate(df["name"]):
            row = df[df["name"] == name]
            values = row[sorted_cols].values.flatten()
            X = list(range(len(values)))

            # Linear regression model
            model = LinearRegression().fit(pd.DataFrame(X), values)
            forecast = model.predict([[len(X)]])[0]
            pred_line = model.predict(pd.DataFrame(X + [len(X)]))

            # Plot
            trace_actual = go.Scatter(
                x=periods,
                y=values,
                mode="lines+markers",
                name="Actual"
            )

            trace_fit = go.Scatter(
                x=periods + [PREDICTED_MONTH],
                y=list(pred_line),
                mode="lines",
                name="Linear Fit"
            )

            trace_forecast = go.Scatter(
                x=[PREDICTED_MONTH],
                y=[forecast],
                mode="markers+text",
                name="Forecast",
                marker=dict(size=10, color="green"),
                text=[f"{forecast:.1f}"],
                textposition="top center"
            )

            fig.add_trace(trace_actual)
            fig.add_trace(trace_fit)
            fig.add_trace(trace_forecast)

            # Visibility mapping for dropdown
            vis = [False] * (len(df['name']) * 3)
            vis[i * 3:i * 3 + 3] = [True, True, True]

            buttons.append(dict(
                label=name,
                method="update",
                args=[
                    {"visible": vis},
                    {"title": f"{prefix[:-1].capitalize()} Forecast for {name}"}
                ]
            ))

        # Show only the first member by default
        for j in range(len(df["name"]) * 3):
            fig.data[j].visible = j < 3

        fig.update_layout(
            updatemenus=[dict(
                buttons=buttons,
                direction="down",
                x=1.05,
                y=1.15
            )],
            title=f"{prefix[:-1].capitalize()} Forecast",
            xaxis_title="Period",
            yaxis_title=prefix[:-1].capitalize()
        )

        return fig

    def forecast_all(self):
        return [
            self.forecast_plot("warattack_"),
            self.forecast_plot("clancapital_"),
            self.forecast_plot("clangames_"),
            self.forecast_plot("clangamesmaxed_"),
            self.forecast_plot("clanscore_")
        ]
