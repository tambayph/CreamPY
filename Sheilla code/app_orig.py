import plotly.graph_objects as go
import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import datetime
import os
import flask
from dash.exceptions import PreventUpdate


token = 'pk.eyJ1Ijoic2hlaWxsYTMxNiIsImEiOiJja28ybnE2ancwMHBjMnZteGszNjMwY2wwIn0.u7B_0Y7IZnI3zqXRWvVMUA'
head = ['Lat', 'Lon']
head2 = ['PREV_Lat', 'PREV_Lon']
params = ['CON1_Lat', 'CON1_Lon', 'CON2_Lat', 'CON2_Lon', 'CON3_Lat', 'CON3_Lon']
param_Init = ['INIT_Lat', 'INIT_Lon', 'FINAL_Lat', 'FINAL_Lon']
param_Final = ['Final_lat', 'Final_lon', 'Cat', 'Mxwd', 'Pres', 'Dir', 'Spd']

app = dash.Dash(__name__)

app.layout = html.Div([

    # 1ST ROW. The user inputs the TC's lat and lon
    html.Div(children=[
        html.H5('Initial Position', style={'display': 'inline-block', 'margin-right': 10}),
        dcc.Input(id='lat', type='number', placeholder='latitude', style={'text-align': 'center'}),
        dcc.Input(id='lon', type='number', placeholder='longitude', style={'text-align': 'center'})
    ]),

    # 2ND ROW. The range slider.
    html.Div(children=[
        dcc.RangeSlider(
            id='slider',
            min=0,
            max=120,
            step=12,
            marks={0: '0h', 24: '24h', 48: '48h', 72: '72h', 96: '96h', 120: '120h'},
            value=[0, 120],
            # verticalHeight=100,
            dots=True,
            allowCross=False,
            pushable=12,
            tooltip={'always_visible': False, 'placement': 'bottom'}

        )
    ], style={'display': 'grid', 'grid-template-columns': '70%', 'margin-left': '40vw', 'margin-top': '1vw'}),

    # 3RD ROW
    html.Div(children=[

        # 3rd Row: 1st Column
        html.Div(children=[
            dash_table.DataTable(
                id='initial',
                columns=[
                    {'name': ['', 'Forecast Hour'], 'id': 'Forecast_Hour'},
                    {'name': ['INITIAL', 'Lat'], 'id': 'INIT_Lat'},
                    {'name': ['INITIAL', 'Lon'], 'id': 'INIT_Lon'},
                    {'name': ['FINAL', 'Lat'], 'id': 'FINAL_Lat'},
                    {'name': ['FINAL', 'Lon'], 'id': 'FINAL_Lon'}
                ],

                data=[
                    dict(Forecast_Hour='T+{}'.format(i), **{j: '' for j in param_Init})
                    for i in range(0, 132, 12)

                ],
                style_header={'fontWeight': 'bold', 'textAlign': 'center'},
                style_cell={'width': '80px','fontSize':12, 'font-family':'Arial'},
                merge_duplicate_headers=True,
                fill_width=False,
                editable=True,
                style_data_conditional=[
                    {
                        'if': {'row_index': 'even'},
                        'backgroundColor': 'rgb(240, 240, 240)'
                    }]
            )
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '2vw', 'margin-top': '1vw'}),


        # 3rd Row : 2nd Column
        html.Div(children=[
            dcc.Graph(id='track_map', config={'displayModeBar': False})
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '1vw', 'margin-top': '1vw'}),


        # 3rd Row: 3rd Column
        html.Div(children=[
                dcc.Checklist(
                    id='all-or-none',
                    options=[{'label': 'SELECT ALL', 'value': 'All'}],
                    value=['All'],
                    labelStyle={'display': 'inline-block'},
                ),

                dcc.Checklist(
                id ='checklist',
                options=[
                    {'label': 'CON1', 'value': 'CON1'},
                    {'label': 'CON2', 'value': 'CON2'},
                    {'label': 'CON3', 'value': 'CON3'},
                    {'label': 'INIT', 'value': 'INIT'},
                    {'label': 'FINAL', 'value': 'FINAL'},
                    {'label': 'PREV', 'value': 'PREV'},
                ],
                value=[],
                labelStyle={'display': 'block'}
                )
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '1vw', 'margin-top': '1vw'}),
    ], className='row'),  # end of 3rd Row

    # 4TH ROW
    html.Div(children=[
            html.H6('Raw NWP Guidance', style={'display': 'inline-block', 'margin-right': 340, 'margin-left': 20}),
            html.H6('Interpolated NWP Guidance', style={'display': 'inline-block', 'margin-right': 10}),
    ], className='row', style={'margin-top': '2vw'}),

    # 5TH ROW
    html.Div(children=[

        # 5th Row: 1st Column
        html.Div(id='div1', children=[
            dash_table.DataTable(
                id='raw',
                columns=(
                        [{'name': [' ', 'Forecast Hour'], 'id': 'Forecast_Hour'}] +
                        [{'name': ['CON{}'.format(i), j], 'id': 'CON{}_{}'.format(i, j)} for i in range(1, 4) for j in
                         head]
                ),

                data=[
                    dict(Forecast_Hour='T+{}'.format(i), **{param: '' for param in params})
                    for i in range(0, 132, 12)
                ],

                style_header={'fontWeight': 'bold', 'textAlign': 'center'},
                style_cell={'width': '70px', 'fontSize':12, 'font-family':'Arial'},
                merge_duplicate_headers=True,
                fill_width=False,
                editable=True,
                style_data_conditional=[
                    {
                        'if': {'row_index': 'even'},
                        'backgroundColor': 'rgb(240, 240, 240)'
                    }]
            )
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '1vw'}),

        # 5th Row: 2nd Column
        html.Div(id='div2', children=[
            html.H6('Interpolated NWP Guidance')
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '1vw'}),

        # 6th Row: 3rd Column
        html.Div(children=[
            dash_table.DataTable(
                id='previous',
                columns=[
                    {'name': ['', 'Forecast Hour'], 'id': 'Forecast_Hour'},
                    {'name': ['PREVIOUS FORECAST', 'Lat'], 'id': 'PREV_Lat'},
                    {'name': ['PREVIOUS FORECAST', 'Lon'], 'id': 'PREV_Lon'},
                ],

                data=[
                    dict(Forecast_Hour='T+{}'.format(i), **{j: '' for j in head2})
                    for i in range(0, 132, 12)
                ],

                style_header={'fontWeight': 'bold', 'textAlign': 'center'},
                style_cell={'width': '70px', 'fontSize':12, 'font-family':'Arial'},
                merge_duplicate_headers=True,
                fill_width=False,
                editable=True,
                style_data_conditional=[
                    {
                        'if': {'row_index': 'even'},
                        'backgroundColor': 'rgb(240, 240, 240)'
                    }]
            )
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '1vw'}),

        dcc.Store(id='session', storage_type='session'),
        dcc.Store(id='data2', storage_type='session')
    ], className='row'),  # end of 5th Row

    html.Div(children=[

        html.Div(children=[
            html.Div(children=[
                dcc.Input(id='Category', type='text', placeholder='Category', style={'text-align': 'center'})
            ]),
            html.Div(children=[
                dcc.Input(id='LocalName', type='text', placeholder='Local Name', style={'text-align': 'center'})
            ]),
            html.Div(children=[
                dcc.Input(id='IntName', type='text', placeholder='International Name', style={'text-align': 'center'})
            ]),

            html.Div(children=[
                dcc.Input(id='Time', type='text', placeholder='Time (UTC)', debounce=True, style={'text-align': 'center'})
            ]),

            html.Div(children=[
                html.A(id='download', children='Download File')
            ], style={'margin-top': '1vw'})

        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '1vw', 'margin-top': '6vw'}),

        html.Div(children=[
            html.H6('Analysis and Forecast', style={'display': 'inline-block'}),
            dash_table.DataTable(
                id='FINAL',
                columns=[
                    {'name': 'Forecast Hour', 'id': 'Forecast_Hour'},
                    {'name': 'Lat', 'id': 'Final_lat'},
                    {'name': 'Lon', 'id': 'Final_lon'},
                    {'name': 'Max Wind', 'id': 'Mxwd'},
                    {'name': 'Category', 'id': 'Cat'},
                    {'name': 'Pressure', 'id': 'Pres'},
                    {'name': 'Direction ', 'id': 'Dir'},
                    {'name': 'Speed ', 'id': 'Spd'},

                ],

                data=[
                    dict(Forecast_Hour=i, **{j: '' for j in param_Final})
                    for i in range(0, 132, 12)
                ],
                style_header={'fontWeight': 'bold', 'textAlign': 'center'},
                style_cell={'width': '90px', 'fontSize':13, 'font-family':'Arial'},
                #  merge_duplicate_headers=True,
                fill_width=False,
                editable=True,
                style_data_conditional=[
                    {
                        'if': {'row_index': 'even'},
                        'backgroundColor': 'rgb(240, 240, 240)'
                    }]
            )
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '1vw', 'margin-top': '3vw'})

    ], className='row')  # end of 5th row

])  # end of app layout


