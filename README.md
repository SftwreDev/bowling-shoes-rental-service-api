# Bowling Shoes Rental Service with LLM Integration and Prompt Engineering

A RESTful API designed to streamline the rental of bowling shoes. This service incorporates advanced features for user management, shoe inventory tracking, and rental transactions, enhanced by LLM integration to improve user interactions and provide dynamic responses through prompt engineering.

---

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Design Choices](#design-choices)

---

## Installation

### Prerequisites
Before you begin, ensure you have the following software installed:
- **Docker**: To run the application in a containerized environment.

### Setup Instructions
Follow these steps to set up the API on your local machine:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/SftwreDev/bowling-shoes-rental-service-api.git
   cd bowling-shoes-rental-service-api
   ```

2. **Configure Environment Variables**
   Create a `.env` file in the root directory and populate it with the following variables:
   ```plaintext
   SUPABASE_PROJECT_URL=your_supabase_project_url
   SUPABASE_API_KEY=your_supabase_api_key
   OPENAI_API_KEY=your_openai_api_key
   OPENAI_GPT_MODEL=gpt-3.5-turbo
   ```

3. **Run Docker Compose**
   Use Docker Compose to build and start the application:
   ```bash
   docker compose up --build
   ```

4. **Access Swagger Documentation**
   Once the application is running, you can access the API documentation at:
   [http://localhost:9000/api/v1/docs#/](http://localhost:9000/api/v1/docs#/)

---

## Usage

After setting up and running the API, you can use the following endpoints to interact with the service:

### Example Request
To view all available customers:
```plaintext
GET /api/v1/customers
```

### Example Response
```json
[
  {
    "id": 1,
    "created_at": "2024-10-27T12:34:56Z",
    "name": "John Doe",
    "age": 30,
    "contact_info": [
      {
        "contact_number": "123-456-7890",
        "email_address": "john@example.com",
        "address": "123 Bowling Lane"
      }
    ],
    "is_disabled": false,
    "medical_conditions": []
  },
  {
    "id": 2,
    "created_at": "2024-10-26T12:34:56Z",
    "name": "Jane Smith",
    "age": 25,
    "contact_info": [
      {
        "contact_number": "098-765-4321",
        "email_address": "jane@example.com",
        "address": "456 Bowling Ave"
      }
    ],
    "is_disabled": true,
    "medical_conditions": ["Asthma"]
  }
]
```

---

## API Documentation

### User Endpoints
- **POST /api/v1/customers**: Register a new customer.
  - **Request Body**: 
    ```json
    {
      "name": "string",
      "age": "integer",
      "contact_info": [
        {
          "contact_number": "string",
          "email_address": "string",
          "address": "string"
        }
      ],
      "is_disabled": "boolean",
      "medical_conditions": ["string"]
    }
    ```
- **GET /api/v1/customers**: Retrieve a list of all customers.

### Rental Endpoints
- **POST /api/v1/customer/rentals/**: Create a new rental entry for a customer.
  - **Request Body**:
    ```json
    {
      "customer_id": "integer",
      "shoe_size": "integer",
      "rental_fee": "float"
    }
    ```
- **GET /api/v1/customer/rentals/**: Retrieve a list of all customer rentals.

---

## Design Choices

### Architecture
The API follows a RESTful architecture, providing clear and structured endpoints to ensure a logical flow for resource management.

### Database
The project utilizes **Supabase** as its database solution, offering scalability and real-time capabilities for managing customer and rental data.

---
