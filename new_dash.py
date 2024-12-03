from dash import Dash, html, dcc, Input, Output, no_update
import dash_bootstrap_components as dbc
import add_map_example as eg

from globals import map_list

# Example data for the dropdown
dropdown_options = [
    {"label": "2021", "value": "21"},
    {"label": "2022", "value": "22"},
    {"label": "2023", "value": "23"},
    {"label": "2024", "value": "24"}
]

# Initialize Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Populate the initial map list
eg.populate_new(21)

# Main app layout
app.layout = html.Div(
    [
        html.H1("Fertilizer and Harvest Maps", style={"text-align": "center"}),
        
        # Dropdown section
        dbc.Row(
            [
                dbc.Col(dbc.Label("Select an option", html_for="dropdown"), width=3),
                dbc.Col(
                    dcc.Dropdown(
                        id="map-dropdown",
                        options=dropdown_options,
                        value=None,  # Default value
                        placeholder="Choose a map...",
                    ),
                    width=6,
                ),
            ],
            justify="center",
        ),
        
        # Map rendering area
        html.Div(id="main"),
    ]
)

# Callback to update the map based on dropdown selection
@app.callback(
    Output("main", "children"),  # Update the "main" Div
    Input("map-dropdown", "value"),  # Listen to the dropdown value
)
def update_maps(selected_map):
    if selected_map == "22":
        # Clear and populate the map for fertilizer
        map_list.clear()
        eg.populate_new(22)
        return map_list
    elif selected_map == "23":
        # Clear and populate the map for harvest
        map_list.clear()
        eg.populate_new(23)
        return map_list
    elif selected_map == "24":
        # Clear and populate the map for harvest
        map_list.clear()
        eg.populate_new(24)
        return map_list
    else:
        # Default state (no map selected)
        map_list.clear()
        eg.populate_new(21)
        return map_list

# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
