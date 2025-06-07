# Epocha

A futuristic, theoretical framework for a data storage system that expands capacity by sending and retrieving information through controlled points in time.

### Concept

Imagine a computer with the ability to store data, recieve messages, and send messages to addresses at any point in the future. This framework would allow the computer to extend it's memory beyond it's actual physical storage capacity. 

Say the computer has a 64 bit integer in memory called x and it wants to store another 64 bit interger y. However, it has no more available memory. The protocol would go as follows: 

- Send a message to its own address containing x at some point in the future (say 1 minute)
- Erase x from it's memory and store y
- Hold on to y for as long as it needs it (up to 1 minute)
- Send another message to itself 1 minute in the future containing y
- Clear y from it's memory
- Receive the message containing x and store it in memory
- Repeat :repeat:

Obviously, this requires the ability to _literally_ send messages into the future, which, as of June 7th, 2025, does not exist. As a result, this project is purely a thought experiment. But maybe one day the technology will catch up and this will become a legitimate tool for data storage. Much like the delorean was invented before the flux capacitor. 😄

### Features

- Time-forward multiplexed data storage
- Error-correcting codes integrated for robustness
- Distributed consensus to handle noisy or missing data
- Priority-based data cycling for efficient storage management
- Modular design allowing prototyping in Python and optimization in lower-level languages

## Getting Started

### Prerequisites
- Python 3.x (for prototyping)
- [Optional] Rust or C/C++ compiler (for optimized modules)

### Installation

```
git clone https://github.com/JebBrown2003/Epocha.git
cd Epocha

# Install Python dependencies
pip install -r requirements.txt
```

### Usage

```
from Epocha import EpochaStorage

storage = EpochaStorage(slot_duration_ms=100)
storage.store(data=0b1101)
retrieved = storage.retrieve()
print(f"Retrieved data: {retrieved}")
```

## Architecture

- Time-forward messaging interface: Abstracts sending/receiving data points into/from the future
- Error correction module: Encodes/decodes data with ECC (e.g., Hamming, Reed-Solomon)
- Consensus layer: Coordinates multiple receivers for data validation
- Priority algorithm: Manages which data to send/store next to optimize space usage

## Contributing

Contributions are welcome! Please open issues or submit pull requests with clear descriptions.

## License

This project is licensed under the MIT License — see the LICENSE file for details.

## Contact

- Jeb Brown — will add later...
- Project Link: https://github.com/JebBrown2003/Epocha
