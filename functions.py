import psycopg2
import tabulate
import dotenv
import os

dotenv.load_dotenv()


def connect_to_db():
    conn = psycopg2.connect(
        host=os.environ.get('host'),
        database=os.environ.get('database'),
        user=os.environ.get('user'),
        password=os.environ.get('password'),
        port=os.environ.get('port')
    )
    return conn


def read_from_db():
    table = "tproduct"
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(
        f"SELECT * FROM {table}"
    )
    result = cur.fetchall()
    headers = ["Id", "Name", "Price", "Date", "Category"]
    t = tabulate.tabulate(result, headers=headers, tablefmt="pretty")
    cur.close()
    conn.close()
    return t


def read_category_table():
    table = "categories"
    conn = connect_to_db()
    cur = conn.cursor()
    query = f"SELECT * from {table}"
    cur.execute(query)
    result = cur.fetchall()
    conn.close()
    cur.close()
    return tabulate.tabulate(result, headers=['Id', 'Name', 'Description'], tablefmt='pretty')


def write_to_db(name, price, category):
    table = "tproduct"
    conn = connect_to_db()
    cur = conn.cursor()
    query = f"INSERT INTO {table} (name, price, category) VALUES (%s, %s, %s);"
    values = (name, price, category)
    cur.execute(query, values)
    conn.commit()
    conn.close()
    cur.close()


def delete_from_table(id_product):
    table = "tproduct"
    conn = connect_to_db()
    cur = conn.cursor()
    query = f"DELETE FROM {table} WHERE id = %s;"
    cur.execute(query, (id_product,))
    conn.commit()
    conn.close()
    cur.close()


def update_table(id_product, name=None, price=None, category=None):
    table = "tproduct"
    conn = connect_to_db()
    cur = conn.cursor()

    query = f"UPDATE {table} SET name = %s, price = %s, category = %s WHERE id = %s"
    values = (name, price, category, id_product)

    cur.execute(query, values)
    conn.commit()
    conn.close()
    cur.close()


def read_table_user():
    table = "users"
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(
        f"SELECT * FROM {table}"
    )
    result = cur.fetchall()
    return result


def write_table_user(name, surname, username, gmail, password):
    data = read_table_user()
    table = "users"
    conn = connect_to_db()
    cur = conn.cursor()
    user_id = -1
    query = f"INSERT INTO {table} (name, surname, username, gmail, password, superuser) VALUES (%s, %s, %s, %s, %s, %s);"
    values = (name, surname, username, gmail, password, True if not data else False)
    try:
        cur.execute(query, values)
        conn.commit()
        conn.close()
        user_id = read_table_user()[-1][0]
        print("Successfully registered user")
        return user_id
    except psycopg2.errors.UniqueViolation:
        print("username or gmail already exists")
        return user_id


def signup():
    name = input("name: ")
    surname = input("surname: ")
    username = input("username: ")
    gmail = input("gmail: ")
    password = input("password: ")
    return write_table_user(name, surname, username, gmail, password)


def login():
    username = input("username: ")
    password = input("password: ")
    conn = connect_to_db()
    cur = conn.cursor()
    query = '''
    select * from users where username = %s and password =%s;
    '''
    values = (username, password)
    cur.execute(query, values)
    result = cur.fetchone()
    conn.close()
    return result[0] if result else -1


def is_superuser(user_id):
    conn = connect_to_db()
    cur = conn.cursor()
    query = '''
    select * from users where id = %s;
    '''
    values = (user_id, )
    cur.execute(query, values)
    result = cur.fetchone()
    conn.close()
    return result[-1]
