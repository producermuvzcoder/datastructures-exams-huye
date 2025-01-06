class ParkingNode:
    def __init__(self, name, base_price=0, parent=None):
        self.name = name
        self.base_price = base_price
        self.parent = parent
        self.children = []
        self.occupancy = 0
        self.capacity = 0

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def calculate_dynamic_price(self):

        occupancy_rate = self.occupancy / self.capacity if self.capacity > 0 else 0

        multiplier = 1 + (0.5 * occupancy_rate)
        return round(self.base_price * multiplier, 2)

    def update_occupancy(self, value):
        self.occupancy = value
  
        if self.parent:
            parent_total_occupancy = sum(child.occupancy for child in self.parent.children)
            self.parent.update_occupancy(parent_total_occupancy)

class ParkingTree:
    def __init__(self):
        self.root = ParkingNode("Parking Lot")

    def add_zone(self, zone_name, base_price):
        zone = ParkingNode(zone_name, base_price)
        self.root.add_child(zone)
        return zone

    def add_floor(self, zone, floor_name, base_price):
        floor = ParkingNode(floor_name, base_price)
        zone.add_child(floor)
        return floor

    def add_spot(self, floor, spot_name, base_price):
        spot = ParkingNode(spot_name, base_price)
        spot.capacity = 1
        floor.add_child(spot)
  
        current = floor
        while current:
            current.capacity += 1
            current = current.parent
        return spot

    def display_structure(self, node=None, level=0):
        if node is None:
            node = self.root
        
        indent = "  " * level
        price_info = f" (Base: ${node.base_price}, Current: ${node.calculate_dynamic_price()})" if node.base_price > 0 else ""
        occupancy_info = f" [Occupancy: {node.occupancy}/{node.capacity}]" if node.capacity > 0 else ""
        
        print(f"{indent}{node.name}{price_info}{occupancy_info}")
        
        for child in node.children:
            self.display_structure(child, level + 1)

def main():

    parking_lot = ParkingTree()

    premium_zone = parking_lot.add_zone("Premium Zone", 10.0)
    standard_zone = parking_lot.add_zone("Standard Zone", 5.0)

    premium_f1 = parking_lot.add_floor(premium_zone, "P-Floor 1", 12.0)
    premium_f2 = parking_lot.add_floor(premium_zone, "P-Floor 2", 11.0)

    standard_f1 = parking_lot.add_floor(standard_zone, "S-Floor 1", 6.0)
    standard_f2 = parking_lot.add_floor(standard_zone, "S-Floor 2", 5.5)

    spots_p1 = [parking_lot.add_spot(premium_f1, f"P1-Spot {i}", 15.0) for i in range(1, 4)]
    spots_p2 = [parking_lot.add_spot(premium_f2, f"P2-Spot {i}", 14.0) for i in range(1, 4)]

    spots_s1 = [parking_lot.add_spot(standard_f1, f"S1-Spot {i}", 7.0) for i in range(1, 6)]
    spots_s2 = [parking_lot.add_spot(standard_f2, f"S2-Spot {i}", 6.5) for i in range(1, 6)]

    print("Initial Parking Lot Structure:")
    parking_lot.display_structure()

    spots_p1[0].update_occupancy(1)
    spots_p1[1].update_occupancy(1)
    spots_s1[0].update_occupancy(1) 
    spots_s1[1].update_occupancy(1)
    print("\nParking Lot Structure After Some Activity:")
    parking_lot.display_structure()

if __name__ == "__main__":
    main()