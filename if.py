from collections import deque

class PharmacyInventory:
    def _init_(self):
        self.available_medications = []
        self.prescription_queue = deque()
        self.undo_stack = []

    def add_medication(self, medication):
        self.available_medications.append(medication)
        print(f"Medication '{medication}' added.")

    def remove_medication(self, medication):
        if medication in self.available_medications:
            self.available_medications.remove(medication)
            print(f"Medication '{medication}' removed.")
        else:
            print(f"Medication '{medication}' not found.")

    def process_prescription(self, prescription):
        if prescription in self.available_medications:
            self.prescription_queue.append(prescription)
            self.undo_stack.append(prescription)  # Store in undo stack
            print(f"Prescription '{prescription}' processed.")
        else:
            print(f"Medication '{prescription}' not available.")

    def undo_last_prescription(self):
        if self.undo_stack:
            last_prescription = self.undo_stack.pop()
            self.prescription_queue.remove(last_prescription)
            print(f"Undo last prescription: '{last_prescription}'")
        else:
            print("No prescriptions to undo.")

    def show_available_medications(self):
        print("Available Medications:")
        for med in self.available_medications:
            print(med)

    def show_processing_queue(self):
        print("Processing Queue:")
        for prescription in self.prescription_queue:
            print(prescription)

# Example usage
pharmacy = PharmacyInventory()
pharmacy.add_medication("Aspirin")
pharmacy.add_medication("Ibuprofen")
pharmacy.show_available_medications()

pharmacy.process_prescription("Aspirin")
pharmacy.show_processing_queue()

pharmacy.undo_last_prescription()
pharmacy.show_processing_queue()