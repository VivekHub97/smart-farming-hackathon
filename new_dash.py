from dash import Dash, html, dcc
import add_map_example as eg
from globals import map_list


def create_page():
    app.layout = html.Div([
    html.H1("Fertilizer and Harvest Maps", style={'text-align': 'center'}),
    # Row for the two maps
    html.Div(map_list)
])

app = Dash(__name__)
# Run the Dash app
if __name__ == "__main__":
    app = Dash(__name__)

    eg.populate_new()
    create_page()

    app.run_server(debug=True)