# ---------------------------------------------------------------------------------------------------------------
@app.callback(
    Output('session', 'data'),
    Input('raw', 'data'),
    Input('lat', 'value'),
    Input('lon', 'value'))
def store_data(rows, lat, lon):
    df = pd.DataFrame(rows)

    temp = df.drop("Forecast_Hour", axis=1)
    temp = temp.apply(pd.to_numeric, errors='coerce')


    first_row = temp.iloc[[0]].values[0]
    colNames_lat = temp.filter(like='Lat').columns
    colNames_lon = temp.filter(like='Lon').columns
    temp = temp.apply(lambda row: row - first_row, axis=1)

    for c in colNames_lat:
        temp[c] = temp[c] + lat
    for c in colNames_lon:
        temp[c] = temp[c] + lon

    temp = round(temp, 1)
    final = pd.concat([df['Forecast_Hour'], temp], axis=1)

    return final.to_dict('records')


@app.callback(
    Output('div2', 'children'),
    Input('session', 'data'),
    Input('raw', 'columns'))
def adjusted_table(rows, columns):
    df = pd.DataFrame(rows)

    return dash_table.DataTable(
        id='adjusted',
        columns=columns,
        data=df.to_dict('records'),
        style_header={
            'fontWeight': 'bold',
            'textAlign': 'center'
        },
        style_cell={
            'width': '90px',
            'whiteSpace': 'normal', 'fontSize':12, 'font-family':'Arial'
        },
        merge_duplicate_headers=True,
        fill_width=False,
        style_data_conditional=[
            {
                'if': {'row_index': 'even'},
                'backgroundColor': 'rgb(240, 240, 240)'
            }]

    )


