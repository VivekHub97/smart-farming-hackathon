from dash import Dash, html, dcc

map_list = []



def add_map(map):
    map_list.append(html.Div([dcc.Graph(figure=map)], style={'width': '48%', 'display': 'inline-block'}))