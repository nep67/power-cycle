import sqlite3
from datetime import *

# create connection
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return None


# create user
def create_user(conn, user):
    sql = ''' INSERT INTO user(email, fname, lname, age, height, weight, gender, category, birth)
              VALUES(?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    return cur.lastrowid

# update user
def update_user(conn, user):
    sql = ''' UPDATE user 
              SET fname = ?, lname = ?, age = ?, height = ?, weight = ?, gender = ?, category = ?, birth = ?
              WHERE email = ? '''
    cur = conn.cursor()
    cur.execute(sql, user)
    return cur.lastrowid

# create textfile
def create_textfile(conn, textfile):
    sql = ''' INSERT INTO  text(user_email, name, path, date)
              VAlUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, textfile)
    return cur.lastrowid


# create calibration_file
def create_calibrate(conn, spreadsheet):
    sql = ''' INSERT INTO  calibration(name,path,date)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, spreadsheet)
    return cur.lastrowid


# search email
def email_select(conn, email):
    sql = ''' SELECT email FROM user WHERE email=? '''
    cur = conn.cursor()
    cur.execute(sql, (email,))
    return cur.fetchone()

# search user for powersheet profile
def user_profile_select(conn, email):
    sql = ''' SELECT email, fname, lname, age, height, weight, gender, category, birth FROM user WHERE email=? '''
    cur = conn.cursor()
    cur.execute(sql, (email,))
    return cur.fetchone()

# create power sheet 
def create_power(conn, spreadsheet):
    sql = ''' INSERT INTO  powersheet(user_email,name,path,date)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, spreadsheet)
    return cur.lastrowid

