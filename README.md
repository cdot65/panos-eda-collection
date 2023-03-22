# Ansible EDA source plugin for PAN-OS firewalls

This project is an implementation of a FastAPI application that receives firewall log messages from a Palo Alto Networks PAN-OS device, embedded within an Ansible EDA source plugin.

## Project Setup

### Prerequisites

There are two methods to deploying, either locally with Poetry or through a Docker container. These docs will cover the Docker based installation:

- Python 3.6 or higher
- Python Poetry
- Docker or Podman (RHEL based machines only)

### Installation

1. Clone the repository from GitHub.
2. Create a virtual environment using the command `poetry install`.
3. Activate the virtual environment using the command `poetry shell`.

### Building the container image

Build the Docker image using the command `invoke build`; macOS users on Apple silicon can use the command `invoke build --arm`.

Run the container using the command `invoke local` (or `invoke local --arm` for Apple silicon).

### Usage

Once the FastAPI application is up and running, you can send a firewall log message to the `/endpoint/` endpoint using a POST request. The request should contain the firewall log message in JSON format.

```http
POST /endpoint/ HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
    "message": "Firewall decryption log message"
}
```

The FastAPI application will parse the message and send the interesting information to an Ansible playbook for execution.

### API Documentation

The FastAPI application uses the OpenAPI specification to document the API. The API documentation is available at the /docs endpoint when the application is running. You can also access the OpenAPI schema at the /openapi.json endpoint.
