import pandas as pd               
import plotly.express as px

import dash            
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

#---------------------------------------------------------------

df = pd.read_csv("transect_one_elevations.csv")
df['Date'] = pd.to_datetime(df['Date'])
df = df.groupby(['Date','Well ID'], as_index=False)['Elevation'].mean()
df = df.set_index('Date')
df = df.loc['1/1/2015':'12/25/2019']
df = df.groupby([pd.Grouper(freq="M"),'Well ID'])['Elevation'].mean().reset_index()
print (df[:5])

#---------------------------------------------------------------
app.layout = html.Div([

    html.Div([
        dcc.Graph(id='our_graph')
    ],className='nine columns'),

    html.Div([

        html.Br(),
        html.Label(['Choose 3 Wells to Compare:'],style={'font-weight': 'bold', "text-align": "center"}),
        dcc.Dropdown(id='well_one',
            options=[{'label':x, 'value':x} for x in df.sort_values('Well ID')['Well ID'].unique()],
            value='04T1EL3W',
            multi=False,
            disabled=False,
            clearable=True,
            searchable=True,
            placeholder='Choose a Well...',
            className='form-dropdown',
            style={'width':"90%"},
            persistence='string',
            persistence_type='memory'),

        dcc.Dropdown(id='well_two',
            options=[{'label':x, 'value':x} for x in df.sort_values('Well ID')['Well ID'].unique()],
            value='06T1EL4W',
            multi=False,
            clearable=False,
            persistence='string',
            persistence_type='session'),

        dcc.Dropdown(id='well_three',
            options=[{'label':x, 'value':x} for x in df.sort_values('Well ID')['Well ID'].unique()],
            value='09T1EL5T',
            multi=False,
            clearable=False,
            persistence='string',
            persistence_type='local'),

    ],className='three columns'),

])

#---------------------------------------------------------------

@app.callback(
    Output('our_graph','figure'),
    [Input('well_one','value'),
     Input('well_two','value'),
     Input('well_three','value')]
)

def build_graph(first_well, second_well, third_well):
    dff=df[(df['Well ID']==first_well)|
           (df['Well ID']==second_well)|
           (df['Well ID']==third_well)]
    # print(dff[:5])

    fig = px.line(dff, x="Date", y="Elevation", color='Well ID', height=600)
    fig.update_layout(yaxis={'title':'Water Elevations (m)'},
                      title={'text':'Barataria Preserve Water-levels Transect One',
                      'font':{'size':28},'x':0.5,'xanchor':'center'})
    return fig

#---------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=False)
