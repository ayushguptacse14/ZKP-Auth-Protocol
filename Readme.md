# Zero-Knowledge Proof Authentication System

This project demonstrates a secure authentication system using zero-knowledge proofs implemented through a gRPC-based client-server architecture. The server offers user registration, authentication challenge creation, and verification  to ensure privacy and security during authentication.

## Table of Contents

- [Project Overview](#project-overview)
- [Server](#server)
- [Client](#client)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Server](#running-the-server)
  - [Running the Client](#running-the-client)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

The project consists of two main components: the server and the client.

### Server

The server provides the authentication service through gRPC, offering the following functionalities:
- User registration with unique usernames and private values 'x'.
- Creation of authentication challenges with random 'c' values for users.
- Verification of authentication responses.

### Client

The client interacts with the server to facilitate user registration and authentication:
- Users can register with unique usernames and private values 'x'.
- Users can log in by responding to authentication challenges using calculated responses 's'.

## Getting Started

Follow these steps to set up and run the server and client components of the project.

### Prerequisites

- Python 3.6 or higher
- gRPC (Python library)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/zkp-authentication-project.git
   cd zkp-authentication-project
   ```

2. Install gRPC (if not already installed):
   ```bash
   pip install grpcio grpcio-tools
   ```

### Running the Server

1. Run the server:
   ```bash
   python server.py
   ```

   Or 
   
2. Run docker container
   ```bash
   docker-compose up --build
   ```

### Running the Client

1. Open a new terminal window.

2. Run the client script:
   ```bash
   python client.py
   ```

## Running Tests

Unit tests are provided in the `test.py` file. To run the tests, follow these steps:

1. Open a terminal window.

2. Navigate to the project root directory:
   ```bash
   python test.py
   ```

## Usage

1. Register: Choose option 1, enter a username and private value 'x', and the user will be registered.
2. Login: Choose option 2, enter the registered username and the corresponding private value 'x', and the user's authentication status will be displayed.
3. Exit: Choose option 3 to exit the client.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for any improvements, bug fixes, or new features you'd like to contribute.

## License

This project is licensed under the [MIT License](LICENSE).


