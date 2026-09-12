import sqlite3 

db_file = "week_6.db"

def get_connection():
    return sqlite3.connect(db_file)

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS reimbursements")
    cursor.execute("DROP TABLE IF EXISTS claims")
    cursor.execute("DROP TABLE IF EXISTS shipment_items")
    cursor.execute("DROP TABLE IF EXISTS products")      
    cursor.execute("DROP TABLE IF EXISTS shipments")
    cursor.execute("""                                                                  
                  CREATE TABLE IF NOT EXISTS shipments (
                  id               INTEGER PRIMARY KEY AUTOINCREMENT,
                  shipment_id      TEXT,
                  date_sent        TEXT,
                  status           TEXT
                  )
                  """)
    cursor.execute("""
                  CREATE TABLE IF NOT EXISTS products (
                  id               INTEGER PRIMARY KEY AUTOINCREMENT,
                  asin             TEXT,
                  title            TEXT,
                  unit_cost        REAL
                )
                """)
    cursor.execute("""
                  CREATE TABLE IF NOT EXISTS shipment_items (
                  id               INTEGER PRIMARY KEY AUTOINCREMENT,
                  shipment_id      INTEGER,
                  product_id       INTEGER,
                  units_sent       INTEGER,
                  units_received   INTEGER,
                  FOREIGN KEY (shipment_id) REFERENCES shipments(id),
                  FOREIGN KEY (product_id) REFERENCES products(id)
                  )
            """)
    cursor.execute("""  
                CREATE TABLE IF NOT EXISTS claims (
                id                 INTEGER PRIMARY KEY AUTOINCREMENT,
                shipment_id        INTEGER,
                product_id         INTEGER,
                units_lost         INTEGER,
                claim_date         TEXT, 
                status             TEXT,
                notes              TEXT,
                FOREIGN KEY (shipment_id) REFERENCES shipments(id),
                FOREIGN KEY (product_id) REFERENCES products(id)               
                )
                """)
    
    cursor.execute(""" 
                CREATE TABLE IF NOT EXISTS reimbursements(
                id                 INTEGER PRIMARY KEY AUTOINCREMENT,
                claim_id           INTEGER,
                amount             REAL,
                date_received      TEXT,
                method             TEXT,
                FOREIGN KEY (claim_id) REFERENCES claims(id)
                )
                """)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_table()
    print("All tables created successfully")
