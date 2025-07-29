#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 10:21:55 2025

@author: zeina
"""

import dash
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc


external_stylesheets = [{
    'href': 'https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap',
    'rel': 'stylesheet'}]

app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Element Mass Calculator</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: 'Inter', sans-serif;
                margin: 0;
                background-color: #f7f7f7;
                padding: 40px;
            }
            .container {
                max-width: 1000px;
                min-height: 90vh;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 0 20px rgba(0,0,0,0.05);
            }
            h1 {
                font-size: 2em;
                font-weight: 800;
                margin-bottom: 10px;
            }
            h2 {
                font-size: 14px;
                font-weight: 400;
                
                }
            label, input {
                font-size: 1rem;
                margin-bottom: 10px;
            }
            .row {
                display: flex;
                gap: 10px;
                margin-bottom: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            {%app_entry%}
        </div>
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>



'''



sidebar = dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.Div(page["name"], className="ms-2"),
                    ],
                    href=page["path"],
                    active="exact",
                )
                for page in dash.page_registry.values()
            ],
            vertical=False,
            pills=True,
            fill=True,
            className="bg-black",
)


app.layout= html.Div([
    html.Div([
        html.Div(
            sidebar
            )
        ]),
        dash.page_container
    ])



if __name__ == "__main__":
    app.run(debug=False)