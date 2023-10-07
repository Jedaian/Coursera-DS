import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px


dir = "/Users/jedai/Desktop/Python/Coursera/Introduction to Data Science/Data Science Capstone project/spacex_launch_dash.csv"
spacex_df = pd.read_csv(dir)
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
mark_payload = {0: '0', 1000: '1000', 2000: '2000', 3000: '3000', 4000: '4000', 5000: '5000',
                6000: '6000', 7000: '7000', 8000: '8000', 9000: '9000', 10000:'10000'}

app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                dcc.Dropdown(id = 'site-dropdown', searchable = True,
                                options = [
                                    {'label': 'All Sites', 'value': 'All site'},
                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                ], value = 'ALL', placeholder = 'Select a Launch Site here'),
                                html.Br(),
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id = 'payload-slider', min = 0, max = 10000,
                                step = 1000, value = [min_payload, max_payload],
                                marks = mark_payload),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

@app.callback(Output(component_id = 'success-pie-chart', component_property = 'figure'),
              Input(component_id = 'site-dropdown', component_property = 'value'))
def get_pie_chart(entered_site):
    if entered_site in ['All site', 'ALL']:
        df_filter = spacex_df.groupby('Launch Site')['class'].value_counts().reset_index(name = 'count')
        fig = px.pie(df_filter[df_filter['class'] == 1], values = 'count', names = 'Launch Site', title = 'Total Success Launches')
        return fig
    else:
        df_filter = spacex_df[spacex_df['Launch Site'] == entered_site]
        class_count = df_filter['class'].value_counts().reset_index()
        class_count.columns = ['class', 'count']
        class_count['class'] = class_count['class'].replace({0: 'Fail', 1: 'Successful'})
        fig = px.pie(class_count, names = 'class', values = 'count', title = f'Total success launches in site {entered_site}')
        return fig


@app.callback(Output(component_id = 'success-payload-scatter-chart', component_property = 'figure'),
              Input(component_id = 'site-dropdown', component_property = 'value'),
              Input(component_id = 'payload-slider', component_property = 'value'))
def get_scatter_chart(entered_site, payload_range):
    min_pay, max_pay = payload_range
    spacex_df['Booster Version Category'] = spacex_df['Booster Version'].str.split().str[0] + " " + spacex_df['Booster Version'].str.split().str[1]
    df_filter = spacex_df[(spacex_df['Payload Mass (kg)'] >= min_pay) & (spacex_df['Payload Mass (kg)'] <= max_pay)]
    if entered_site in ['All site', 'ALL']:
        fig = px.scatter(df_filter, x = 'Payload Mass (kg)', y = 'class', color = 'Booster Version Category',
                         title = 'Correlation between Payload and Success for All Sites', )
        return fig
    else:
        df_filter = df_filter[df_filter['Launch Site'] == entered_site]
        fig = px.scatter(df_filter, x = 'Payload Mass (kg)', y = 'class', color = 'Booster Version Category', 
                         title = f'Correlation between Payload and Success for site {entered_site}')
        return fig

if __name__ == '__main__':
    app.run_server(debug = True)
