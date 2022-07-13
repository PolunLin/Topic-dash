import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.graph_objs as go
import pickle
import dash_auth
app = dash.Dash()
# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {
    'flysheet': '0000'
}

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)




with open("data/doctm.pkl",'rb') as f:
    doctm = pickle.load(f)
with open("data/df_1.pkl",'rb') as f:
    top_word = pickle.load(f)

w= 5
F= []
for i in range(30):
    F.append(doctm[i+1][w])

slctid =0
trace1 = go.Bar(
    x = list(range(1,31)),
    y=F,
    name='Topic score'
)


app.layout = html.Div([


html.Div([
    html.H2(children='Topic model  with Dash'),
    dcc.Dropdown(
                    id='docid',
                    options=[{'label': i, 'value': i} for i in doctm.index],
                    placeholder='Search a document id',
                    searchable=True,
                    value=1
                ),
    dcc.Graph(id='topic_doc',figure=go.Figure(data=trace1) 
                            #    layout=go.Layout(barmode='stack')
                            #    )

              )],style={'width': '40%', 'display': 'inline-block',  'float': 'left', 'height':'100%',"textAlign":'left'}),
              

html.Div([dash_table.DataTable(  
    id='view_doc',                    
                    columns=[{'name':i, 'id':i} for i in doctm[['paper']].columns],
                    data=doctm[doctm.index == slctid][['paper']].to_dict('records'),
                    # fixed_rows={ 'headers': True, 'data': 0 },
                    style_table={ 'height':'500px','overflow':'scroll'},
                    style_cell={
        'whiteSpace': 'normal',
        'height': 'auto',
        # 'lineHeight': '15px',
        'width':'55%',
        "textAlign":"left",
        'font_size': '20px',
        "font-family":'Microsoft JhengHei'
    },
                    # page_current=0,
                    # page_size=PAGE_SIZE,
                    )]
, style={'width': '55%', 'display': 'inline-block',  'float': 'right', 'height':'100%',"textAlign":'left','padding-top': '50px',}),

html.Div([dash_table.DataTable(  
    id='topic word',
 columns=[{'name':i, 'id':i} for i in top_word.columns],
                    data=top_word.to_dict('records'),
                    # fixed_rows={ 'headers': True, 'data': 0 },
                    style_table={ 'height':'500px','overflow':'scroll'},
                    style_cell={
        'whiteSpace': 'normal',
        'height': 'auto',
        # 'lineHeight': '15px',
        'width':'55%',
        "textAlign":"left"
    },
    style_cell_conditional=[
        {
            'if': {
                'column_id': 'index',
            },
            'width':'3%'
        }],
                    # page_current=0,
                    # page_size=PAGE_SIZE,
                    )]
, style={'width': '100%', 'display': 'inline-block',  'float': 'left', 'height':'100%',"textAlign":'left','padding-top': '50px',})


])

@app.callback(
    dash.dependencies.Output('topic_doc', 'figure'),
    [dash.dependencies.Input('docid', 'value')]
    )
def update_figure(selected_docid):
    # filtered_df = doctm[doctm.index == selected_docid]
    F= []
    for i in range(30):
        F.append(doctm[i+1][selected_docid])

    trace = []
    trace.append(go.Bar(
    x=list(range(1,31)),
    y=F,
    name='Topic score'
    ))
  
 
    return {'data':trace}
@app.callback(
    dash.dependencies.Output('view_doc', 'data'),
    [dash.dependencies.Input('docid', 'value')
     ])
def update_table(selected_docid):
    data=doctm[doctm.index == selected_docid][['paper']].to_dict('records')
    return data



if __name__ == '__main__':
    app.run_server(debug=False)