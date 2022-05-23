import base64
import datetime
import io
import os
import pandas as pd
from operator import index

# import open_ai

import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table

FONT_AWESOME = (
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"
)

external_stylesheets = [dbc.themes.BOOTSTRAP, FONT_AWESOME]

image_filename = f'{os.getcwd()}/CIMB.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.title = 'Compu-Mundo-Hyper-Mega-Red'

# Main layout
app.layout = html.Div(children=[
    # Buttons layout
    html.Div(children=[
        # Upload Button layout
        html.Div([
            dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Arrastre y Suelte o ',
                html.A('Seleccione Archivo'),
            ]),
            # Style the button and its content
            style={
                'width': '90%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'text-align':'center',
                'margin': '10px'
            },
            # Allow multiple files to be uploaded
            multiple=True
            )
        ],style={'width': '49%', 'display': 'inline-block','text-align':'center'}),
        # Download Button layout
        html.Div([
            html.Button("Descargue Archivo", id="btn-download-txt", 
            # Style the button and its content
            style={
                'width': '90%',
                'height': '60px',
                'text-align':'center',
                'margin': '10px'
            },),
            dcc.Download(id="download-text")
        ],style={'width': '49%', 'display': 'inline-block','text-align':'center'}), 
    # Style the main button layout  
    ],style={'text-align':'center'}),

    # CSV/Excel Table
    html.Div(children=[
        html.Hr(),
        # Table layout
        html.Div(id='output-data-upload', 
        style={
            'width': '80%',
            'margin': '10px',
            'text-align':'center'
            }),
        # Bottom layout
        # CIMB Image
        html.Div([html.Img(
            src='data:image/png;base64,{}'.format(encoded_image.decode()),
            style={
            'width': '15%',
            'margin': '10px'
            }                
        ),
        # Text at the bottom
        html.P('Página desarrollada por los niños chinos del CIMB. Todos los derechos reservados.', 
        style={'font-size':'75%'})
        ], style={'text-align':'center'})
    ,
    ], style={'display': 'inline-block','text-align':'center'}),
    # Initialize the DCC element to store data in web browser
    dcc.Store(id='stored-data'), 
])

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        df = pd.DataFrame({'error':['Error al procesar el archivo']})
        print(e)
        return html.Div([
            'Error al procesar el archivo.'
        ])

    return html.Div([
        html.H5(f'Nombre de archivo : {filename}', style={'text-align':'center'}),
        # html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            df.head(10).to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns]
        ),
        dcc.Store(id='stored-data', data=df.to_dict('data')),

        # For debugging, display the raw contents provided by the web browser
        # html.Div('Raw Content'),
        # html.Pre(contents[0:200] + '...', style={
        #     'whiteSpace': 'pre-wrap',
        #     'wordBreak': 'break-all'
        # })
    ])

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              prevent_initial_call=True,
              suppress_callback_exceptions=True,
)

def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n) for c, n in
            zip(list_of_contents, list_of_names)]
        return children
    
@app.callback(
    Output("download-text", "data"),
    Input("btn-download-txt", "n_clicks"),
    State('stored-data','data'),
    prevent_initial_call=True,
    suppress_callback_exceptions=True,
)

def func(n_clicks, data):
    df = pd.DataFrame(data)
    # Analyze the dataframe

    return dcc.send_data_frame(df.to_excel, "JavierPls.xlsx", sheet_name="Sheet_1", index=False, )

if __name__ == '__main__':
    app.run_server(debug=False)