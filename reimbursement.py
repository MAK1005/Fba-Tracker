from db import get_connection

def add_reimbursement(claim_id, amount, date_received, method):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reimbursements (claim_id,amount,date_received,method) VALUES (?,?,?,?)",(claim_id,amount,date_received,method,))
    conn.commit()
    conn.close()

def get_all_reimbursements():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                SELECT reimbursements.id, products.asin, claims.units_lost,reimbursements.amount, claims.claim_date, reimbursements.date_received, reimbursements.method
                FROM reimbursements
                JOIN claims ON reimbursements.claim_id = claims.id
                JOIN products ON claims.product_id = products.id 
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows



def get_total_reimbursed():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
            SELECT SUM(amount) as amount_sum
            FROM reimbursements
    """)
    row = cursor.fetchone()
    conn.close()
    return row [0]


if __name__ == "__main__":
    from db import create_table
    from products import add_product
    from shipment import add_shipment
    from claims import add_claim
    create_table()
    
    add_product("B001234", "AirPods", 45.00)
    add_shipment("FBA123456", "2024-01-15", "discrepancy")
    add_claim(1, 1, 2, "2024-01-20", "approved", "2 units missing")
    
    add_reimbursement(1, 90.00, "2024-02-01", "cash")
    
    print(get_all_reimbursements())
    print("Total reimbursed:", get_total_reimbursed())