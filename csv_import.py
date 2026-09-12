import csv
import os
from products import add_product, get_product_by_asin
from shipment import add_shipment, get_all_shipments
from shipment_items import add_item

def import_from_csv(filename):
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return

    count = 0 
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:   
            asin = row["ASIN"]
            title = row["Title"]
            units_sent = int(row["Units_Sent"])
            units_received = int(row["Units_Received"])
            date = row["Date"]
            shipment_id = row["Shipment_ID"]

            existing = get_product_by_asin(asin)
            if not existing:
                add_product(asin, title, 0)
                existing = get_product_by_asin(asin)

            status = "discrepancy" if units_sent != units_received else "received"
            add_shipment(shipment_id, date, status)

            
            shipments = get_all_shipments()
            shipment_db_id = shipments[-1][0]

            product_db_id = existing[0]

          
            add_item(shipment_db_id, product_db_id, units_sent, units_received)

            count += 1   

    print(f"Imported {count} rows from {filename}")   

if __name__ == "__main__":
    import_from_csv("audit.csv")

    from products import get_all_products
    from shipment import get_all_shipments
    from shipment_items import get_discrepancies

    print("Products:", get_all_products())
    print("Shipments:", get_all_shipments())
    print("Discrepancies:", get_discrepancies())