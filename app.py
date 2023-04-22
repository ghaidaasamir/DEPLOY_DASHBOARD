from dash import Input, Output, dash_table, dcc, html
import dash
import dash_bootstrap_components as dbc
#import importlib
from dash.dependencies import Output, Input
#SamaWrapper = importlib.import_module('annotation.05_code.wrapper.sama_aws_wrapper.SamaWrapper')
from postgresql import Postgresql

def show_table(update_db, ex1):
    #sama_wrapper = SamaWrapper()
    column_names = ['Project_ID','Task_ID','ROS_BagName', 'Status', 'Status_on_Sama', 'Manual_Annotator','Reviewer', 'Created_at','Priority']
    df = ex1.read_from_table(column_names)
    df_obj = df.select_dtypes(['object'])
    df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
    columns = []
    dropdown = {}
    for name in column_names:
        columns.append({'id': name, 'name': name, 'presentation': 'dropdown'})
        dropdown[name] = {}
        values = df[name].unique()
        dropdown[name]['options'] = [{'label': i, 'value': i}
                        for i in values]
    return df, columns, dropdown

def start_app():
    
    ex1 = Postgresql(user="postgres",password="ghaidaa",host="127.0.0.1",port="5432",database="postgres")
    update_db = False
    df, columns, dropdown = show_table(update_db, ex1)
    dropdown_Task_IDs = df['Task_ID'].unique()
    dropdown_projects = ["Brightskies CFT1 AMPS TPF", #"Brightskies CFT1 AMPS RMF", "Brightskies CFT1 AMPS RMF - clone", "Brightskies CFT1 AMPS RMF_Scenario", "Brightskies CFT1 AMPS ENV", 
    "Brightskies CFT1 AMPS TCIS", "Brightskies CFT1 AMPS TCIL", "Brightskies CFT1 AMPS SEF"]
    return dropdown_Task_IDs, df, columns, dropdown, dropdown_projects

dropdown_Task_IDs, df, columns, dropdown, dropdown_projects = start_app()
    
app = dash.Dash(__name__)

server = app.server

app.scripts.config.serve_locally = True

app.config['suppress_callback_exceptions'] = True

html.Img(src="dog.jpeg", style ={"height": "50px", "width": "50px", 'float':'left'})
dbc.Row(
        [
            dbc.Col(html.Div(html.P(' '))),
            html.H1('test 1')
        ]),


controls = [
        dbc.Row([dbc.Col([
                dbc.Label("Project ID",style={'font-size': '24px'},color='dark'),
                html.Div([dcc.Dropdown(dropdown_projects, 'Brightskies CFT1 AMPS TCIS', id='project-dropdown'
                ,style={
                'backgroundColor': '#f2f2f2',
                'color': '#333333',
                'fontFamily': 'Arial',
                'fontSize': '16px',
                'border': '1px solid #cccccc',
                'borderRadius': '5px',
                'boxShadow': '2px 2px 5px #888888',
                'width': '400px'}),]),
                html.Br(),
                html.Div([dcc.Dropdown(['ENTER TASK ID','SHOW ALL TASKS'], 'SHOW ALL TASKS', id='options-dropdown',style={
                'backgroundColor': '#f2f2f2',
                'color': '#333333',
                'fontFamily': 'Arial',
                'fontSize': '16px',
                'border': '1px solid #cccccc',
                'borderRadius': '5px',
                'boxShadow': '2px 2px 5px #888888',
                'width': '400px'}
                ),]),
                ])
                ]),
        dbc.Row([
            html.Div(
            [
                html.Br(),
                dbc.Label("TASK ID",style={'font-size': '24px'},color='dark'),
                html.Br(),
                dcc.Dropdown(dropdown_Task_IDs, id='input1', style=
                #dcc.Input(id="input1", type="text", placeholder="", style=
                {'backgroundColor': '#f2f2f2',
                'color': '#333333',
                'fontFamily': 'Arial',
                'fontSize': '16px',
                'border': '1px solid #cccccc',
                'borderRadius': '5px',
                'boxShadow': '2px 2px 5px #888888',
                'width': '400px'}),
            ]
            )
        ]),
        dbc.Row([html.Div(id='container')]),
        dbc.Row([#dbc.Col(dbc.Label("Table",style={'font-size': '24px'},color='primary'),),
                html.Br(),
                html.Div(id='dd-output')]),
        dbc.Row([#dbc.Col(dbc.Label("Table",style={'font-size': '24px'},color='primary'),),
                html.Br(),
                html.Div(id='dd-output2')])
    ]

app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        html.H1("SAMA PIPELINE"),
        html.Hr(),
        html.Div(controls)

    ])

@app.callback(
    Output('dd-output', 'children'),
    Input('project-dropdown', 'value'),
    Input("options-dropdown", "value"),
    Input("input1", "value"))

def display_output(project_name, options, task_id):
    print(project_name, options, task_id)
    df_project = df.loc[df['Project_ID'] == project_name]
    if options == 'SHOW ALL TASKS':
        return html.Div([
                    dash_table.DataTable(
                    id='table-dropdown1',
                    data=df_project.to_dict('records'),
                    columns=columns,
                    style_cell={
                        'fontSize': '16px',
                        'color': '#1f77b4',
                        'textAlign': 'left',
                    },
                    style_header={
                        'backgroundColor': '#f2f2f2',
                        'fontWeight': 'bold'
                    },
                    style_table={
                        'border': '1px solid #ccc',
                        'margin': '20px'
                    },
                    
                    # Enable row selection
                    row_selectable='multi',
                    selected_rows=[],
                    editable=True,
                    dropdown=dropdown
                    ),
                    html.Div(id='table-dropdown-container')
                ])
    else:
        if task_id in df['Task_ID'].values:
            df_task = df.loc[df['Task_ID'] == task_id]
            return html.Div([
                        dash_table.DataTable(
                        id='table-dropdown2',
                        data=df_task.to_dict('records'),
                        columns=columns,
                        style_cell={
                            'fontSize': '16px',
                            'color': '#1f77b4',
                            'textAlign': 'left'
                        },
                        style_header={
                            'backgroundColor': '#f2f2f2',
                            'fontWeight': 'bold'
                        },
                        style_table={
                            'border': '1px solid #ccc',
                            'margin': '20px'
                        },
                        editable=True,
                        dropdown=dropdown
                        ),
                        html.Div(id='table-dropdown-container')
                    ])

# Define the callback
@app.callback(
    Output('dd-output2', 'children'),
    [Input('table-dropdown1', 'selected_rows')]
)
def update_figure(selected_rows):
    if not selected_rows:
        # Return an empty figure if no rows are selected
        return {}

    # Otherwise, create a figure based on the selected row
    rows = df.iloc[selected_rows].to_dict('records')
    return html.Div([
                    dash_table.DataTable(
                    id='table-dropdown3',
                    data=rows,
                    columns=columns,
                    style_cell={
                        'fontSize': '16px',
                        'color': '#1f77b4',
                        'textAlign': 'left'
                    },
                    style_header={
                        'backgroundColor': '#f2f2f2',
                        'fontWeight': 'bold'
                    },
                    style_table={
                        'border': '1px solid #ccc',
                        'margin': '20px',
                    },
                    editable=True,
                    dropdown=dropdown
                    )
                ])

if __name__ == '__main__':

    app.run_server(debug=True)
    #app.run_server(debug=True, port=8086, use_reloader=False)