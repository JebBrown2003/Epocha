class EpochaStorage:
    
    def __init__(self, slot_duration_ms=100):
        self.slot_duration_ms = slot_duration_ms
        self.storage = {}
    
    def store(self, data: int):
        slot = self._get_current_slot()
        self.storage[slot] = data
        print(f"Storing data in slot {slot}: {data}")
    
    def retrieve(self):
        slot = self._get_current_slot()
        data = self.storage.get(slot)

        if data is None:
            print(f"No data found for slot {slot}")
            return None
        else:
            print(f"Retrieving data from slot {slot}: {data}")
            return data

    def _get_current_slot(self):
        return 0