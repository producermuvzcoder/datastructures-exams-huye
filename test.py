class PharmacyInventorySystem:
    def _init_(self):
        self.undo_stack = []
        self.prescription_queue = []
        self.available_medications = []
    def add_medication(self, medication):
        self.available_medications.append(medication)
    def remove_medication(self, medication):
        if medication in self.available_medications:
            self.available_medications.remove(medication)
    def add_prescription(self, prescription):
        self.prescription_queue.append(prescription)
        self.undo_stack.append(prescription)
    def process_prescription(self):
        if self.prescription_queue:
            return self.prescription_queue.pop(0)
        return None
    def undo_last_prescription(self):
        if self.undo_stack:
            last_prescription = self.undo_stack.pop()
            self.prescription_queue.remove(last_prescription)
    def get_available_medications(self):
        return self.available_medications
    def get_pending_prescriptions(self):
        return self.prescription_queue
pharmacy = PharmacyInventorySystem()
pharmacy.add_medication("Aspirin")
pharmacy.add_medication("Ibuprofen")
pharmacy.add_prescription("Prescription 1")
pharmacy.add_prescription("Prescription 2")
print(pharmacy.get_available_medications())
print(pharmacy.get_pending_prescriptions())
processed = pharmacy.process_prescription()
print(f"Processed: {processed}")
pharmacy.undo_last_prescription()
print(pharmacy.get_pending_prescriptions())