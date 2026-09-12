from db import get_connection

def add_claim(shipment_id, product_id, units_lost, claim_date, status, notes):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO claims (shipment_id,product_id,units_lost,claim_date,status,notes) VALUES (?,?,?,?,?,?)", (shipment_id,product_id,units_lost,claim_date,status,notes,))
    conn.commit()
    conn.close()

def get_all_claims():    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT claims.id, shipments.shipment_id, products.asin, products.title, claims.units_lost, claims.claim_date, claims.status
                    FROM claims
                    JOIN products ON claims.product_id = products.id
                    JOIN shipments ON claims.shipment_id = shipments.id
                    ORDER BY claim_date DESC        
            """)
    rows = cursor.fetchall()
    conn.close()
    return rows
    

def get_claims_by_status(status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT claims.id, shipments.shipment_id, products.asin, products.title, claims.units_lost, claims.claim_date, claims.status
                    FROM claims
                    JOIN products ON claims.product_id = products.id
                    JOIN shipments ON claims.shipment_id = shipments.id
                    WHERE claims.status = ?""", (status,))
    rows = cursor.fetchall()
    conn.close()
    return rows
    
def update_claim_status(claim_id, new_status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE claims SET status = ? WHERE id = ?", (new_status,claim_id,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    from db import create_table
    from products import add_product
    from shipment import add_shipment
    create_table()
    
    add_product("B001234", "AirPods", 45.00)
    add_shipment("FBA123456", "2024-01-15", "discrepancy")
    
    add_claim(1, 1, 2, "2024-01-20", "pending", "2 units missing from shipment")
    
    print(get_all_claims())
    print(get_claims_by_status("pending"))
    
    update_claim_status(1, "submitted")
    print(get_all_claims())