@app.callback(
    Output('track_map', 'figure'),
    Input('checklist', 'value'),
    Input('data2', 'data'),
    Input('slider', 'value'))
def update_map(option_chosen, data, sel_hour):
    df = pd.DataFrame(data)

    dff = df[(df['Forecast_Hour'] >= sel_hour[0]) & (df['Forecast_Hour'] <= sel_hour[1])]

    opColor = [['CON1', '#3283FE'], ['CON2', '#a5d854'], ['CON3', 'violet'],
               ['INIT', 'orange'], ['FINAL', 'red'], ['PREV', 'gray']]

    dfCol = pd.DataFrame(data=opColor)

    option = option_chosen

    fig = go.Figure()

    fig.update_geos(lataxis_showgrid=True, lonaxis_showgrid=True)

    fig.add_trace(go.Scattermapbox(
        mode="markers+lines",
        lon=[120, 135, 135, 115, 115, 120, 120],
        lat=[25, 25, 5, 5, 15, 21, 25],
        name='PAR',
        marker={'size': 1, 'color': '#38a6a5'}))

    fig.update_layout(
        mapbox_style="dark",
        width=900,
        height=550,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        showlegend=False,
        mapbox=dict(
            uirevision = True,
            accesstoken=token,
            bearing=0,
            center=go.layout.mapbox.Center(lat=15, lon=130),
            pitch=0,
            zoom=4)
    )

    for option in option:
        option_lat = '{}_Lat'.format(option)
        option_lon = '{}_Lon'.format(option)
        tr = dfCol[dfCol[0] == option].index.values
        tr = np.ndarray.item(tr)
        color = dfCol.iloc[tr][1]
        fig.add_trace(go.Scattermapbox(
            customdata=df['Forecast_Hour'],
            mode="markers+lines",
            lat=dff[option_lat],
            lon=dff[option_lon],
            hovertemplate ='(%{lat:.1f}N,' + '%{lon:.1f}E) ' + '%{customdata}H',
            name=option,
            marker={'size': 8, 'color': color}

        ))

    return fig


