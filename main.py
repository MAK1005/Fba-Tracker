from db import create_table
from products import add_product, get_all_products
from shipment import add_shipment, get_all_shipments
from shipment_items import add_item, get_discrepancies
from claims import add_claim, get_all_claims, get_claims_by_status
from reimbursement import add_reimbursement, get_all_reimbursements, get_total_reimbursed
from reports import (total_units_lost_by_product, total_value_lost,
                     claims_by_status, recovery_rate, shipments_with_discrepancies)

if __name__ == "__main__":
    create_table()
    print("=== FBA Lost Inventory & Reimbursement Tracker ===\n")

    add_product("BOI9012", "Apple airpods 3", 250)
    add_product("BOP7201", "Samsung s24", 500)
    add_product("BQW8910", "Earpiece", 20)

    add_shipment(1,"26-05-01","sent")
    add_shipment(2,"20-04-02", "discrepency")
    add_shipment(3,"15=03-01", "sent")

    add_item(1, 1, 10, 8)
    add_item(2,2,11,9)
    add_item(3,3,12,10)
    
    add_claim(1, 1, 2, "2024-01-20", "pending", "2 units missing from shipment")
    add_claim(2, 2, 3, "2025-01-05", "approved", "No units missing from shipment")
    add_claim(3, 3, 4, "2026-11-02", "pending", "5 units missing from shipment")

    add_reimbursement(1, 90.00, "2024-02-01", "cash")
    add_reimbursement(2, 10.00, "2026-12-11", "card")

    print("\n=== Products ===")
    for row in get_all_products():
        print(f"ID:{row[0]}  ASIN:{row[1]}  {row[2]}  ${row[3]:.2f}")

    print("\n=== Shipments ===")
    for row in get_all_shipments():
        print(f"ID:{row[0]}  Shipment:{row[1]}  Date:{row[2]}  Status:{row[3]}")

    print("\n=== Discrepancies ===")
    for row in get_discrepancies():
        print(f"Shipment:{row[1]}  ASIN:{row[2]}  {row[3]}  Sent:{row[4]}  Received:{row[5]}  Lost:{row[4]-row[5]}")

    print("\n=== Claims ===")
    for row in get_all_claims():
        print(f"ID:{row[0]}  Shipment:{row[1]}  {row[3]}  Units lost:{row[4]}  Date:{row[5]}  Status:{row[6]}")

    print("\n=== Reimbursements ===")
    for row in get_all_reimbursements():
        print(f"ASIN:{row[1]}  Units:{row[2]}  Amount:${row[3]:.2f}  Date:{row[5]}  Method:{row[6]}")

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
