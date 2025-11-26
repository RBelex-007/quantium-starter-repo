import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import glob

data_files = glob.glob('data/daily_sales_data_*.csv')
dfs = [pd.read_csv(file) for file in data_files]
df = pd.concat(dfs, ignore_index=True)

df['date'] = pd.to_datetime(df['date'])
df['price'] = df['price'].str.replace('$', '').astype(float)
df['sales'] = df['price']*df['quantity']

pinkm_df = df[df['product'] == 'pink morsel'].copy()

app = dash.Dash(__name__)

app.layout = html.Div([ 
    html.H1("Pink Morsel Sales Dashboard"),

    html.Div([
        html.Div([
            dcc.Graph(id='sales-by-date'),
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Graph(id='sales-by-region'),
        ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'}),
    ])
])

@app.callback(
    Output('sales-by-date', 'figure'),
    Input('sales-by-date', 'id')  # Dummy input to trigger the callback
)

def update_sales_by_date(_):
    sales_by_date = pinkm_df.groupby('date')['sales'].sum().reset_index()
    fig = px.line(sales_by_date, x='date', y='sales', title='Total Sales of Pink Morsel Over Time')
    return fig

@app.callback(
    Output('sales-by-region', 'figure'),
    Input('sales-by-region', 'id')
)

def update_sales_by_region(_):
    sales_by_region = pinkm_df.groupby('region')['sales'].sum().reset_index()
    fig = px.bar(sales_by_region, x='region', y='sales', title='Total Sales of Pink Morsel by region')
    return fig

if __name__ == '__main__':
    app.run(debug=True)# Dash app to visualize Pink Morsel sales data