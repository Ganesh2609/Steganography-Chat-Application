import mysql.connector

def destroy_database(chat):
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="Coc0406")
    cursor = mydb.cursor()
    cursor.execute(f"DROP DATABASE IF EXISTS {chat}")
    mydb.commit()
    mydb.close()

def create_database(chat):
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="Coc0406")
    cursor = mydb.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {chat}")
    cursor.execute(f"USE {chat}")
    mydb.commit()
    mydb.close()

#recieve =0,send =1
def create_user_table(username, chat):
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="Coc0406")
    cursor = mydb.cursor()
    cursor.execute(f"USE {chat}")
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {username} (
            client TEXT,
            type TEXT,
            message LONGBLOB,
            time TEXT,
            img LONGBLOB
        )
    ''')
    mydb.commit()
    mydb.close()

def insert_message(username, client,type1,message,time,img, chat):
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="Coc0406")
    cursor = mydb.cursor()
    cursor.execute(f"USE {chat}")
    cursor.execute(f'INSERT INTO {username} (client,type,message,time,img) VALUES (%s,%s,%s,%s,%s)', (client, type1, message,time,img))
    mydb.commit()
    mydb.close()

def load_data(username, chat):
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="Coc0406")
    cursor = mydb.cursor()
    cursor.execute(f"USE {chat}")
    cursor.execute(f"SELECT * FROM {username}")
    result = cursor.fetchall()
    mydb.commit()
    mydb.close()
    if len(result) == 0:
        return 0
    return result
