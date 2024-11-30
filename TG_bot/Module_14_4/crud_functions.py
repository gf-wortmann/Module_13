import sqlite3


def initiate_db():
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products(
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL
        )
    ''')
    connection.commit()
    connection.close()


def fill_db(items_count):
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    for i in range(1, items_count + 1):
        cursor.execute('''
            INSERT INTO Products (id, title, price) VALUES (?,?,?)
        ''', (i, f'Product {i}', i * 100)
                       )
    connection.commit()
    connection.close()


def get_all_products():
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    cursor.execute('''
            SELECT * FROM products
    ''')
    
    result = cursor.fetchall()
    connection.close()
    return result


if __name__ == "__main__":
    contain = get_all_products()
    
    print(contain)
