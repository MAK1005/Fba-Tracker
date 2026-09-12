class Product:
    def __init__(self, id, asin, title, unit_cost):
        self.id = id
        self.asin = asin
        self.title = title
        self.unit_cost = unit_cost

    def total_value_lost(self, units_lost):
        tvl = self.unit_cost * units_lost
        return f"units value lost = {tvl}"
        

    def __str__(self):
        return f"ASIN:{self.asin}  {self.title}  ${self.unit_cost:.2f}"

    def to_dict(self):
        return {
            "id": self.id,
            "asin": self.asin,
            "title": self.title,
            "unit_cost": self.unit_cost
        }

    @classmethod
    def from_db_row(cls, row):
        return cls(row[0], row[1], row[2], row[3])

class Shipment:
    def __init__(self, id, shipment_id, date_sent, status):
        self.id = id
        self.shipment_id = shipment_id
        self.date_sent = date_sent
        self.status = status

        

    def is_discrepancy(self):
        return self.status == "discrepancy"


        

    def __str__(self):
            return f"Shipment:{self.shipment_id}  Date:{self.date_sent}  Status:{self.status}"

    def to_dict(self):
        return {
            "id": self.id,
            "asin": self.asin,
            "title": self.title,
            "unit_cost": self.unit_cost
        }

    @classmethod
    def from_db_row(cls, row):
        return cls(row[0], row[1], row[2], row[3])

class Claim:
    def __init__(self, id, shipment_id, asin, title, units_lost, claim_date, status):
        self.id = id
        self.shipment_id = shipment_id
        self.asin = asin
        self.title = title
        self.units_lost = units_lost
        self.claim_date = claim_date
        self.status = status

    def is_pending(self):
        return self.status == "pending"
        

    def value_lost(self, unit_cost):
        vl = self.units_lost *unit_cost
        return f"VALUE LOSS = {vl}"
        

    def __str__(self):
            return f"Claim:{self.id}  {self.title}  Units lost:{self.units_lost}  Status:{self.status}"

    def to_dict(self):
        return {
            "id": self.id,
            "asin": self.asin,
            "title": self.title,
            "unit_cost": self.unit_cost
        }

    @classmethod
    def from_db_row(cls, row):
        return cls(row[0], row[1], row[2], row[3])
    
if __name__ == "__main__":
    from products import get_all_products

    products = [Product.from_db_row(row) for row in get_all_products()]
    for p in products:
        print(p)
        print(p.to_dict())