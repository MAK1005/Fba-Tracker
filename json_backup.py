import json
import os
from datetime import datetime
from db import get_connection
from products import get_all_products
from shipment import get_all_shipments
from claims import get_all_claims

def backup_all(filename=None):

    if filename is None:
            filename = f"claims_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(filename, "w") as f:     
                data = {
                "products": get_all_products(),
                "shipments": get_all_shipments(),
                "claims": get_all_claims()
                }
                json.dump(data, f, indent=4)
                print(f"Backup saved to {filename}")

def restore_from_backup(filename):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return

    conn = get_connection()
    cursor = conn.cursor()
    
    for p in data.get("products", []):
        cursor.execute("""
            INSERT OR IGNORE INTO products (id, asin, title, unit_cost)
            VALUES (?,?,?,?)
        """, (p[0], p[1], p[2], p[3]))

    for s in data.get("shipments", []):
        cursor.execute("""
            INSERT OR IGNORE INTO shipments (id, shipment_id, date_sent, status)
            VALUES (?,?,?,?)
        """, (s[0], s[1], s[2], s[3]))

    for c in data.get("claims", []):
        cursor.execute("""
            INSERT OR IGNORE INTO claims (id, shipment_id, product_id, units_lost, claim_date, status, notes)
            VALUES (?,?,?,?,?,?,?)
        """, (c[0], c[1], c[2], c[3], c[4], c[5], c[6]))

    conn.commit()
    conn.close()
    print(f"Restored from {filename}")


if __name__ == "__main__":
    backup_all()
    restore_from_backup("claims_20260907_192438.json")