# create graph
def create_graph(conn, graph):
    sql = ''' INSERT INTO  graph(user_email,name,path,date)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, graph)
    return cur.lastrowid

# Called from power_chart.py
def graph_insert(user_email ,name, path, date):
    database = 'cycle.db'

    # database connection
    conn = create_connection(database)
    with conn:
        # new graph
        graph = (user_email, name, path, date)
        graph_rid = create_graph(conn, graph)

# Called from power.py
def power_insert(user_email ,name, path, date):
    database = 'cycle.db'

    # database connection
    conn = create_connection(database)
    with conn:
        # new spreadsheet
        spreadsheet = (user_email, name, path, date)
        calibrate_rid = create_power(conn, spreadsheet)

# Called from power.py
def user_profile_search(email):
    database = 'cycle.db'

    # database connection
    conn = create_connection(database)
    with conn:
        # search for user
        search_result = user_profile_select(conn, email)

    return search_result


# Called from GUI.py user insertion
def user_insert(email, fname, lname, age, height, weight, gender, category, birth):
    database = 'cycle.db'

    # database connection
    conn = create_connection(database)
    with conn:
        # new user
        user = (email, fname, lname, age, height, weight, gender, category, birth)
        user_rid = create_user(conn, user)

# Called from GUI.py user update
def user_update(email, fname, lname, age, height, weight, gender, category, birth):
    database = 'cycle.db'

    # database connection
    conn = create_connection(database)
    with conn:
        # update user
        user = (fname, lname, age, height, weight, gender, category, birth, email)
        user_rid = update_user(conn, user)

# Called from calibrate.py
def calibrate_insert(name, path, date):
    database = 'cycle.db'

    # database connection
    conn = create_connection(database)
    with conn:
        # new spreadsheet
        spreadsheet = (name, path, date)
        calibrate_rid = create_calibrate(conn, spreadsheet)


# Called from run_sensor.py
def textfile_insert(user_email, name, path, date):
    database = 'cycle.db'

    # database connection
    conn = create_connection(database)
    with conn:
        # new textfile
        textfile = (user_email, name, path, date)
        text_rid = create_textfile(conn, textfile)


# Called from GUI.py email search window
def email_search(email):
    database = 'cycle.db'

    # database connection
    conn = create_connection(database)
    with conn:
        # search for email
        search_result = email_select(conn, email)

    return search_result


# search for text files
def text_file_select(conn, from_date, to_date ):
    sql = ''' SELECT fname, lname, email, name, path, date FROM user JOIN text ON user.email = text.user_email WHERE date BETWEEN ? AND ?'''
    cur = conn.cursor()
    cur.execute(sql, (from_date, to_date))
    return cur.fetchall()


# Called from GUI.py search file window
def text_file_search(from_date, to_date):
    database = 'cycle.db'

    if from_date == "" and to_date == "":
        datetime1 = from_date
        datetime2 = to_date
    else:
        d1 = datetime.strptime(from_date, '%Y-%m-%d')
        t1 = time(0, 0, 0)
        datetime1 = datetime.combine(d1, t1)
        d2 = datetime.strptime(to_date, '%Y-%m-%d')
        t2 = time(23, 59, 59)
        datetime2 = datetime.combine(d2, t2)

    # database connection
    conn = create_connection(database)
    with conn:
        # search text files for a specific date range
        search_result = text_file_select(conn, datetime1, datetime2)

    return search_result


# search for text files last 5 records
def text_file_records_select(conn):
    sql = ''' SELECT fname, lname, email, name, path, date FROM user JOIN text ON user.email = text.user_email ORDER BY date DESC LIMIT 15'''
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()


# Called from GUI.py search file window
def text_file_records_search():
    database = 'cycle.db'

    # database connection
    conn = create_connection(database)
    with conn:
        # search last 5 text files
        search_result = text_file_records_select(conn)

    return search_result


# search for power sheet files
def power_file_select(conn, from_date, to_date ):
    sql = ''' SELECT fname, lname, email, name, path, date FROM user JOIN powersheet ON user.email = powersheet.user_email WHERE date BETWEEN ? AND ?'''
    cur = conn.cursor()
    cur.execute(sql, (from_date, to_date))
    return cur.fetchall()


# Called from GUI.py search file window
def power_file_search(from_date, to_date):
    database = 'cycle.db'

    if from_date == "" and to_date == "":
        datetime1 = from_date
        datetime2 = to_date
    else:
        d1 = datetime.strptime(from_date, '%Y-%m-%d')
        t1 = time(0, 0, 0)
        datetime1 = datetime.combine(d1, t1)
        d2 = datetime.strptime(to_date, '%Y-%m-%d')
        t2 = time(23, 59, 59)
        datetime2 = datetime.combine(d2, t2)

    # database connection
    conn = create_connection(database)
    with conn:
        # search power files for a specific date range
        search_result = power_file_select(conn, datetime1, datetime2)

    return search_result


# search for power files last 5 records
def power_file_records_select(conn):
    sql = ''' SELECT fname, lname, email, name, path, date FROM user JOIN powersheet ON user.email = powersheet.user_email ORDER BY date DESC LIMIT 15'''
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()


# Called from GUI.py search file window
def power_file_records_search():
    database = 'cycle.db'

    # database connection
    conn = create_connection(database)
    with conn:
        # search last 5 power files
        search_result = power_file_records_select(conn)

    return search_result


# search for calibration file
def calibration_file_select(conn, from_date, to_date):
    sql = ''' SELECT name, path, date FROM calibration  WHERE date BETWEEN ? AND ?'''
    cur = conn.cursor()
    cur.execute(sql, (from_date, to_date))
    return cur.fetchall()


# Called from GUI.py search file window
def calibration_file_search(from_date, to_date):
    database = 'cycle.db'

    if from_date == "" and to_date == "":
        datetime1 = from_date
        datetime2 = to_date
    else:
        d1 = datetime.strptime(from_date, '%Y-%m-%d')
        t1 = time(0, 0, 0)
        datetime1 = datetime.combine(d1, t1)
        d2 = datetime.strptime(to_date, '%Y-%m-%d')
        t2 = time(23, 59, 59)
        datetime2 = datetime.combine(d2, t2)

    # database connection
    conn = create_connection(database)
    with conn:
        # search calibration file for a specific date range
        search_result = calibration_file_select(conn, datetime1, datetime2)

    return search_result


# search for calibration files last 5 records
def calibration_file_records_select(conn):
    sql = ''' SELECT name, path, date FROM calibration ORDER BY date DESC LIMIT 15'''
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()


# Called from GUI.py search file window
def calibration_file_records_search():
    database = 'cycle.db'

    # database connection
    conn = create_connection(database)
    with conn:
        # search calibration file last 5 records
        search_result = calibration_file_records_select(conn)

    return search_result


# search for graph files
def graph_file_select(conn, from_date, to_date ):
    sql = ''' SELECT fname, lname, email, name, path, date FROM user JOIN graph ON user.email = graph.user_email WHERE date BETWEEN ? AND ?'''
    cur = conn.cursor()
    cur.execute(sql, (from_date, to_date))
    return cur.fetchall()


# Called from GUI.py search file window
def graph_file_search(from_date, to_date):
    database = 'cycle.db'

    if from_date == "" and to_date == "":
        datetime1 = from_date
        datetime2 = to_date
    else:
        d1 = datetime.strptime(from_date, '%Y-%m-%d')
        t1 = time(0, 0, 0)
        datetime1 = datetime.combine(d1, t1)
        d2 = datetime.strptime(to_date, '%Y-%m-%d')
        t2 = time(23, 59, 59)
        datetime2 = datetime.combine(d2, t2)

    # database connection
    conn = create_connection(database)
    with conn:
        # search graph files for a specific date range
        search_result = graph_file_select(conn, datetime1, datetime2)

    return search_result


# search for graph files last 5 records
def graph_file_records_select(conn):
    sql = ''' SELECT fname, lname, email, name, path, date FROM user JOIN graph ON user.email = graph.user_email ORDER BY date DESC LIMIT 15'''
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()


# Called from GUI.py search file window
def graph_file_records_search():
    database = 'cycle.db'

    # database connection
    conn = create_connection(database)
    with conn:
        # search last 5 graph files
        search_result = graph_file_records_select(conn)

    return search_result


# search by user name
def user_select(conn, fname, lname, from_date, to_date):
    sql = '''SELECT fname, lname, email, name, path, date 
            FROM 
            (
            SELECT fname, lname, email, name, path, date 
            FROM user JOIN text ON user.email = text.user_email 
            UNION
            SELECT fname, lname, email, name, path, date 
            FROM user JOIN powersheet ON user.email = powersheet.user_email 
            UNION
            SELECT fname, lname, email, name, path, date 
            FROM user JOIN graph ON user.email = graph.user_email 
            )
            WHERE fname=? AND lname=? AND date BETWEEN ? AND ?'''
    cur = conn.cursor()
    cur.execute(sql, (fname, lname, from_date, to_date))
    return cur.fetchall()


# Called from GUI.py search user window
def user_search(fname, lname, from_date, to_date):
    database = 'cycle.db'

    if from_date == "" and to_date == "":
        datetime1 = from_date
        datetime2 = to_date
    else:
        d1 = datetime.strptime(from_date, '%Y-%m-%d')
        t1 = time(0, 0, 0)
        datetime1 = datetime.combine(d1, t1)
        d2 = datetime.strptime(to_date, '%Y-%m-%d')
        t2 = time(23, 59, 59)
        datetime2 = datetime.combine(d2, t2)

    # database connection
    conn = create_connection(database)
    with conn:

        # search by user for a specific date range
        search_result = user_select(conn, fname, lname, datetime1, datetime2)

    return search_result


# search for last 5 records when you search by user name and there is no date entered
def user_records_select(conn, fname, lname):
    sql = '''SELECT fname, lname, email, name, path, date 
            FROM 
            (
            SELECT fname, lname, email, name, path, date 
            FROM user JOIN text ON user.email = text.user_email 
            UNION
            SELECT fname, lname, email, name, path, date 
            FROM user JOIN powersheet ON user.email = powersheet.user_email 
            UNION
            SELECT fname, lname, email, name, path, date 
            FROM user JOIN graph ON user.email = graph.user_email 
            )
            WHERE fname=? AND lname=?
            ORDER BY date DESC LIMIT 15'''
    cur = conn.cursor()
    cur.execute(sql, (fname, lname))
    return cur.fetchall()


# Called from GUI.py search user window
def user_records_search(fname, lname):
    database = 'cycle.db'

    # database connection
    conn = create_connection(database)
    with conn:

        # search and display last 5 records
        search_result = user_records_select(conn, fname, lname)

    return search_result
