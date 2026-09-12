from db import get_connection

def add_shipment(shipment_id, date_sent, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO shipments (shipment_id,date_sent,status) VALUES(?,?,?)", (shipment_id,date_sent,status,))
    conn.commit()
    conn.close()


def get_all_shipments():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM shipments ORDER BY status ASC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_shipment(shipment_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM shipments WHERE id = ?",(shipment_id,))
    rows = cursor.fetchone()
    conn.close()
    return rows

def update_status(shipment_id, new_status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE shipments SET status = ? WHERE id = ?",(new_status,shipment_id,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    from db import create_table
    create_table()
    
    add_shipment("FBA123456", "2024-01-15", "sent")
    add_shipment("FBA789012", "2024-01-20", "discrepancy")
    
    print(get_all_shipments())
    print(get_shipment(1))
    
    update_status(1, "received")
    print(get_all_shipments())