import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

LATEST_MONTH = "NOV_2025"

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
