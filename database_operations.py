import psycopg2
from psycopg2 import OperationalError

def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        #print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection

def get_data(ubit):
    
    #print("trying to connect to database")
    connection = create_connection(
        "visual_welcome_center", "postgres", "Vincy1005!", "127.0.0.1", "5432"
    )
    #print("connection successfull")
    
    connection.autocommit = True
    cursor = connection.cursor()
    query = "select u.name, v.date_of_visit, v.time_of_visit, u.ubit, u.email from users as u INNER JOIN visits as v ON u.ubit=v.ubit where u.ubit="+ubit+";"
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        #print("Query executed successfully: ",results)
        return results
    except OperationalError as e:
        print(f"The error '{e}' occurred")

def insert_rows(ubit, name, email):
    connection = create_connection(
        "visual_welcome_center", "postgres", "Vincy1005!", "127.0.0.1", "5432"
    )
    connection.autocommit = True
    cursor = connection.cursor()
    results = []
    try:
        results = cursor.execute("select * from users where ubit="+str(ubit)+";")
        if results is not None:
            cursor.execute("update users set name='"+name+"',email='"+email+"' where ubit="+str(ubit)+";")
            cursor.execute("insert into visits values("+str(ubit)+",current_date,current_time);")
        else:
            cursor.execute("insert into users values("+str(ubit)+",'"+name+"','"+email+"');")
            cursor.execute("insert into visits values("+str(ubit)+",current_date,current_time);")
        #print("Query executed successfully")
        print("Data recorded successfully!")
    except OperationalError as e:
        print("")
