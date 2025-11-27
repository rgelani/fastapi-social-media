# FastAPI Social Media

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)  
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-green.svg)](https://fastapi.tiangolo.com/)  
[![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)](LICENSE)  
[![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)]()

A modern, scalable **social media backend** built with **FastAPI**, **Python**, and **PostgreSQL**. This project provides secure user authentication, post management, and social interactions via a RESTful API.

---

## Table of Contents

- [Features](#features)  
- [Tech Stack](#tech-stack)  
- [Getting Started](#getting-started)  
  - [Prerequisites](#prerequisites)  
  - [Installation](#installation)  
  - [Creating Virtual Environment](#creating-virtual-environment)  
  - [Running the Application](#running-the-application)    
- [License](#license)  

---

## Features

- Secure user registration, login, and JWT-based authentication  
- CRUD operations for posts  
- Like and unlike posts functionality  
- RESTful API with automatic **Swagger UI** documentation  
- Dockerized environment for easy setup and deployment  
- Modular and maintainable code structure  
- Environment-based configuration  

---

## Tech Stack

- **Backend Framework:** FastAPI  
- **Programming Language:** Python 3.9+  
- **Database:** PostgreSQL (via SQLAlchemy ORM)  
- **Data Validation:** Pydantic  
- **Authentication:** JWT / OAuth2  
- **Containerization:** Docker & Docker Compose  
- **Testing:** Pytest (optional)  

---

## Getting Started

### Prerequisites

- Python 3.9+  
- PostgreSQL (or SQLite for testing)  
- Docker & Docker Compose (optional)  

### Installation

Clone the repository:

```bash
  git clone https://github.com/rgelani/fastapi-social-media.git
  cd fastapi-social-media
```

### Creating virtual environment

Create a virtual environment and install dependencies

```bash

python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Running the Application

```
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.