################
@app.callback(
    Output("checklist", "value"),
    [Input("all-or-none", "value")],
    [State("checklist", "options")],
)
def select_all_none(all_selected, options):
    all_or_none = []
    all_or_none = [option["value"] for option in options if all_selected]
    return all_or_none


######
@app.callback(
    Output('data2', 'data'),
    Input('session', 'data'),
    Input('initial', 'data'),
    Input('previous', 'data'))
def update_data(adjusted, initial, prev):
    df1 = pd.DataFrame(adjusted)
    df1['Forecast_Hour'] = df1['Forecast_Hour'].str[2:5]
    df1['Forecast_Hour'] = df1['Forecast_Hour'].astype(int)
    df2 = pd.DataFrame(initial)
    df3 = pd.DataFrame(prev)
    df = pd.concat([df1, df2, df3], axis=1)

    df = df.drop("Forecast_Hour", axis=1)
    new_df = pd.concat([df1['Forecast_Hour'], df], axis=1)



    return new_df.to_dict('records')


######-----
@app.callback(
    Output('download', 'href'),
    Input('Category', 'value'),
    Input('LocalName', 'value'),
    Input('IntName', 'value'),
    Input('Time', 'value'),
    Input('FINAL', 'data'))
def downloadFile(Category, LocalName, IntName, Time, final):
    if Time is None:
        raise PreventUpdate

    df = pd.DataFrame(final)
    df['Forecast_Hour'] = df['Forecast_Hour'].apply(lambda x: '{0:0>3}'.format(x))
    df['Final_lat'] = df['Final_lat'].apply(lambda x: '{0:0>4}'.format(x))
    df['Mxwd'] = df['Mxwd'].apply(lambda x: '{0:0>3}'.format(x)) + 'KT'
    df.at[0, 'Pres'] = '{0:0>4}'.format(df.at[0, 'Pres']) + 'HPA'
    df.at[0, 'Spd'] = '{0:0>2}'.format(df.at[0, 'Spd']) + 'KT'

    time = '{:<04}'.format(Time)
    date = datetime.datetime.utcnow().date()
    date1 = date.strftime('%m/%y')
    dateStamp = date.strftime('%y%m%d')

    fileName = LocalName + '_' + dateStamp + Time + '.txt'
    df.to_csv(fileName, header=None, index=None, sep='\t', mode='w+')

    dummy_file = fileName + '.bak'

    with open(fileName, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        write_obj.write(Category + ' ' + LocalName + '/' + IntName + '\n')
        write_obj.write(date1 + ' ' + time + ' ' + '\n' + '\n')
        write_obj.write('ANALYSIS AND FORECAST\n')

        for line in read_obj:
            write_obj.write(line)

    os.remove(fileName)
    os.rename(dummy_file, fileName)

    return '/downloads/{}'.format(fileName)


@app.server.route('/downloads/<path:path>')
def serve_static(path):
    root_dir = os.getcwd()

    return flask.send_from_directory(root_dir, path, as_attachment=True)


###############
@app.callback(
    Output('FINAL', 'data'),
    Input('FINAL', 'data_timestamp'),
    State('FINAL', 'data'))

def update_columns(timestamp, rows):
    TY=['{}'.format(i) for i in range(65,125,5)]
    STY = ['{}'.format(i) for i in range(125, 185, 5)]


    for row in rows:
        if row['Mxwd'] == '25' or row['Mxwd'] == '30':
            row['Cat'] = 'TD'
        elif row['Mxwd'] == '35' or row['Mxwd'] == '40' or row['Mxwd'] == '45':
            row['Cat'] = 'TS'
        elif row['Mxwd'] == '50' or row['Mxwd'] == '55':
            row['Cat'] = 'STS'
        elif row['Mxwd'] == '':
            row['Cat'] = ''


        for x,y in zip(TY,STY):
            if row['Mxwd'] == x:
                row['Cat'] = 'TY'
            elif row['Mxwd'] == y:
                row['Cat'] = 'STY'
    return rows

if __name__ == '__main__':
    app.run_server(debug=True, port=8000)