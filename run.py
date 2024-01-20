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


def read_from_db(table="tproduct"):
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


while True:
    print("Exit | Create | Read | Update | Delete [0|1|2|3|4] ")
    option = int(input("option: "))
    if option == 0:
        break
    elif option == 1:
        print("Category table:")
        print(read_category_table())
        name_product = input("name: ")
        price_product = float(input("price: "))
        category_product = int(input("category: "))
        write_to_db(name=name_product, price=price_product, category=category_product)
    elif option == 2:
        print(read_from_db())
    elif option == 3:
        print(read_from_db())
        product_id = int(input("id_product: "))
        name_product = input("name: ")
        price_product = float(input("price: "))
        print("Category table:")
        print(read_category_table())
        category_product = int(input("category: "))
        update_table(id_product=product_id, name=name_product, price=price_product, category=category_product)
    elif option == 4:
        print(read_from_db())
        product_id = int(input("id_product: "))
        delete_from_table(id_product=product_id)
