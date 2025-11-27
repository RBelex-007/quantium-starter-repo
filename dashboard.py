import pandas as pd
import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import glob
import os

data_files = glob.glob('data/daily_sales_data_*.csv')
dfs = [pd.read_csv(file) for file in data_files]
df = pd.concat(dfs, ignore_index=True)

df['date'] = pd.to_datetime(df['date'])
df['price'] = df['price'].str.replace('$', '').astype(float)
df['sales'] = df['price']*df['quantity']

pinkm_df = df[df['product'] == 'pink morsel'].copy()
pinkm_df_sub = pinkm_df[['sales', 'date', 'region']]

# Create directory if it doesn't exist
os.makedirs('data/processed', exist_ok=True)
pinkm_df_sub.to_csv('data/processed/pinkm_sales_data.csv', index=False)

app = dash.Dash(__name__)

app.layout = html.Div(
    className='container',
    children=[
        html.H1("Pink Morsel Sales Dashboard", className='header'),
        html.Div(id='view-label', style={'marginBottom': '8px'}),
        html.Div(
            className='card',
            children=[
                html.Button("Switch view", id='toggle-button', n_clicks=0),
                dcc.Store(id='view-store', data='date'),
                dcc.Graph(id='sales-graph')
            ]
        )
    ]
)

# toggle the view state when button clicked
@app.callback(
    Output('view-store', 'data'),
    Input('toggle-button', 'n_clicks'),
    State('view-store', 'data'),
    prevent_initial_call=False
)
def toggle_view(n_clicks, current_view):
    # start with 'date' (default). Each click switches view.
    if n_clicks is None:
        return current_view
    return 'region' if current_view == 'date' else 'date'

# update graph based on current view
@app.callback(
    Output('sales-graph', 'figure'),
    Output('view-label', 'children'),
    Input('view-store', 'data')
)
def update_graph_and_label(view):
    if view == 'date':
        sales_by_date = pinkm_df.groupby('date')['sales'].sum().reset_index()
        fig = px.line(sales_by_date, x='date', y='sales', title='Total Sales of Pink Morsel Over Time')
        label = "Currently showing: Sales by Date"
    else:
        sales_by_region = pinkm_df.groupby('region')['sales'].sum().reset_index()
        fig = px.bar(sales_by_region, x='region', y='sales', title='Total Sales of Pink Morsel by Region')
        label = "Currently showing: Sales by Region"
    return fig, label

if __name__ == '__main__':
    app.run(debug=True)