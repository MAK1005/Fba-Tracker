import csv
import os
from datetime import datetime
from claims import get_all_claims
from reports import recovery_rate, total_value_lost, total_units_lost_by_product

def export_claims_csv(filename=None):
    if filename is None:
        filename = f"claims_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    with open(filename, "w", newline="") as f:     
        writer = csv.DictWriter(f, fieldnames=["Shipment_ID", "ASIN", "Title", "Units_lost", "Claim_Date", "Status", "Notes"])
        writer.writeheader()                            
        claims = get_all_claims()
        for claim in claims:
            writer.writerow({
                "Shipment_ID": claim[1],
                "ASIN": claim[2],
                "Title": claim[3],
                "Units_lost": claim[4],
                "Claim_Date": claim[5],
                "Status": claim[6]
        })
    print(f"Exported {len(claims)} claims to {filename}")

def export_summary_csv(filename=None):
     reimbursed, total_lost = recovery_rate()
     products_lost = total_value_lost()  
     units_lost = total_units_lost_by_product()

     if filename is None:
            filename = f"claims_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
     with open(filename, "w", newline="") as f:     
             writer = csv.DictWriter(f, fieldnames=["ASIN", "Title", "Units_Lost", "Value_Lost", "Reimbursed", "Recovery_Rate"])
             writer.writeheader()  

             for i, row in enumerate(products_lost):
               writer.writerow({
                   "ASIN": row[0],
                   "Title": row[1],
                   "Units_Lost": units_lost[i][2] if i < len(units_lost) else 0,
                   "Value_Lost": row[2],
                   "Reimbursed": reimbursed,
                   "Recovery_Rate": f"{(reimbursed/total_lost*100):.1f}%" if total_lost > 0 else "0%"
               })



if __name__ == "__main__":
    export_claims_csv()
    export_summary_csv()