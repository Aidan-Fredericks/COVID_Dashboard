from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import requests
import plotly.express as px
 
response = requests.get("https://api.covid19api.com/live/country/united-states")
DATA = response.json()
 
fig = px.line(DATA,x="Date",y="Deaths",color="Province",title="Deaths Over Time In Each State")
 
states_list = []
for i in DATA:
    states_list.append(i["Province"])
    
app = Dash(__name__)
 
app.layout = html.Div(children = [
    dcc.Markdown(
        id = "title",
        children = "## COVID Dashboard"
    ),
 
    dcc.Dropdown(
        id = "state_select_dropdown",
        options = states_list,
        value = ["California"],
        multi = True #allows us to select multiple values
    ),
 
    dcc.Graph(
        id = "states_line_graph",
        figure = fig
    )
])
 
@app.callback(
    Output("states_line_graph","figure"),
    Input("state_select_dropdown","value"),
)
def update_states_graph(states_names):
    if states_names == []: #if dropdown menu is empty, creates a blank graph that still has correct labels
        fig = px.line([{"Date":"2021-06-25T00:00:00Z","Deaths":1}],x="Date",y="Deaths",title="Deaths Over Time in Each State")
        return fig
    else:
        records_to_display = []
        for curr_state in DATA:
            if curr_state["Province"] in states_names:
                records_to_display.append(curr_state)
        fig = px.line(records_to_display,x="Date",y="Deaths",color="Province",title="Deaths Over Time in Each State")
        return fig
 
if __name__ == '__main__':
    app.run_server(debug=True)
