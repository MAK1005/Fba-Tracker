from db import get_connection

def add_item(shipment_id, product_id, units_sent, units_received):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO shipment_items (shipment_id,product_id,units_sent,units_received) VALUES (?,?,?,?)",(shipment_id,product_id,units_sent,units_received,))
    conn.commit()
    conn.close()

def get_items_by_shipment(shipment_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT shipment_items.id, products.asin, products.title, shipment_items.units_sent, shipment_items.units_received
                     FROM shipment_items
                     JOIN products ON shipment_items.product_id = products.id
                     WHERE shipment_id = ?
            """,(shipment_id,)) 
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_discrepancies():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                SELECT shipment_items.id, shipments.shipment_id, products.asin, products.title, shipment_items.units_sent, shipment_items.units_received
                FROM shipment_items
                JOIN products ON shipment_items.product_id = products.id 
                JOIN shipments ON shipment_items.shipment_id = shipments.id
                WHERE shipment_items.units_sent != shipment_items.units_received
        """)
    rows =  cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    from db import create_table
    from products import add_product
    from shipment import add_shipment
    create_table()
    
    add_product("B001234", "AirPods", 45.00)
    add_product("B005678", "Phone Case", 8.50)
    add_shipment("FBA123456", "2024-01-15", "discrepancy")
    
    add_item(1, 1, 10, 8)   # 2 units lost
    add_item(1, 2, 5, 5)    # none lost
    
    print(get_items_by_shipment(1))
    print(get_discrepancies())