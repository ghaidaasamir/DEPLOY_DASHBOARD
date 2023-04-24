import psycopg2
import pandas as pd

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
            print('1')
        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)

        finally:
            # closing database connection.
            print('2')
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

 
