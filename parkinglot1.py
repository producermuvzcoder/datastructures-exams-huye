from enum import Enum
from datetime import datetime, timedelta
from typing import Optional, List
import time

class SpotType(Enum):
    STANDARD = "standard"
    COMPACT = "compact"
    HANDICAP = "handicap"
    ELECTRIC = "electric"

class ParkingSpot:
    def __init__(self, spot_id: str, spot_type: SpotType, base_rate: float):
        self.spot_id = spot_id
        self.type = spot_type
        self.base_rate = base_rate
        self.available = True

class ParkingRecord:
    def __init__(self, vehicle_id: str, spot_id: str, entry_time: datetime):
        self.vehicle_id = vehicle_id
        self.spot_id = spot_id
        self.entry_time = entry_time

class ParkingArray:
    """Custom Array implementation for parking management"""
    def __init__(self):
        self._spots = [None] * 10
        self._size = 0

    def add(self, spot: ParkingSpot) -> None:
        """Add a parking spot to the array"""
        if self._size == len(self._spots):
            self._resize()
        self._spots[self._size] = spot
        self._size += 1

    def remove(self, spot_id: str) -> bool:
        """Remove a parking spot by its ID"""
        for i in range(self._size):
            if self._spots[i].spot_id == spot_id:
                for j in range(i, self._size - 1):
                    self._spots[j] = self._spots[j + 1]
                self._spots[self._size - 1] = None
                self._size -= 1
                return True
        return False

    def get(self, index: int) -> Optional[ParkingSpot]:
        """Get a parking spot by index"""
        if 0 <= index < self._size:
            return self._spots[index]
        raise IndexError(f"Index {index} is out of bounds for size {self._size}")

    def size(self) -> int:
        """Get current size of the array"""
        return self._size

    def _resize(self) -> None:
        """Resize array when full"""
        new_spots = [None] * (len(self._spots) * 2)
        for i in range(self._size):
            new_spots[i] = self._spots[i]
        self._spots = new_spots

class ParkingLotManager:
    """Manages parking operations using Python's built-in list"""
    def __init__(self):
        self.parking_spots: List[ParkingSpot] = []
        self.parking_records: List[ParkingRecord] = []

    def add_parking_spot(self, spot_id: str, spot_type: SpotType, base_rate: float) -> None:
        """Add a new parking spot"""
        self.parking_spots.append(ParkingSpot(spot_id, spot_type, base_rate))
        print(f"Added new {spot_type.value} parking spot {spot_id} with base rate ${base_rate}/hour")

    def find_available_spot(self, spot_type: SpotType) -> Optional[ParkingSpot]:
        """Find an available parking spot of the specified type"""
        for spot in self.parking_spots:
            if spot.type == spot_type and spot.available:
                return spot
        return None

    def park_vehicle(self, vehicle_id: str, spot_type: SpotType) -> ParkingRecord:
        """Park a vehicle in an available spot"""
        spot = self.find_available_spot(spot_type)
        if not spot:
            raise ValueError(f"No available parking spots of type: {spot_type}")
        
        spot.available = False
        record = ParkingRecord(vehicle_id, spot.spot_id, datetime.now())
        self.parking_records.append(record)
        print(f"Vehicle {vehicle_id} parked in {spot_type.value} spot {spot.spot_id}")
        return record

    def calculate_fee(self, record: ParkingRecord) -> float:
        """Calculate parking fee with dynamic pricing"""
        exit_time = datetime.now()
        duration = exit_time - record.entry_time
        hours = duration.total_seconds() / 3600
        hours = int(hours) + (1 if duration.total_seconds() % 3600 > 0 else 0)

        spot = next(spot for spot in self.parking_spots if spot.spot_id == record.spot_id)
        base_rate = spot.base_rate
        occupancy_rate = self._calculate_occupancy_rate(spot.type)

        time_factor = self._calculate_time_factor(record.entry_time)
        occupancy_factor = self._calculate_occupancy_factor(occupancy_rate)

        fee = base_rate * hours * time_factor * occupancy_factor
        
        print(f"\nParking Fee Breakdown for vehicle {record.vehicle_id}:")
        print(f"Duration: {hours} hours")
        print(f"Base rate: ${base_rate}/hour")
        print(f"Time factor: {time_factor}x (based on parking time)")
        print(f"Occupancy factor: {occupancy_factor}x (based on {occupancy_rate:.1%} occupancy)")
        print(f"Total fee: ${fee:.2f}")
        
        return fee

    def _calculate_time_factor(self, time: datetime) -> float:
        """Calculate time-based pricing factor"""
        hour = time.hour
        if 9 <= hour <= 17:
            return 1.5
        if hour >= 22 or hour <= 6:
            return 0.7
        return 1.0

    def _calculate_occupancy_factor(self, occupancy_rate: float) -> float:
        """Calculate occupancy-based pricing factor"""
        if occupancy_rate >= 0.8:
            return 1.5
        elif occupancy_rate >= 0.5:
            return 1.2
        return 1.0 

    def _calculate_occupancy_rate(self, spot_type: SpotType) -> float:
        """Calculate current occupancy rate for a specific spot type"""
        total_spots = sum(1 for spot in self.parking_spots if spot.type == spot_type)
        if total_spots == 0:
            return 0.0
        
        occupied_spots = sum(1 for spot in self.parking_spots 
                           if spot.type == spot_type and not spot.available)
        return occupied_spots / total_spots

    def display_status(self):
        """Display current status of the parking lot"""
        print("\nParking Lot Status:")
        print("------------------")
        for spot_type in SpotType:
            total = sum(1 for spot in self.parking_spots if spot.type == spot_type)
            available = sum(1 for spot in self.parking_spots 
                          if spot.type == spot_type and spot.available)
            if total > 0:
                print(f"{spot_type.value.capitalize()} spots: {available}/{total} available")

def main():
    manager = ParkingLotManager()
    
    print("Initializing Parking Lot Management System...")
    print("-------------------------------------------")
    manager.add_parking_spot("A1", SpotType.STANDARD, 10.0)
    manager.add_parking_spot("A2", SpotType.STANDARD, 10.0)
    manager.add_parking_spot("B1", SpotType.ELECTRIC, 15.0)
    manager.add_parking_spot("C1", SpotType.HANDICAP, 8.0)
    
    print("\nInitial status:")
    manager.display_status()
    
    try:
        print("\nSimulating parking operations:")
        record1 = manager.park_vehicle("CAR123", SpotType.STANDARD)
        record2 = manager.park_vehicle("TESLA1", SpotType.ELECTRIC)
        print("\nUpdated status:")
        manager.display_status()
        print("\nSimulating 2.5 hours passing...")
        record1.entry_time = datetime.now() - timedelta(hours=2, minutes=30)
        fee1 = manager.calculate_fee(record1)
        print("\nTrying to park another standard vehicle...")
        record3 = manager.park_vehicle("CAR456", SpotType.STANDARD)
        
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()