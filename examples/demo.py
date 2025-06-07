import time
import json
import python_epocha


# --- Portaling method: write to a text file with a timestamp ---
def mock_portaling_to_file(kvpair: dict[str, int], delay_ms: int, filename="examples/portaled_data.txt"):

    # Upload the data to a text file with a future release time
    # data should not be read until the release time
    address, data = next(iter(kvpair.items()))
    payload = {
        "address": address,
        "data": data,
        "release_time": time.time() + (delay_ms / 1000)
    }
    # Append the payload to the file specified by filename
    with open(filename, "a") as f:
        f.write(json.dumps(payload) + "\n")
    print(f"🚀 Portaled: (data: {data}, (address: {address}) for {delay_ms}ms into the future.")


# --- Retrieval method: read from text file and insert back into storage if ready ---
def retrieve_from_portal(storage: python_epocha.EpochaStorage, filename="portaled_data.txt"):

    # Open the portaled data file and read lines
    print("🔍 Listening for portaled data...")
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"⚠️ {filename} not found.")
        return

    # For manually checking if data is ready to be retrieved
    now = time.time()
    remaining_lines = []

    for line in lines:
        payload = json.loads(line)

        # Manually check if the data is ready to be retrieved
        if now >= payload["release_time"]:

            # Check if the address has been deleted
            if storage.addresses.get(payload["address"]) == "deleted":
                print(f"❌ data at: (Address: {payload['address']}) has been deleted, skipping.")
                continue

            address = payload["address"]
            data = payload["data"]
            print(f"✅ Received data from portal: (data: {data}, address: {address})")
            # Store the data back into the storage
            # This should store the data back at the same address
            # This might also trigger the next portal if storage is full
            storage.store(data)
        else:
            remaining_lines.append(line) # Keep lines not ready for retrieval to write back to file later

    # Overwrite file with lines not ready for retrieval
    with open(filename, "w") as f:
        f.writelines(remaining_lines)


# --- Main demo sequence ---
if __name__ == "__main__":
    storage = python_epocha.EpochaStorage(
        portaling_method=mock_portaling_to_file,
        portal_length_ms=2000,
        capacity=2
    )

    # Store 3 items; one will be portaled
    # print contents of storage after each operation
    print("📦 Storing items in EpochaStorage...")
    a1 = storage.store(42)
    storage.print_storage()
    a2 = storage.store(99)
    storage.print_storage()
    a3 = storage.store(7)  # Should triggers portal of first entry (42)
    storage.print_storage()

    # Try retrieving from future
    # This will not work immediately since the data is portaled
    retrieve_from_portal(storage)

    print("\n⌛ Waiting 2.5 seconds for portaled data to become available...\n")
    time.sleep(2.5)

    # Try retrieving from future
    # This will store the portaled data back into storage
    #   and send the next data to the portal
    retrieve_from_portal(storage)
    storage.print_storage()

    # Delete the first address (42)
    print(f"\nAttempting to delete data at: (address: {a2}) while in the portal...")
    storage.delete(a2)

    print("\n⌛ Waiting 2.5 seconds for deleted portaled data to become available...\n")
    time.sleep(2.5)

    # Try retrieving from future again
    # This should not retrieve the deleted data
    retrieve_from_portal(storage)

    # Retrieve all addresses
    print("Retrieving all addresses:")
    storage.retrieve(a1)
    storage.retrieve(a2)
    storage.retrieve(a3)
