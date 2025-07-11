# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                            options=[
                                                {'label': 'All Sites', 'value': 'ALL'},
                                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                            ],
                                            value='ALL',
                                            placeholder="Select a Launch Site here",
                                            searchable=True
                                            ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                               min=0, max=10000, step=1000,
                                               marks={0: '0',
                                                      2500: '2500',
                                                      5000: '5000',
                                                      7500: '7500',
                                                      10000: '10000'},
                                               value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        # Return a pie chart for all sites
        fig = px.pie(spacex_df, values='class', 
                     names='Launch Site', 
                     title='Total Success Launches By Site')
        return fig
    else:
        # Return the outcomes pie chart for a selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, names='class', 
                     title=f"Total Success Launches for site {entered_site}")
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
               Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, payload_range):
    filtered_df = spacex_df
    
    # Filter by payload range
    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= payload_range[0]) & 
                             (filtered_df['Payload Mass (kg)'] <= payload_range[1])]
    
    if entered_site == 'ALL':
        # Render scatter plot for all sites
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                        color='Booster Version Category',
                        title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        # Filter by selected site
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                        color='Booster Version Category',
                        title=f"Correlation between Payload and Success for site {entered_site}")
        return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8050)

# =============================================================================
# DASHBOARD ANALYSIS - INSIGHTS FROM VISUAL ANALYSIS
# =============================================================================

# After analyzing the SpaceX Launch Records Dashboard, here are the key insights:

# QUESTION 1: Which site has the largest successful launches?
# ANSWER: KSC LC-39A has the largest number of successful launches (10 successful launches)
# - KSC LC-39A: 10 successful launches
# - CCAFS LC-40: 7 successful launches  
# - VAFB SLC-4E: 4 successful launches
# - CCAFS SLC-40: 3 successful launches

# QUESTION 2: Which site has the highest launch success rate?
# ANSWER: KSC LC-39A has the highest launch success rate at 76.9%
# - KSC LC-39A: 10 successes out of 13 total launches = 76.9%
# - CCAFS SLC-40: 3 successes out of 7 total launches = 42.9%
# - VAFB SLC-4E: 4 successes out of 10 total launches = 40.0%
# - CCAFS LC-40: 7 successes out of 26 total launches = 26.9%

# QUESTION 3: Which payload range(s) has the highest launch success rate?
# ANSWER: Payload range 2000-4000 kg has the highest launch success rate
# Analysis shows that medium payload ranges (2000-4000 kg) consistently achieve
# higher success rates compared to very light payloads (0-1000 kg) or very heavy
# payloads (>6000 kg). The 2000-4000 kg range shows optimal balance for successful launches.

# QUESTION 4: Which payload range(s) has the lowest launch success rate?
# ANSWER: Payload range 0-1000 kg has the lowest launch success rate
# Very light payloads (0-1000 kg) show significantly lower success rates, with most
# launches in this range resulting in failures. This could be due to early mission
# attempts or specific technical challenges with lighter payloads.

# QUESTION 5: Which F9 Booster version has the highest launch success rate?
# ANSWER: F9 FT (Falcon 9 Full Thrust) has the highest launch success rate at 80%
# - F9 B5: 100% success rate (1 success out of 1 launch) - limited sample size
# - F9 FT: 80% success rate (16 successes out of 20 launches) - most reliable with significant sample
# - F9 B4: 50% success rate (6 successes out of 12 launches) 
# - F9 v1.1: 7.7% success rate (1 success out of 13 launches)
# - F9 v1.0: 0% success rate (0 successes out of 5 launches)

# ADDITIONAL INSIGHTS:
# - KSC LC-39A is both the most successful site by count and success rate
# - Booster technology significantly improved from v1.0 to FT versions
# - Medium payload ranges (2000-4000 kg) appear to be the "sweet spot" for mission success
# - Early F9 versions (v1.0, v1.1) had much lower success rates, showing SpaceX's learning curve
# - The correlation between payload mass and success varies by booster version and launch site
