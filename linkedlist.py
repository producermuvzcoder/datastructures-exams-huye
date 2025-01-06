class ParkingOrder:
    def __init__(self, vehicle_id, entry_time, base_price):
        self.vehicle_id = vehicle_id
        self.entry_time = entry_time
        self.base_price = base_price
        self.dynamic_price = base_price
        self.next = None
        self.exit_time = None

class ParkingOrderManager:
    def __init__(self, max_capacity):
        self.head = None
        self.size = 0
        self.max_capacity = max_capacity
    
    def add_order(self, vehicle_id, entry_time, base_price):
        if self.size >= self.max_capacity:
            print(f"Parking lot full! Cannot add order for vehicle {vehicle_id}")
            return False
            
        new_order = ParkingOrder(vehicle_id, entry_time, base_price)

        occupancy_rate = self.size / self.max_capacity
        if occupancy_rate > 0.8:
            new_order.dynamic_price = base_price * 1.5
        elif occupancy_rate > 0.6:
            new_order.dynamic_price = base_price * 1.25

        new_order.next = self.head
        self.head = new_order
        self.size += 1
        return True
        
    def remove_order(self, vehicle_id, exit_time):
        current = self.head
        prev = None
        
        while current:
            if current.vehicle_id == vehicle_id:
                current.exit_time = exit_time
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                self.size -= 1
                return current
            prev = current
            current = current.next
        return None
        
    def get_order(self, vehicle_id):
        current = self.head
        while current:
            if current.vehicle_id == vehicle_id:
                return current
            current = current.next
        return None
        
    def display_orders(self):
        current = self.head
        orders = []
        while current:
            order_info = {
                "vehicle_id": current.vehicle_id,
                "entry_time": current.entry_time,
                "base_price": current.base_price,
                "dynamic_price": current.dynamic_price,
                "exit_time": current.exit_time
            }
            orders.append(order_info)
            current = current.next
        return orders

if __name__ == "__main__":

    parking_manager = ParkingOrderManager(5)

    parking_manager.add_order("CAR001", "09:00", 100)
    parking_manager.add_order("CAR002", "09:30", 100)
    parking_manager.add_order("CAR003", "10:00", 100)
    parking_manager.add_order("CAR004", "10:30", 100) 
    
    print("\nCurrent Orders:")
    for order in parking_manager.display_orders():
        print(f"Vehicle: {order['vehicle_id']}")
        print(f"Entry Time: {order['entry_time']}")
        print(f"Base Price: ${order['base_price']}")
        print(f"Dynamic Price: ${order['dynamic_price']}")
        print("---")

    removed_order = parking_manager.remove_order("CAR002", "11:30")
    if removed_order:
        print(f"\nRemoved order for vehicle {removed_order.vehicle_id}")
        print(f"Duration: {removed_order.entry_time} to {removed_order.exit_time}")
        print(f"Final Price: ${removed_order.dynamic_price}")