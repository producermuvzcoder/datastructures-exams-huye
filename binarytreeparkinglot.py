class ParkingSpot:
    def __init__(self, spot_id, floor, section, base_price):
        self.spot_id = spot_id
        self.floor = floor
        self.section = section
        self.base_price = base_price
        self.is_occupied = False
        self.current_price = base_price
        self.occupation_time = None

class TreeNode:
    def __init__(self, parking_spot):
        self.parking_spot = parking_spot
        self.left = None
        self.right = None
        
class ParkingLotSystem:
    def __init__(self):
        self.root = None
        self.total_spots = 0
        self.occupied_spots = 0
        
    def insert_spot(self, spot):
        if not self.root:
            self.root = TreeNode(spot)
            self.total_spots += 1
            return True
            
        current = self.root
        while True:
            if spot.spot_id < current.parking_spot.spot_id:
                if current.left is None:
                    current.left = TreeNode(spot)
                    self.total_spots += 1
                    return True
                current = current.left
            elif spot.spot_id > current.parking_spot.spot_id:
                if current.right is None:
                    current.right = TreeNode(spot)
                    self.total_spots += 1
                    return True
                current = current.right
            else:
                return False
    
    def find_spot(self, spot_id):
        current = self.root
        while current:
            if spot_id == current.parking_spot.spot_id:
                return current.parking_spot
            elif spot_id < current.parking_spot.spot_id:
                current = current.left
            else:
                current = current.right
        return None
    
    def calculate_dynamic_price(self, spot):

        occupancy_rate = self.occupied_spots / self.total_spots

        time_multiplier = 1.0
        occupancy_multiplier = 1.0

        if occupancy_rate > 0.8:
            occupancy_multiplier = 1.5
        elif occupancy_rate > 0.6:
            occupancy_multiplier = 1.3
        elif occupancy_rate > 0.4:
            occupancy_multiplier = 1.1

        spot.current_price = spot.base_price * occupancy_multiplier * time_multiplier
        return spot.current_price
    
    def occupy_spot(self, spot_id, timestamp):
        spot = self.find_spot(spot_id)
        if spot and not spot.is_occupied:
            spot.is_occupied = True
            spot.occupation_time = timestamp
            self.occupied_spots += 1
            self.calculate_dynamic_price(spot)
            return True
        return False
    
    def release_spot(self, spot_id, timestamp):
        spot = self.find_spot(spot_id)
        if spot and spot.is_occupied:
            spot.is_occupied = False
            spot.occupation_time = None
            self.occupied_spots -= 1
            self.calculate_dynamic_price(spot)
            return True
        return False
    
    def get_available_spots(self):
        available_spots = []
        def inorder_traversal(node):
            if node:
                inorder_traversal(node.left)
                if not node.parking_spot.is_occupied:
                    available_spots.append(node.parking_spot)
                inorder_traversal(node.right)
        
        inorder_traversal(self.root)
        return available_spots

import time

parking_system = ParkingLotSystem()

spots = [
    ParkingSpot(101, 1, "A", 10.0),
    ParkingSpot(102, 1, "A", 10.0),
    ParkingSpot(103, 1, "B", 12.0),
    ParkingSpot(201, 2, "A", 15.0),
    ParkingSpot(202, 2, "B", 15.0),
]

for spot in spots:
    parking_system.insert_spot(spot)

current_time = time.time()

print("Occupying spot 101:")
parking_system.occupy_spot(101, current_time)
spot = parking_system.find_spot(101)
print(f"Spot 101 current price: ${spot.current_price:.2f}")

available = parking_system.get_available_spots()
print(f"\nAvailable spots: {len(available)}")
for spot in available:
    print(f"Spot {spot.spot_id}: ${spot.current_price:.2f}")