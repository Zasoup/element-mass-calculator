#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 10:49:37 2025

@author: zeina
"""

import dash
from dash import html, dcc, Output, Input, State, ctx, callback, ALL
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
from ..Elements import elem

external_stylesheets = [{
    'href': 'https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap',
    'rel': 'stylesheet'
}]

dash.register_page(__name__, path='/',  name='Standard Mode', title='Element Mass Calculator', description='Calculate the individual masses of elements based on percentage composition and total sample mass. Designed for lab efficiency and accuracy.',
    image='picture.png')


colors = {
    'background': '#333333',
    'banner': '#000000',
    'text': '#38c2cf',
    'button1': '#007ea7',
    'button2': '#ffffff',
    'desc': '#8ecae6'    
    
}


periodic_table_layout = [
    ['H', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'He'],
    ['Li', 'Be', '', '', '', '', '', '', '', '', '', '', 'B', 'C', 'N', 'O', 'F', 'Ne'],
    ['Na', 'Mg', '', '', '', '', '', '', '', '', '', '', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar'],
    ['K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr'],
         ['Rb ', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe' ],
         ['Cs', 'Ba', '', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn' ],
         ['Fr', 'Ra', '', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og'],
         ['', '', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', ''],
         ['', '', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', '' ],
]


standardInstructions = """
Enter the total mass in grams, then specify each element's symbol and its corresponding percentage. Use the "+ Add Element" button to include as many elements as needed. When you're finished, click "Calculate" to compute the individual element masses.  
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
        children= standardInstructions,
        style={
            
            'textAlign': 'center',
            'color': colors['desc'],
            'padding-bottom': '12px', 
            'marginLeft': '40px',
            'marginRight': '40px'}
            
        ),

   
html.Div([
    html.Label("Total mass (g):"),
    dcc.Input(id='total-mass', type='number', value=1, step=0.01, style={ 'width': '80px', 'height': '30px'})
], style={
        'textAlign': 'center',
        'color': colors['text'],
        'padding-top': '5px',
        'padding-bottom': '10px'
       
    }),



html.Div(id='std-element-rows', style={'textAlign': 'center'}, children=[
    html.Div([
        dcc.Input(id={'type': 'symbol', 'index': 0}, type='text', placeholder="Symbol", style={'width': '70px', 'height': '30px', 'marginRight': '5px'}),
        dcc.Input(id={'type': 'percent', 'index': 0}, type='number', placeholder="Percent", style={'width': '80px', 'height': '30px'}),
    ])
]),

    html.Div([
        html.Button("+ Add Element", id='add-row-btn', n_clicks=0, style={'padding-top': '5px','padding-bottom': '5px', 'backgroundColor': colors['button2'],'color': colors['button1'], 'height': '35px','textAlign': 'center'}),
        html.Button("Calculate", id='calculate-btn', n_clicks=0, style={'padding-top': '5px','padding-bottom': '5px', 'backgroundColor': colors['button1'],'color': colors['button2'], 'height': '35px','textAlign': 'center'})
        
    ], style={"display": "flex", "justifyContent": "center", "gap": "15px", "marginTop": "20px", 'marginBottom': '20px'}),

html.Div(id='std-result', style={'whiteSpace': 'pre-wrap','marginTop': '20px'}),



])
    


@callback(
    Output('std-element-rows', 'children'),
    Input('add-row-btn', 'n_clicks'),
    State('std-element-rows', 'children'),
)
def add_row(n_clicks, children):
    index = len(children)
    children.append(html.Div([
        dcc.Input(id={'type': 'symbol', 'index': index}, type='text', placeholder="Symbol", style={'width': '70px', 'marginRight': '5px', 'height': '30px'}),
        dcc.Input(id={'type': 'percent', 'index': index}, type='number', placeholder="Percent", style={'width': '80px',  'height': '30px'}),
    ]))
    return children


@callback(
    Output('std-result', 'children'),
    Input('calculate-btn', 'n_clicks'),
    State('total-mass', 'value'),
    State({'type': 'symbol', 'index': dash.ALL}, 'value'),
    State({'type': 'percent', 'index': dash.ALL}, 'value'),
)
def calculate(n_clicks, total_mass, symbols, percents):
    if n_clicks == 0:
        return ""

    total_weighted_sum = 0
    weighted_terms = []
    atomic_masses = []
    percent_values = []
    symbols_used = []
    total_percent = 0
    
    for symbol, percent in zip(symbols, percents):
        if symbol is None or percent is None:
            continue
        found = False
        for e in elem:
            if e.get_symbol().lower() == symbol.strip().lower():
                mass = e.get_mass()
                term = mass * percent
                weighted_terms.append(term)
                atomic_masses.append(mass)
                percent_values.append(percent)
                total_percent+=percent
                symbols_used.append(symbol)
                total_weighted_sum += term
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

    if abs(total_percent-100) > 0.01:
        percentAlerts = html.Div(
            [
                dbc.Alert(
                    (f"Percentages must add up to 100%. Currently: {total_percent:.2f}%"),color="none", 
                    style={"color":"#ff4444",  'padding-bottom': '15px'},
                    is_open=True, 
                    duration=4000)
            ])
        return percentAlerts
            
    result_text = "Final Calculated Masses:\n"
    for i in range(len(symbols_used)):
        mi_pi = weighted_terms[i]
        mass_i = (mi_pi / total_weighted_sum) * total_mass
        result_text += f"{symbols_used[i]}: ({atomic_masses[i]} × {percent_values[i]}) / {total_weighted_sum:.2f} × {total_mass} = {mass_i:.4f} g\n"

    return html.Div(result_text, style={"color": "white", "whiteSpace": "pre-wrap", 'marginLeft': '10px', 'padding-bottom': '15px'})

