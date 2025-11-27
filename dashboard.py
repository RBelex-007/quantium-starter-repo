import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import glob
import os

data_files = glob.glob('data/daily_sales_data_*.csv')
dfs = [pd.read_csv(file) for file in data_files]
df = pd.concat(dfs, ignore_index=True)

df['date'] = pd.to_datetime(df['date'])
df['price'] = df['price'].str.replace('$', '').astype(float)
df['sales'] = df['price'] * df['quantity']

pinkm_df = df[df['product'] == 'pink morsel'].copy()
pinkm_df_sub = pinkm_df[['sales', 'date', 'region']]

# Create directory if it doesn't exist
os.makedirs('data/processed', exist_ok=True)
pinkm_df_sub.to_csv('data/processed/pinkm_sales_data.csv', index=False)

app = dash.Dash(__name__)

# simple button styles
DEFAULT_BTN_STYLE = {
    'margin': '4px',
    'padding': '8px 12px',
    'border': '1px solid #ccc',
    'backgroundColor': '#fff',
    'cursor': 'pointer'
}
ACTIVE_BTN_STYLE = {
    **DEFAULT_BTN_STYLE,
    'backgroundColor': '#2c7be5',
    'color': 'white',
    'border': '1px solid #1a5fb4'
}

app.layout = html.Div(
    className='container',
    children=[
        html.H1("Pink Morsel Sales Dashboard", className='header'),
        html.Div(id='selection-label', style={'marginBottom': '8px'}),
        html.Div(
            className='card',
            children=[
                html.Div([
                    html.Button("All", id='btn-all', n_clicks=0, style=DEFAULT_BTN_STYLE),
                    html.Button("North", id='btn-north', n_clicks=0, style=DEFAULT_BTN_STYLE),
                    html.Button("East", id='btn-east', n_clicks=0, style=DEFAULT_BTN_STYLE),
                    html.Button("South", id='btn-south', n_clicks=0, style=DEFAULT_BTN_STYLE),
                    html.Button("West", id='btn-west', n_clicks=0, style=DEFAULT_BTN_STYLE),
                ], style={'marginBottom': '12px'}),
                dcc.Graph(id='sales-graph')
            ]
        )
    ]
)

# single callback handles which button was clicked and updates graph + button styles + label
@app.callback(
    Output('sales-graph', 'figure'),
    Output('selection-label', 'children'),
    Output('btn-all', 'style'),
    Output('btn-north', 'style'),
    Output('btn-east', 'style'),
    Output('btn-south', 'style'),
    Output('btn-west', 'style'),
    Input('btn-all', 'n_clicks'),
    Input('btn-north', 'n_clicks'),
    Input('btn-east', 'n_clicks'),
    Input('btn-south', 'n_clicks'),
    Input('btn-west', 'n_clicks'),
)
def update_chart(n_all, n_north, n_east, n_south, n_west):
    # determine which button triggered the callback
    ctx = dash.callback_context
    if not ctx.triggered:
        selected = 'All'
    else:
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
        mapping = {
            'btn-all': 'All',
            'btn-north': 'north',
            'btn-east': 'east',
            'btn-south': 'south',
            'btn-west': 'west'
        }
        selected = mapping.get(triggered_id, 'All')

    # build figure
    if selected == 'All':
        sales = pinkm_df.groupby(['date', 'region'])['sales'].sum().reset_index()
        fig = px.line(sales.sort_values('date'), x='date', y='sales', color='region',
                      title='Pink Morsel Sales by Date — All Regions')
    else:
        sales = (pinkm_df[pinkm_df['region'] == selected]
                 .groupby('date')['sales'].sum().reset_index()
                 .sort_values('date'))
        fig = px.line(sales, x='date', y='sales',
                      title=f'Pink Morsel Sales by Date — {selected.capitalize()}')

    # prepare label and button styles
    label = f"Showing: {selected.capitalize()}"
    styles = {
        'All': ACTIVE_BTN_STYLE if selected == 'All' else DEFAULT_BTN_STYLE,
        'north': ACTIVE_BTN_STYLE if selected == 'north' else DEFAULT_BTN_STYLE,
        'east': ACTIVE_BTN_STYLE if selected == 'east' else DEFAULT_BTN_STYLE,
        'south': ACTIVE_BTN_STYLE if selected == 'south' else DEFAULT_BTN_STYLE,
        'west': ACTIVE_BTN_STYLE if selected == 'west' else DEFAULT_BTN_STYLE,
    }

    return fig, label, styles['All'], styles['north'], styles['east'], styles['south'], styles['west']

if __name__ == '__main__':
    app.run(debug=True)