# Start command for Render deployment: gunicorn Assignment7:server
# Dashboard deployed at: https://render.com/your_dashboard_link (Password: yourpassword)

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

data = [
    {"Year": 1930, "Winner": "Uruguay", "Runner-up": "Argentina"},
    {"Year": 1934, "Winner": "Italy", "Runner-up": "Czechoslovakia"},
    {"Year": 1938, "Winner": "Italy", "Runner-up": "Hungary"},
    {"Year": 1950, "Winner": "Uruguay", "Runner-up": "Brazil"},
    {"Year": 1954, "Winner": "West Germany", "Runner-up": "Hungary"},
    {"Year": 1958, "Winner": "Brazil", "Runner-up": "Sweden"},
    {"Year": 1962, "Winner": "Brazil", "Runner-up": "Czechoslovakia"},
    {"Year": 1966, "Winner": "England", "Runner-up": "West Germany"},
    {"Year": 1970, "Winner": "Brazil", "Runner-up": "Italy"},
    {"Year": 1974, "Winner": "West Germany", "Runner-up": "Netherlands"},
    {"Year": 1978, "Winner": "Argentina", "Runner-up": "Netherlands"},
    {"Year": 1982, "Winner": "Italy", "Runner-up": "West Germany"},
    {"Year": 1986, "Winner": "Argentina", "Runner-up": "West Germany"},
    {"Year": 1990, "Winner": "West Germany", "Runner-up": "Argentina"},
    {"Year": 1994, "Winner": "Brazil", "Runner-up": "Italy"},
    {"Year": 1998, "Winner": "France", "Runner-up": "Brazil"},
    {"Year": 2002, "Winner": "Brazil", "Runner-up": "Germany"},
    {"Year": 2006, "Winner": "Italy", "Runner-up": "France"},
    {"Year": 2010, "Winner": "Spain", "Runner-up": "Netherlands"},
    {"Year": 2014, "Winner": "Germany", "Runner-up": "Argentina"},
    {"Year": 2018, "Winner": "France", "Runner-up": "Croatia"},
    {"Year": 2022, "Winner": "Argentina", "Runner-up": "France"}
]
df = pd.DataFrame(data)

df['Winner'] = df['Winner'].replace({'West Germany': 'Germany'})
df['Runner-up'] = df['Runner-up'].replace({'West Germany': 'Germany'})

iso_mapping = {
    "Uruguay": "URY",
    "Argentina": "ARG",
    "Italy": "ITA",
    "Czechoslovakia": "CZE",
    "Hungary": "HUN",
    "Brazil": "BRA",
    "Sweden": "SWE",
    "England": "GBR",
    "Germany": "DEU",
    "Netherlands": "NLD",
    "France": "FRA",
    "Spain": "ESP",
    "Croatia": "HRV"
}

wins = df['Winner'].value_counts().reset_index()
wins.columns = ['Country', 'Wins']
wins['ISO'] = wins['Country'].map(iso_mapping)

fig = px.choropleth(
    wins,
    locations="ISO",
    color="Wins",
    hover_name="Country",
    color_continuous_scale=px.colors.sequential.Plasma,
    title="FIFA World Cup Wins by Country"
)
fig.update_layout(height=800, width=1000)

app = dash.Dash(__name__)
server = app.server 

app.layout = html.Div([
    html.H1("FIFA World Cup Dashboard"),
    dcc.Graph(id="choropleth", figure=fig),
    html.H2("Countries that have ever won the World Cup"),
    html.Div(
        id="winning-countries",
        children=", ".join(sorted(wins['Country'].tolist()))
    ),
    html.H2("Select a Country to view win count"),
    dcc.Dropdown(
        id="country-dropdown",
        options=[{"label": country, "value": country} for country in sorted(wins['Country'].tolist())],
        placeholder="Select a country"
    ),
    html.Div(id="country-win-count"),
    html.H2("Select a Year to view the Final Match Details"),
    dcc.Dropdown(
        id="year-dropdown",
        options=[{"label": str(year), "value": year} for year in sorted(df['Year'].tolist())],
        placeholder="Select a year"
    ),
    html.Div(id="year-details")
])

@app.callback(
    Output("country-win-count", "children"),
    [Input("country-dropdown", "value")]
)
def update_country_win_count(selected_country):
    if selected_country:
        count = wins.loc[wins["Country"] == selected_country, "Wins"].values[0]
        return f"{selected_country} has won the World Cup {count} times."
    return ""

@app.callback(
    Output("year-details", "children"),
    [Input("year-dropdown", "value")]
)
def update_year_details(selected_year):
    if selected_year:
        row = df.loc[df["Year"] == selected_year].iloc[0]
        return f"In {selected_year}, the winner was {row['Winner']} and the runner-up was {row['Runner-up']}."
    return ""

if __name__ == '__main__':
    app.run(debug=True)
