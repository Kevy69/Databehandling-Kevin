from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from Load_data import Load_data
from plotly_graphs import Data, General, Finland
from styles import Styles


# Load the dataset and initialize everything
Load_data.load()
Data.initialize()

# initialize dash app
app = Dash(name=__name__, external_stylesheets=[dbc.themes.LUX], suppress_callback_exceptions=True)
server = app.server


# Define layouts for each page
layout_general = html.Div([
        #setting page heading and style
        html.H3( 
            children="General olympic statistics",
            style={"textAlign": "center", "color": "#636EFA"},
        ),
        #Dropdownmeny 
        dcc.Dropdown( 
            id="sports-dropdown",
            value=Data.sports3[0],  # Preselection
            #clearable=False,
            options=[{"label": i, "value": i} for i in Data.sports3],
            style={"width": "75%", "margin": "auto"},
        ),
        
        dcc.Graph(id="sports-graph"),
        # Our sports graph included in the dropdown meny
        dcc.Graph(
            id="age_distribution_3countries",
            figure=General.age_distribution_3sports(),
        ),
        
        dcc.Graph(
            id="height_distribution_3countries",
            figure=General.height_distribution_3sports(),
        ),
        
        dcc.Graph(
            id="weight_distribution_3countries",
            figure=General.weight_distribution_3sports(),
        ),
    ]
)


# Our second page in the side bar with layout and graphs
layout_finland = html.Div(
    [
        html.H3(
            children="Olympic statistics for Finland",
            style={"textAlign": "center", "color": "#636EFA"},
        ),
        
        dcc.Graph(
            id="medal_distribution_sports_finland",
            figure=Finland.medal_distribution_sports_finland(),
        ),
        
        dcc.Graph(
            id="medal_distribution_olympics_finland",
            figure=Finland.medal_distribution_olympics_finland(),
        ),

        dcc.Graph(
            id="age_distribution_olympics_finland",
            figure=Finland.age_distribution_olympics_finland(),
        ),
        
        dcc.Graph(
            id="height_distribution_olympics_finland",
            figure=Finland.height_distribution_olympics_finland(),
        ),
        
        dcc.Graph(
            id="weight_distribution_olympics_finland",
            figure=Finland.weight_distribution_olympics_finland(),
        ),
        
        dcc.Graph(
            id="medal_distribution_finland_players",
            figure=Finland.medal_distribution_finland_players(),
        ),
    ]
)


# define sidebar section of HTML
sidebar = html.Div([
        # html.H2("Drag Race: Plotly Dashboard", className="display-4"),
        html.Img(
            src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Olympic_rings_without_rims.svg/1200px-Olympic_rings_without_rims.svg.png",
            style={'height':'22%'}),
        html.Hr(),
        html.P("Olympic Games stats", className="lead"),
        
        dbc.Nav([
                dbc.NavLink("General", href="/", active="exact"),
                dbc.NavLink("Finland", href="/page-1", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=Styles.sidebar,
)




# Callback function for medal histogram
@app.callback(
    Output(component_id="sports-graph", component_property="figure"),
    Input(component_id="sports-dropdown", component_property="value"),
)
def update_sports_graph(selected_sport):
    return General.medal_distribution_sports(selected_sport)

# Define content section of HTML
content = html.Div(id="page-content", style=Styles.content)

# INDEX LAYOUT
app.layout = html.Div(children=[dcc.Location(id="url"), sidebar, content])

# INDEX CALLBACKS
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def render_page_content(pathname):
    if pathname == "/":
        return layout_general
    elif pathname == "/page-1":
        return layout_finland

    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P("The pathname {pathname} was not recognised..."),
        ]
    )



# Run local server
if __name__ == "__main__":
    app.run_server(port=6969, debug=True)
