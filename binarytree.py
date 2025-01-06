class ParkingNode:
    def __init__(self, spot_id, base_price, occupancy_status=False):
        self.spot_id = spot_id
        self.base_price = base_price
        self.occupancy_status = occupancy_status
        self.entry_time = None
        self.left = None
        self.right = None

class ParkingLotTree:
    def __init__(self):
        self.root = None
        self.total_spots = 0
        self.occupied_spots = 0
    
    def insert(self, spot_id, base_price):
        if not self.root:
            self.root = ParkingNode(spot_id, base_price)
            self.total_spots += 1
            print(f"Created new parking spot {spot_id} with base price ${base_price:.2f}")
            return True
            
        return self._insert_recursive(self.root, spot_id, base_price)
    
    def _insert_recursive(self, node, spot_id, base_price):
        if spot_id < node.spot_id:
            if node.left is None:
                node.left = ParkingNode(spot_id, base_price)
                self.total_spots += 1
                print(f"Created new parking spot {spot_id} with base price ${base_price:.2f}")
                return True
            return self._insert_recursive(node.left, spot_id, base_price)
        elif spot_id > node.spot_id:
            if node.right is None:
                node.right = ParkingNode(spot_id, base_price)
                self.total_spots += 1
                print(f"Created new parking spot {spot_id} with base price ${base_price:.2f}")
                return True
            return self._insert_recursive(node.right, spot_id, base_price)
        print(f"Error: Spot {spot_id} already exists")
        return False
    
    def find_spot(self, spot_id):
        return self._find_recursive(self.root, spot_id)
    
    def _find_recursive(self, node, spot_id):
        if not node or node.spot_id == spot_id:
            return node
        if spot_id < node.spot_id:
            return self._find_recursive(node.left, spot_id)
        return self._find_recursive(node.right, spot_id)
    
    def calculate_dynamic_price(self, spot_id, base_multiplier=1.0):
        """Calculate dynamic price based on occupancy rate and time of day"""
        occupancy_rate = self.occupied_spots / self.total_spots if self.total_spots > 0 else 0
        
        time_multiplier = self._get_time_multiplier()
        occupancy_multiplier = 1.0 + (occupancy_rate * 0.5)
        
        spot = self.find_spot(spot_id)
        if not spot:
            print(f"Error: Spot {spot_id} not found")
            return None
            
        dynamic_price = spot.base_price * base_multiplier * time_multiplier * occupancy_multiplier
        return round(dynamic_price, 2)
    
    def _get_time_multiplier(self):
        from datetime import datetime
        current_hour = datetime.now().hour
        
        if (8 <= current_hour <= 10) or (16 <= current_hour <= 19):
            return 1.5
        elif current_hour >= 23 or current_hour <= 5:
            return 0.7
        return 1.0
    
    def park_vehicle(self, spot_id):
        from datetime import datetime
        
        spot = self.find_spot(spot_id)
        if not spot:
            print(f"Error: Spot {spot_id} not found")
            return False
        if spot.occupancy_status:
            print(f"Error: Spot {spot_id} is already occupied")
            return False
            
        spot.occupancy_status = True
        spot.entry_time = datetime.now()
        self.occupied_spots += 1
        current_price = self.calculate_dynamic_price(spot_id)
        print(f"Vehicle parked in spot {spot_id}. Current rate: ${current_price:.2f}/hour")
        return True
    
    def remove_vehicle(self, spot_id):
        from datetime import datetime
        
        spot = self.find_spot(spot_id)
        if not spot:
            print(f"Error: Spot {spot_id} not found")
            return False
        if not spot.occupancy_status:
            print(f"Error: Spot {spot_id} is already empty")
            return False
            
        duration = datetime.now() - spot.entry_time
        hours = duration.total_seconds() / 3600
        final_price = self.calculate_dynamic_price(spot_id) * hours
        
        spot.occupancy_status = False
        spot.entry_time = None
        self.occupied_spots -= 1
        
        print(f"Vehicle removed from spot {spot_id}")
        print(f"Duration: {hours:.2f} hours")
        print(f"Total charge: ${final_price:.2f}")
        return True
    
    def get_available_spots(self):
        available_spots = []
        self._inorder_available(self.root, available_spots)
        return available_spots
    
    def _inorder_available(self, node, available_spots):
        if node:
            self._inorder_available(node.left, available_spots)
            if not node.occupancy_status:
                available_spots.append(node.spot_id)
            self._inorder_available(node.right, available_spots)
    
    def display_parking_status(self):
        """Display current status of the parking lot"""
        print("\n=== Parking Lot Status ===")
        print(f"Total spots: {self.total_spots}")
        print(f"Occupied spots: {self.occupied_spots}")
        print(f"Available spots: {self.total_spots - self.occupied_spots}")
        print(f"Occupancy rate: {(self.occupied_spots/self.total_spots*100):.1f}%" if self.total_spots > 0 else "0%")
        
        available = self.get_available_spots()
        print("\nAvailable spot IDs:", available)
        
        print("\nCurrent pricing:")
        if available:
            sample_price = self.calculate_dynamic_price(available[0])
            print(f"Sample rate for spot {available[0]}: ${sample_price:.2f}/hour")
        
        print("\nDetailed spot status:")
        self._display_spots_recursive(self.root)
        print("\n")
    
    def _display_spots_recursive(self, node):
        if node:
            self._display_spots_recursive(node.left)
            status = "Occupied" if node.occupancy_status else "Available"
            current_price = self.calculate_dynamic_price(node.spot_id)
            print(f"Spot {node.spot_id}: {status} - Current rate: ${current_price:.2f}/hour")
            self._display_spots_recursive(node.right)


def run_demo():

    parking_lot = ParkingLotTree()

    parking_lot.insert(101, 10.00)
    parking_lot.insert(102, 12.00)
    parking_lot.insert(103, 15.00)

    parking_lot.display_parking_status()

    parking_lot.park_vehicle(101)
    parking_lot.park_vehicle(103)

    parking_lot.display_parking_status()

    parking_lot.remove_vehicle(101)

    parking_lot.display_parking_status()

if __name__ == "__main__":
    run_demo()