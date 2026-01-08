## Description
This repository contains the completed homework assignment based on the **Core Project “Personal Assistant”**.  
The main goal of the assignment is to properly configure the project environment using a dependency management tool and to containerize the application using Docker.

The project demonstrates:
- creation of an isolated virtual environment with a fixed Python version,
- dependency management with locked versions,
- running a CLI application inside a Docker container in interactive mode.

## Technologies
- Python
- pipenv - for virtual environment and dependency management
- Docker - for containerization
- CLI (Command Line Interface) application architecture

## Functionality
- Creation of a virtual environment using **pipenv**
- Explicit specification of the Python version in the Pipfile
- Installation and locking of all required project dependencies
- Configuration of the development environment to use the created virtual environment
- Dockerfile that:
  - uses an appropriate base Python image,
  - copies the application source code into the container,
  - installs all dependencies,
  - runs the Personal Assistant CLI application as the main container process

## Links
- **GitHub Repository:**  
  https://github.com/OAtamanchuk/goit-ds-hw-01
