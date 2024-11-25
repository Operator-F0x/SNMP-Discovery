# SNMP Discovery Script

This Python script uses SNMP (Simple Network Management Protocol) to discover devices on a network. It queries network devices for information and displays the results.

## Features

- Discovers devices on the network using SNMP
- Retrieves and displays device information
- Supports SNMPv1, SNMPv2c, and SNMPv3

## Requirements

- Python 3.x
- `pysnmp` library

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/KaSaNaa/SNMP-Discovery-Script.git
    ```

2. Navigate to the project directory:

    ```sh
    cd SNMP-Discovery-Script
    ```

3. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Edit the `config.json` file to include your SNMP community strings and network details.
2. Run the script:

    ```sh
    python snmp_discovery.py
    ```

## Configuration

The `config.json` file should contain the following information:

```json
{
    "community": "public",
    "version": "2c",
    "network": "192.168.1.0/24"
}
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
