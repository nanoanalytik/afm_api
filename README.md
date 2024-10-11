
# AFM Control API Documentation

Welcome to the **AFM Control by nano analytik GmbH API repository**! This repository provides comprehensive documentation and example source code to help you integrate with our AFM system using our API.

## Overview

Our AFM API allows developers and researchers to integrate external applications with the Atomic Force Microscope, enabling access to real-time data, control over the microscope functions, and automated measurement processes. The API supports communication through HTTP/REST protocols, making it easy to integrate with a wide range of systems.

## Key Features

- **Real-time data access**: Obtain high-precision measurement data from the AFM in real time.
- **Instrument control**: Perform actions such as starting and stopping scans, controlling probe positioning, and adjusting scan parameters.
- **Extensibility**: The API is designed to be flexible, allowing integration with custom applications or software systems used in atomic-scale research.

## Getting Started

### Requirements

Before using the API, ensure you have the following:

- nano analytik AFM system compatible with the API.
- Authentication credentials (API key) provided by your system administrator.
- An internet connection to access the AFM system over the network.

### API Documentation

The complete API documentation is available [docs/API.md](./docs/API.md). It includes detailed information about all available endpoints, request/response formats, and example usage.

### Example Code

We have provided example code in various programming languages to demonstrate how to interact with the API. You can find these examples in the `examples/` directory.

Examples include languages:

- Python
- .NET/C#

Check the [examples/README.md](./examples/README.md) for more details on how to run each example.

**Note:** These examples are simplified to highlight API usage and may not include comprehensive error handling, input validation, or user interface components necessary for production applications.