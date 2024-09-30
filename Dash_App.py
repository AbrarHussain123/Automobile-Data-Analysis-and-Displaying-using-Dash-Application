import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import plotly.express as px
URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"
data = pd.read_csv(URL)
print('Data downloaded and read into a dataframe!')
from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd

app = Dash(__name__)


app.layout = html.Div([

    
    html.H1(
        children='Automobile Sales Statistics Dashboard', 
        style={'color': '#503D36', 'fontSize': 24, 'textAlign': 'center'}
    ),

    
    dcc.Dropdown(
        id='dropdown-statistics', 
        options=[
            {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
            {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
        ],
        placeholder='Select a report type',
        value='Select Statistics',   
        style={
            'width': '80%',
            'padding': '3px',
            'fontSize': '20px',
            'textAlignLast': 'center'
        }
    ),

    
    dcc.Dropdown(
        id='select-year',
        value='select-year', 
        options=[{'label': i, 'value': i} for i in range(1980, 2024)],
        placeholder='Select a year',
        style={
            'width': '80%',
            'padding': '3px',
            'fontSize': '20px',
            'textAlignLast': 'center'
        }
    ),

    
    html.Div(id='output-container', className='chart-grid', style={'display': 'flex'})
])

@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics',component_property='value'))

def update_input_container(selected_statistics):
    if selected_statistics =='Yearly Statistics': 
        return False
    else: 
        return True
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'), Input(component_id='select-year', component_property='value')])

def update_output_container(selected_statistics, input_year):
    R_chart1 = None
    R_chart2 = None
    R_chart3 = None
    R_chart4 = None

    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]
        
        # Plot 1: Automobile sales fluctuate over Recession Period (year-wise) using line chart
        # Grouping data for plotting
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        # Plotting the line graph
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, 
                           x='Year',
                           y='Automobile_Sales',
                           title="Automobile Sales over Recession")
        )

        # Plot 2: Calculate the average number of vehicles sold by vehicle type and represent as a Bar chart
        # Use groupby to create relevant data for plotting
        average_sales = recession_data.groupby(['Recession', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(average_sales,
                          x='Vehicle_Type',
                          y='Automobile_Sales',
                          title="Vehicle Type Sales During Recession")
        )

        # Plot 3: Pie chart for total expenditure share by vehicle type during recessions
        # Grouping data for plotting
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec,
                           values=exp_rec.values,
                           names=exp_rec.index,
                           title='Total Vehicle Expenditure for Each Vehicle Type During Recession')
        )

        # Plot 4: Develop a Bar chart for the effect of unemployment rate on vehicle type and sales
        # Grouping data for plotting
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(unemp_data,
                          x='unemployment_rate',
                          y='Automobile_Sales',
                          color='Vehicle_Type',
                          labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
                          title='Effect of Unemployment Rate on Vehicle Type and Sales')
        )

        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1), html.Div(children=R_chart2)], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3), html.Div(children=R_chart4)], style={'display': 'flex'})
        ]

    elif (input_year and selected_statistics == 'Yearly Statistics'):
        yearly_data = data[data['Year'] == input_year]

        # Plot 1: Yearly Automobile sales using line chart for the whole period.
        # Grouping data for plotting
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yas,
                           x='Year',
                           y='Automobile_Sales',
                           title='Yearly Automobile Sales')
        )

        # Plot 2: Total Monthly Automobile sales using line chart.
        # Grouping data for plotting
        mas = data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(mas,
                           x='Month',
                           y='Automobile_Sales',
                           title='Total Monthly Automobile Sales')
        )

        # Plot 3: Bar chart for average number of vehicles sold during the given year
        # Grouping data for plotting
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(avr_vdata,
                          x='Vehicle_Type',
                          y='Automobile_Sales',
                          title='Average Vehicles Sold by Vehicle Type in the Year {}'.format(input_year))
        )

        # Plot 4: Total Advertisement Expenditure for each vehicle using pie chart
        # Grouping data for plotting
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum()
        Y_chart4 = dcc.Graph(
            figure=px.pie(exp_data,
                           values=exp_data.values,
                           names=exp_data.index,
                           title='Total Advertisement Expenditure for Each Vehicle')
        )

        return [
            html.Div(className='chart-item', children=[html.Div(children=Y_chart1), html.Div(children=Y_chart2)], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=Y_chart3), html.Div(children=Y_chart4)], style={'display': 'flex'})
        ]

    # If no valid statistics are selected or input year is not valid
    return []


     
        
# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
