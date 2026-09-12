from db import get_connection

def add_product(asin, title, unit_cost):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (asin,title,unit_cost) VALUES(?,?,?)", (asin,title,unit_cost))
    conn.commit()
    conn.close()

def get_all_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products ORDER BY title ASC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_product_by_asin(asin):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE asin = ?",(asin,))
    rows = cursor.fetchone()
    conn.close()
    return rows

def update_cost(product_id, new_cost):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET unit_cost = ? WHERE id = ?",(new_cost,product_id,))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    from db import create_table
    create_table()
    
    add_product("B001234", "Apple AirPods", 45.00)
    add_product("B005678", "Phone Case", 8.50)
    
    print(get_all_products())
    print(get_product_by_asin("B001234"))
    
    update_cost(1, 42.00)
    print(get_all_products())