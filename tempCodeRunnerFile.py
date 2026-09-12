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