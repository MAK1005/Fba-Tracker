from db import get_connection

def total_units_lost_by_product():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT products.asin, products.title, SUM(claims.units_lost) as unit_lost_sum
        FROM claims
        JOIN products ON claims.product_id = products.id
        GROUP BY products.id
        ORDER BY unit_lost_sum DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows



def total_value_lost():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT products.asin, products.title, SUM(claims.units_lost * products.unit_cost) as value_lost
        FROM claims
        JOIN products ON claims.product_id = products.id
        GROUP BY products.id
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows
    

def claims_by_status():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
            SELECT status, COUNT(*)
            FROM claims
            GROUP BY claims.status
        """)
    row = cursor.fetchall()
    conn.close()
    return row
    

def recovery_rate():
    conn= get_connection()
    cursor = conn.cursor()
    cursor.execute("""
         SELECT SUM(amount)
         FROM reimbursements
         """)
    reim_sum = cursor.fetchone() or 0

    cursor.execute("""
             SELECT SUM (claims.units_lost * products.unit_cost) as recovered 
             FROM claims 
             JOIN products ON claims.product_id = products.id
        """)
    recov = cursor.fetchone() or 0 
    conn.close()
    return reim_sum [0], recov[0]
    
    


def shipments_with_discrepancies():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
         SELECT shipments.status, shipment_items.id 
         FROM shipments
         JOIN shipment_items ON shipments.id = shipment_items.shipment_id
         WHERE shipments.status = 'discrepancy'
        """)
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    from db import create_table
    from products import add_product
    from shipment import add_shipment
    from shipment_items import add_item
    from claims import add_claim
    from reimbursement import add_reimbursement
    create_table()
    
    add_product("B001234", "AirPods", 45.00)
    add_product("B005678", "Phone Case", 8.50)
    add_shipment("FBA123456", "2024-01-15", "discrepancy")
    add_item(1, 1, 10, 8)
    add_item(1, 2, 5, 3)
    add_claim(1, 1, 2, "2024-01-20", "approved", "2 units missing")
    add_claim(1, 2, 2, "2024-01-20", "pending", "2 units missing")
    add_reimbursement(1, 90.00, "2024-02-01", "cash")

    print("\n=== Units Lost by Product ===")
    for row in total_units_lost_by_product():
        print(f"{row[1]} ({row[0]}) — {row[2]} units lost")

    print("\n=== Value Lost ===")
    for row in total_value_lost():
        print(f"{row[1]} — ${row[2]:.2f} lost")

    print("\n=== Claims by Status ===")
    for row in claims_by_status():
        print(f"{row[0]} — {row[1]} claims")

    print("\n=== Recovery Rate ===")
    reimbursed, lost = recovery_rate()
    print(f"Reimbursed: ${reimbursed:.2f}")
    print(f"Total lost: ${lost:.2f}")
    if lost > 0:
        print(f"Recovery rate: {(reimbursed/lost)*100:.1f}%")

    print("\n=== Shipments with Discrepancies ===")
    for row in shipments_with_discrepancies():
        print(row)