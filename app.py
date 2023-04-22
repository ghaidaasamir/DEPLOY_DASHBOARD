import psycopg2
import pandas as pd
from dash import Dash, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import dash
import importlib
from dash.dependencies import Output, Input
from dash import dcc
from dash import html
#SamaWrapper = importlib.import_module('annotation.05_code.wrapper.sama_aws_wrapper.SamaWrapper')

class Postgresql():

    def __init__(self,user="postgres",password="ghaidaa",host="127.0.0.1",port="5432",database="postgres"):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database

    def create_table(self):
        try:
            connection = psycopg2.connect(user=self.user,
                                        password=self.password,
                                        host=self.host,
                                        port=self.port,
                                        database=self.database)
            cursor = connection.cursor() 
            """ create tables in the PostgreSQL database"""
            create_table = (
                """
                CREATE TABLE Dashboard (
                    Project_ID CHAR(30),
                    Task_ID CHAR(40),
                    ROS_BagName CHAR(50),
                    Status CHAR(30),
                    Status_on_Sama CHAR(30),
                    Manual_Annotator CHAR(30),
                    Reviewer CHAR(30),
                    Created_at CHAR(40), 
                    Priority CHAR(30)
                )
                """)
            cursor.execute(create_table)
            connection.commit()

        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into Dashboard table", error)

        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

   
    def insert_into_table(self, table_db):
        try:
            connection = psycopg2.connect(user=self.user,
                                        password=self.password,
                                        host=self.host,
                                        port=self.port,
                                        database=self.database)
            cursor = connection.cursor() 
            postgres_insert_query = """ INSERT INTO Dashboard (Project_ID, Task_ID, ROS_BagName, Status, Status_on_Sama, Manual_Annotator, Reviewer, Created_at, Priority) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            records = []
            for task in table_db:
                Task_ID = list(task.keys())[0]
                Project_ID = task[Task_ID]['project_id']
                Project_ID = project_ids_to_names[Project_ID]
                ROS_BagName = task[Task_ID]['rosbag']
                Status = task[Task_ID]['state']
                Status_on_Sama = task[Task_ID]['state']
                Manual_Annotator = 'Ghaidaa'
                Reviewer = 'Ghaidaa'
                Created_at = task[Task_ID]['created_at']
                Priority = task[Task_ID]['priority']
                record_to_insert = (Project_ID, Task_ID, ROS_BagName, Status, Status_on_Sama, Manual_Annotator, Reviewer, Created_at, Priority)
                records.append(record_to_insert)
                
            result = cursor.executemany(postgres_insert_query, records)
            connection.commit()
            print("Records inserted successfully into table")

        except (Exception, psycopg2.Error) as error:
            print("Failed to insert records into Dashboard table", error)

        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

    def update_table(self,new_values):
        try:
            connection = psycopg2.connect(user=self.user,
                                        password=self.password,
                                        host=self.host,
                                        port=self.port,
                                        database=self.database)

            cursor = connection.cursor()

            print("Table Before updating record ")
            sql_select_query = """select * from Dashboard"""
            cursor.execute(sql_select_query, (0,))
            record = cursor.fetchone()
            print(record)

            for k, v in new_values.items():
                # Update single record now
                sql_update_query = ("Update Dashboard "
                    f"set {k} "
                    f" = {v}")
                cursor.execute(sql_update_query)
                connection.commit()
                count = cursor.rowcount
                print(count, "Record Updated successfully ")

            print("Table After updating record ")
            sql_select_query = """select * from Dashboard"""
            cursor.execute(sql_select_query, (0,))
            record = cursor.fetchone()
            print(record)

        except (Exception, psycopg2.Error) as error:
            print("Error in update operation", error)

        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

    def read_from_table(self, column_names):

        try:
            connection = psycopg2.connect(user=self.user,
                                        password=self.password,
                                        host=self.host,
                                        port=self.port,
                                        database=self.database)
            cursor = connection.cursor()
            postgreSQL_select_Query = "select * from Dashboard"

            cursor.execute(postgreSQL_select_Query)
            print("Selecting rows from Dashboard table using cursor.fetchall")
            pipeline_records = cursor.fetchall()
            # Now we need to transform the list into a pandas DataFrame:
            df = pd.DataFrame(pipeline_records, columns=column_names)
            cursor.close()
        
        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)

        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
                return df
    def delete_table(self):   
        
        conn = psycopg2.connect(user=self.user,
                                        password=self.password,
                                        host=self.host,
                                        port=self.port,
                                        database=self.database)
        # Creating a cursor object using the cursor()
        # method
        cursor = conn.cursor()

        # drop table accounts
        sql = '''DROP TABLE IF EXISTS Dashboard '''

        # Executing the query
        cursor.execute(sql)

        print("Table dropped !")
        # Commit your changes in the database
        conn.commit()

        # Closing the connection
        conn.close()
 

def show_table(update_db):
    #sama_wrapper = SamaWrapper()
    number_of_tasks = 3
    projects_names = ["Brightskies CFT1 AMPS TPF", #"Brightskies CFT1 AMPS RMF", "Brightskies CFT1 AMPS RMF - clone", "Brightskies CFT1 AMPS RMF_Scenario", "Brightskies CFT1 AMPS ENV", 
    "Brightskies CFT1 AMPS TCIS", "Brightskies CFT1 AMPS TCIL", "Brightskies CFT1 AMPS SEF"]
#     if update_db == True:
#         ex1.delete_table()
#         ex1.create_table()
#         for project_name in projects_names:
#             print(project_name)
#             table_db = sama_wrapper.get_tasks_status(project_name, number_of_tasks)
#             ex1.insert_into_table(table_db)
#         ex1.update_table({'Status':'in progress'})
    df = ex1.read_from_table(column_names)
    df_obj = df.select_dtypes(['object'])
    df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
    columns = []
    dropdown = {}
    for name in column_names:
        columns.append({'id': name, 'name': name, 'presentation': 'dropdown'})
        dropdown[name] = {}
        values = df[name].unique()
        df_project = df['Project_ID'].unique()
        dropdown[name]['options'] = [{'label': i, 'value': i}
                        for i in values]
    return df, columns, dropdown


if __name__ == '__main__':

    ex1 = Postgresql(user="postgres",password="ghaidaa",host="127.0.0.1",port="5432",database="postgres")
    column_names = ['Project_ID','Task_ID','ROS_BagName', 'Status', 'Status_on_Sama', 'Manual_Annotator','Reviewer', 'Created_at','Priority']
    project_ids_to_names = {
                              10944:"Brightskies CFT1 AMPS TPF",
                              13207:"Brightskies CFT1 AMPS RMF",
                              13724:"Brightskies CFT1 AMPS RMF - clone",
                              13368:"Brightskies CFT1 AMPS RMF_Scenario",
                              13370:"Brightskies CFT1 AMPS ENV",
                              13209:"Brightskies CFT1 AMPS TCIS",
                              13212:"Brightskies CFT1 AMPS TCIL",
                              14407:"Brightskies CFT1 AMPS SEF"
                            }

    dropdown_projects = ["Brightskies CFT1 AMPS TPF", #"Brightskies CFT1 AMPS RMF", "Brightskies CFT1 AMPS RMF - clone", "Brightskies CFT1 AMPS RMF_Scenario", "Brightskies CFT1 AMPS ENV", 
    "Brightskies CFT1 AMPS TCIS", "Brightskies CFT1 AMPS TCIL", "Brightskies CFT1 AMPS SEF"]
    update_db = False
    df, columns, dropdown = show_table(update_db)
    dropdown_Task_IDs = df['Task_ID'].unique()


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

    app.run_server(debug=True)
    #app.run_server(debug=True, port=8086, use_reloader=False)
