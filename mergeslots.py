class ParkingSpot:
    def __init__(self, id, zone, floor, base_price, priority_level=1):
        self.id = id
        self.zone = zone
        self.floor = floor
        self.base_price = base_price
        self.priority_level = priority_level 
        self.is_occupied = False
        self.occupancy_time = None

    def calculate_dynamic_price(self, zone_occupancy_rate):

        occupancy_multiplier = 1 + (0.5 * zone_occupancy_rate)
        priority_multiplier = 1 + (0.1 * self.priority_level)
        return round(self.base_price * occupancy_multiplier * priority_multiplier, 2)

    def __str__(self):
        status = "Occupied" if self.is_occupied else "Available"
        return f"Spot {self.id} ({self.zone}-{self.floor}) - Priority: {self.priority_level}, Base Price: ${self.base_price}, Status: {status}"

def merge_sort(parking_spots, key_func):
    if len(parking_spots) <= 1:
        return parking_spots

    mid = len(parking_spots) // 2
    left = parking_spots[:mid]
    right = parking_spots[mid:]

    left = merge_sort(left, key_func)
    right = merge_sort(right, key_func)

    return merge(left, right, key_func)

def merge(left, right, key_func):
    result = []
    left_idx, right_idx = 0, 0

    while left_idx < len(left) and right_idx < len(right):

        if key_func(left[left_idx]) <= key_func(right[right_idx]):
            result.append(left[left_idx])
            left_idx += 1
        else:
            result.append(right[right_idx])
            right_idx += 1

    result.extend(left[left_idx:])
    result.extend(right[right_idx:])
    return result

class ParkingLotManager:
    def __init__(self):
        self.parking_spots = []
        self.zone_occupancy = {"Premium": 0.0, "Standard": 0.0}

    def add_spot(self, spot):
        self.parking_spots.append(spot)

    def update_zone_occupancy(self, zone):
        zone_spots = [spot for spot in self.parking_spots if spot.zone == zone]
        occupied_spots = len([spot for spot in zone_spots if spot.is_occupied])
        total_spots = len(zone_spots)
        self.zone_occupancy[zone] = occupied_spots / total_spots if total_spots > 0 else 0.0

    def sort_by_priority(self):
        return merge_sort(self.parking_spots, 
                         key_func=lambda x: (-x.priority_level, x.base_price))

    def sort_by_price(self):
        return merge_sort(self.parking_spots, 
                         key_func=lambda x: x.calculate_dynamic_price(self.zone_occupancy[x.zone]))

    def sort_by_availability_and_priority(self):
        return merge_sort(self.parking_spots, 
                         key_func=lambda x: (x.is_occupied, -x.priority_level))

    def display_spots(self, spots):
        for spot in spots:
            dynamic_price = spot.calculate_dynamic_price(self.zone_occupancy[spot.zone])
            print(f"{spot} (Dynamic Price: ${dynamic_price})")

def main():

    manager = ParkingLotManager()

    spots_data = [
        ("P1", "Premium", "F1", 15.0, 5), 
        ("P2", "Premium", "F1", 14.0, 4),
        ("P3", "Premium", "F2", 13.0, 4),
        ("S1", "Standard", "F1", 8.0, 3),
        ("S2", "Standard", "F1", 7.0, 2),
        ("S3", "Standard", "F2", 6.0, 1), 
    ]

    for id, zone, floor, price, priority in spots_data:
        spot = ParkingSpot(id, zone, floor, price, priority)
        manager.add_spot(spot)

    manager.parking_spots[0].is_occupied = True
    manager.parking_spots[3].is_occupied = True  

    manager.update_zone_occupancy("Premium")
    manager.update_zone_occupancy("Standard")

    print("1. Sorted by Priority (High to Low):")
    priority_sorted = manager.sort_by_priority()
    manager.display_spots(priority_sorted)

    print("\n2. Sorted by Dynamic Price (Low to High):")
    price_sorted = manager.sort_by_price()
    manager.display_spots(price_sorted)

    print("\n3. Sorted by Availability and Priority:")
    availability_sorted = manager.sort_by_availability_and_priority()
    manager.display_spots(availability_sorted)

if __name__ == "__main__":
    main()