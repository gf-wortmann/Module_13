import sqlite3


def initiate_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products(
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL
        )
    ''')
    connection.commit()


def fill_db(items_count):
    for i in range(1, items_count + 1):
        # print(f'id = {i}, title = "{i}-я жопа!"')
        cursor.execute('''
            INSERT INTO Products (id, title, price) VALUES (?,?,?)
        '''
                       , (i, f'Product {i}', i * 100)
                       )
    connection.commit()
    
    
def get_all_products():
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    cursor.execute('''
            SELECT * FROM products
    ''')
    
    result =  cursor.fetchall()
    connection.close()
    return result


def add_descriptions():
    cursor.execute('''SELECT COUNT() FROM Products''')
    a = cursor.fetchall()
    print(*a[0])
    b = a[0][0]
    print(b)
    
    for i in range(1, b + 1):
        cursor.execute('''
        UPDATE Products SET description = ? WHERE id = ?
        '''
                       , (f'description {i}', i)
                       )
    connection.commit()


if __name__ == "__main__":
    # connection = sqlite3.connect('Module_14_4/products.db')
    # cursor = connection.cursor()
    # # initiate_db()
    # fill_db(4)
    # add_descriptions()
    contain = get_all_products()
    # connection.close()
    
    print(contain)
