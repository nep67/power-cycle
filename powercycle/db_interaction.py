import sqlite3

# create connection
def create_connection(db_file):

    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

# create user
def create_user(conn, user):

    sql = ''' INSERT INTO user(email, fname, lname, age, height, weight, gender, category)
              VALUES(?,?,?,?,?,?,?,?) '''
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
def create_calibrate(conn, spreedsheet):
    sql = ''' INSERT INTO  calibration(name,path,date)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, spreedsheet)
    return cur.lastrowid

# search email
def email_select(conn, email):
    sql = ''' SELECT email FROM user WHERE email=? '''
    cur = conn.cursor()
    cur.execute(sql, (email,))
    return cur.fetchone()

## Called from GUI.py user insertion
def user_insert(email, fname, lname, age, height, weight, gender, category):

    database = 'cycle.db'

    # database connection
    conn = create_connection(database)
    with conn:
        # new user
        user = (email, fname, lname, age, height, weight, gender, category)
        user_rid = create_user(conn, user)

## Called from calibrate.py
def calibrate_insert(name, path, date):
    
    database = 'cycle.db'

    # database connection
    conn = create_connection(database)
    with conn:
        # new spreedsheet
        spreedsheet = (name, path, date)
        calibrate_rid = create_calibrate(conn, spreedsheet)

## Called from run_sensor.py
def textfile_insert(user_email, name, path, date):

    database = 'cycle.db'

    # database connection
    conn = create_connection(database)
    with conn:
        # new textfile
        textfile = (user_email, name, path, date)
        text_rid = create_textfile(conn, textfile)

## Called from GUI.py email search window
def email_search(email):
   
    database = 'cycle.db'
    
    # database connection
    conn = create_connection(database)
    with conn:
        # search for email
        search_result = email_select(conn, email)

    return search_result

