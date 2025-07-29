#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 21 14:59:16 2025

@author: zeina
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 10:49:37 2025

@author: zeina
"""
import dash
from dash import html, dcc, Output, Input, State, ctx, callback, ALL, callback_context, MATCH
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from ..Elements import elem

dash.register_page(__name__, name='Alternate Mode')
external_stylesheets = [{
    'href': 'https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap',
    'rel': 'stylesheet'
}]



colors = {
    'background': '#333333',
    'banner': '#000000',
    'text': '#38c2cf',
    'button1': '#007ea7',
    'button2': '#ffffff',
    'desc': '#8ecae6'   
    }


reverse_instructions = """
    Enter the element symbol and subscript for each element in the compound.
    Specify the mass of one element, and the calculator will estimate the total mass
    and the individual masses of the remaining elements.
"""



layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children= 'Element Mass Calculator',
        style={
                'backgroundColor': colors['banner'],
                'textAlign': 'center',
                'color': colors['text'],
                'padding-top': '20px',
                'padding-bottom': '15px'
            }
        ),
    html.H2(
        children= reverse_instructions,
        style={
            
            'textAlign': 'center',
            'color': colors['desc'],
            'padding-bottom': '12px', 
            'marginLeft': '40px',
            'marginRight': '40px'}
            
        ),

html.Div([
    
    html.Div([
        html.Label("Known element:"),
        dcc.Input(id='known-symbol', type='text', placeholder="Symbol", style={'width': '70px', 'height': '30px'}),
        dcc.Input(id='known-subscript', type='number', placeholder="Subscript", style={'width': '90px', 'height': '30px'}),
        dcc.Input(id='known-mass', type='number', placeholder="Known Mass", style={'width': '115px', 'height': '30px'}),
        ], style={"display": "flex", "justifyContent": "center", "gap": "5px", "marginTop": "10px"}),
    ], style={
        'textAlign': 'center',
        'color': colors['text'],
        'padding-top': '5px',
        'padding-bottom': '10px'
       
    }),



html.Div(id='alt-element-rows', style={'textAlign': 'center'}, children=[
    html.Div([
        dcc.Input(id={'type': 'symbol', 'index': 0}, type='text', placeholder="Symbol", style={'width': '70px', 'marginRight': '5px', 'height': '30px' }),
        dcc.Input(id={'type': 'subscript', 'index': 0}, type='number', placeholder="Subscript", style={'width': '90px', 'height': '30px'})
    ])
]),

   html.Div([
        html.Button("+ Add Element", id='alt-add-row-btn', n_clicks=0, style={'padding-top': '5px','padding-bottom': '5px', 'backgroundColor': colors['button2'],'color': colors['button1'], 'height': '35px'}),
        html.Button("Calculate", id='alt-calculate-btn', n_clicks=0, style={'backgroundColor': colors['button1'],'color': colors['button2'], 'height': '35px'})
        
    ], style={"display": "flex", "justifyContent": "center", "gap": "15px", "marginTop": "20px", 'marginBottom': '20px'}),

html.Div(id='alt-result', style={'whiteSpace': 'pre-wrap','marginTop': '20px'})

])
    


@callback(
    Output('alt-element-rows', 'children'),
    Input('alt-add-row-btn', 'n_clicks'),
    State('alt-element-rows', 'children'),
)
def add_row(n_clicks, children):
    index = len(children)
    children.append(html.Div([
        dcc.Input(id={'type': 'symbol', 'index': index}, type='text', placeholder="Symbol", style={'width': '70px', 'marginRight': '5px', 'height': '30px'}),
        dcc.Input(id={'type': 'subscript', 'index': index}, type='number', placeholder="Subscript", style={'width': '90px', 'height': '30px'}),
    ]))
    return children


@callback(
    Output('alt-result', 'children'),
    Input('alt-calculate-btn', 'n_clicks'),
    State('known-symbol', 'value'),
    State('known-subscript', 'value'),
    State('known-mass', 'value'),
    State({'type': 'symbol', 'index': dash.ALL}, 'value'),
    State({'type': 'subscript', 'index': dash.ALL}, 'value'),
)
def reverse_calculate(n_clicks, known_symbol, known_subscript, known_mass, symbols, subscripts):
    if n_clicks == 0:
        return ""

    if known_symbol is None or known_mass is None or known_subscript is None:
        blankAlert = html.Div(
            [
                dbc.Alert(
                    ("Please enter the known element's symbol, subscript, and mass."), color="none",
                    style={"color":"#ff4444", 'padding-bottom': '15px'},
                    is_open=True, 
                    duration=4000)
            ])
        return blankAlert
         

    symbols.insert(0, known_symbol)
    subscripts.insert(0, known_subscript)

    atomic_masses = []
    symbols_used = []
    sub_list = []
    
    
    for i, (symbol, sub) in enumerate(zip(symbols, subscripts)):
        if not symbol or sub is None:
            continue
        found = False
        for e in elem:
            if e.get_symbol().lower() == symbol.strip().lower():
                atomic_masses.append(e.get_mass())
                symbols_used.append(symbol)
                sub_list.append(sub)
                found = True
                break
        if not found:
            eAlert = html.Div(
                [
                    dbc.Alert(
                        (f"Element '{symbol}' not found."), color="none",
                        style={"color":"#ff4444", 'padding-bottom': '15px'},
                        is_open=True, 
                        duration=4000)
                ])
            return eAlert

    if not atomic_masses:
        return "No valid element entries found."

    known_mass_val = atomic_masses[0]
    known_mass_per_unit = known_mass_val * known_subscript
    try:
        total_mass = known_mass * sum([m * s for m, s in zip(atomic_masses, sub_list)]) / known_mass_per_unit
    except Exception:
        return "Error in mass calculation. Please check your inputs."

    result_text = f"Estimated Total Mass: {total_mass:.4f} g\n\nCalculated Element Masses:\n"
    for symbol, mass, sub in zip(symbols_used, atomic_masses, sub_list):
        mass_i = (mass * sub / known_mass_per_unit) * known_mass
        result_text += f"{symbol}: {mass_i:.4f} g\n"

    return html.Div(result_text, style={"color": "white", "whiteSpace": "pre-wrap", 'marginLeft': '10px', 'padding-bottom': '15px'})

