from collections import deque
from hashlib import sha256

# EpochaStorage allows for storing and retrieving data with a portal mechanism to handle data in transit.
class EpochaStorage:
    
    # EpochaStorage is a simple storage system that allows for storing and retrieving data
    def __init__(self, portaling_method, portal_length_ms: int = 1000, capacity: int = 2):

        # portaling method is a function that handles the portaling of data
        self.portaling_method = portaling_method
        # length of portal in milliseconds
        self.portal_length_ms = portal_length_ms
        # physical storage is a deque
        self.storage = deque([])
        # capacity of physical storage
        self.capacity = capacity
        # current space usage of physical storage
        self.curr_usage = 0
        # addresses is a dictionary to map addresses to the state of the data
        # e.g. "in transit" or the actual data
        self.addresses = {}
    
    # Get the current data based on the address
    def retrieve(self, address: int) -> int:
        # Try to get the data from the addresses dictionary
        data = self.addresses.get(address, None)

        # If data is None, it means no data was found for the address
        # If data is "in transit", it means the data is currently being portaled
        # Otherwise, return the actual data
        if data is None:
            print(f"No data found for: (address: {address})")
            return None
        elif (data == "in transit"):
            print(f"Data currently in transit for: (address: {address})")
            return None
        else: 
            print(f"Retrieved: (data: {data}, address: {address})")
            return data

    # Store data in the storage, if full, portal the oldest data
    # Returns the address of the stored data
    def store(self, data: int) -> int:

        print(f"⬇️ Attempting to store: ({data})")

        # Generate a unique address for the data
        address = self._get_address(data)
        
        # If storage is full, portal the oldest data then store the new data
        # update the current usage amount
        if self.curr_usage == self.capacity:
            oldest = self.storage.popleft()
            old_addr, old_dat = next(iter(oldest.items()))
            print(f"🌀 Storage is full, portaling: (data: {old_dat}, address: {old_addr})")
            self.addresses[old_addr] = "in transit" # Mark the data as in transit
            self.portal(oldest)
        else:
            self.curr_usage += 1
        
        # Store the new data in storage
        print(f"📝 Stored: (data: {data}, address: {address})")
        self.storage.append({address: data})
        
        # Add the address, data pair to the addresses dictionary
        self.addresses[address] = data
        return address

    # Portal the data using the provided portaling method
    # kvpair is a dictionary with the address as the key and the data as the value
    def portal(self, kvpair: dict[str, int]):
        return self.portaling_method(kvpair, self.portal_length_ms)

    def delete(self, address: int):
        # Remove the address from the addresses dictionary
        if address in self.addresses:
            # Mark the address as deleted
            self.addresses[address] = "deleted"
            # Also remove the data from the storage if it exists
            for item in self.storage:
                if address in item.keys():
                    self.storage.remove(item)
                    self.curr_usage -= 1
                    break
            print(f"🗑️ Deleted data at: (address: {address})")
        else:
            print(f"❌ No data found to delete at: (address: {address})")

    # Print the current storage contents and usage
    # This is useful for debugging and monitoring the storage state
    def print_storage(self):
        print("💾 Current storage contents:")
        for item in self.storage:
            address, data = next(iter(item.items()))
            print(f"\t(Data: {data}, Address: {address})")
        print(f"\tCurrent space usage: {self.curr_usage}/{self.capacity}")

    # Uses SHA-256 hash of the data to create a unique address
    def _get_address(self, data: int) -> int:
        # Convert the data to bytes then hash it
        byte_data = data.to_bytes((data.bit_length() + 7) // 8 or 1, byteorder="big")
        return sha256(byte_data).hexdigest()