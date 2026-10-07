# Warehouse Ops API

A production-minded REST API for managing warehouse stock, built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**.

The system provides a clean HTTP interface for creating products, retrieving stock information, selling inventory, restocking products, and identifying items that have reached their low-stock threshold.

---

## Overview

Warehouse operations often involve simple-looking actions that require reliable backend behavior:

* What products exist?
* How much stock is currently available?
* Can an order be fulfilled?
* How much stock should be added after a delivery?
* Which products need attention because their stock is running low?

**Warehouse Ops API** provides these core operations through a RESTful API backed by PostgreSQL.

The project was built to practice backend engineering fundamentals including:

* REST API design
* FastAPI routing
* Request and response validation
* Dependency-based configuration
* SQLAlchemy ORM
* PostgreSQL persistence
* Database querying
* Business-rule validation
* HTTP error handling
* Environment-based configuration

---

## Features

### Product Management

* Create a warehouse item
* Retrieve an item by ID
* Persist item data in PostgreSQL
* Enforce unique SKUs

### Stock Operations

* Sell stock
* Prevent selling more units than are available
* Restock products
* Query products below their configured stock threshold

### Validation

Request data is validated using Pydantic.

Examples:

* Quantity cannot be negative when creating an item
* Low-stock thresholds cannot be negative
* Sell/restock quantities must be greater than zero

### Error Handling

The API returns appropriate HTTP errors for situations such as:

* Item not found
* Insufficient stock
* Invalid request data

---

## Tech Stack

| Technology | Purpose                      |
| ---------- | ---------------------------- |
| Python     | Application language         |
| FastAPI    | REST API framework           |
| Pydantic   | Request/response validation  |
| SQLAlchemy | ORM and database interaction |
| PostgreSQL | Relational database          |
| psycopg    | PostgreSQL driver            |
| Uvicorn    | ASGI server                  |

---

## Architecture

The application follows a simple layered flow:

```text
Client
   │
   ▼
FastAPI Route
   │
   ▼
Pydantic Schema
   │
   ▼
Business Logic
   │
   ▼
SQLAlchemy
   │
   ▼
PostgreSQL
   │
   ▼
Response Schema
```

The project intentionally avoids unnecessary abstraction layers. The focus is on understanding the actual request → application → database flow before introducing additional architectural complexity.

---

## Project Structure

```text
warehouse-ops-api/
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   └── routes/
│   │       └── routes.py
│   │
│   ├── core/
│   │   └── config.py
│   │
│   ├── db/
│   │   ├── database.py
│   │   └── models.py
│   │
│   └── schemas/
│       └── schemas.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Database Model

The application uses an `items` table:

```text
items
├── id
├── name
├── sku
├── quantity
└── low_stock_threshold
```

### Constraints

* `id` is the primary key
* `sku` must be unique
* `name` cannot be null
* `quantity` cannot be negative
* `low_stock_threshold` cannot be negative

Example:

```text
ID   Name          SKU       Quantity   Threshold
--------------------------------------------------
1    Keyboard      KEY001    50         10
2    Mouse         MOU001    5          10
3    Monitor       MON001    25         5
4    USB Cable     USB001    3          10
5    Laptop Stand  LST001    18         5
```

---

## API Endpoints

Base URL:

```text
/api/v1
```

### Health Check

```http
GET /api/v1/health
```

Returns:

```json
{
  "status": "ok"
}
```

---

### Create Item

```http
POST /api/v1/items
```

Example request:

```json
{
  "name": "Keyboard",
  "sku": "KEY001",
  "quantity": 50,
  "low_stock_threshold": 10
}
```

---

### Get Item

```http
GET /api/v1/items/{id}
```

Example:

```http
GET /api/v1/items/1
```

Returns the requested item or `404 Not Found` if it does not exist.

---

### Sell Item

```http
POST /api/v1/items/{id}/sell
```

Example request:

```json
{
  "quantity": 5
}
```

The operation reduces the item's available stock.

If the requested quantity exceeds the available stock, the API rejects the operation.

---

### Restock Item

```http
POST /api/v1/items/{id}/restock
```

Example request:

```json
{
  "quantity": 20
}
```

The operation increases the item's stock.

---

### Low-Stock Items

```http
GET /api/v1/items/low-stock
```

Returns all items where:

```text
quantity <= low_stock_threshold
```

---

## Running Locally

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd warehouse-ops-api
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure the database

Create a `.env` file:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/warehouse_ops
```

Make sure PostgreSQL is running and the `warehouse_ops` database exists.

### 5. Start the API

```powershell
python -m uvicorn app.main:app --reload
```

The API will be available locally.

---

## Interactive API Documentation

FastAPI automatically generates interactive documentation.

Open:

```text
/docs
```

You can use Swagger UI to send requests directly to the API and inspect responses.

Alternative documentation is available at:

```text
/redoc
```

---

## Example Workflow

A typical warehouse workflow might look like this:

```text
Create Item
     │
     ▼
Stock = 50
     │
     ▼
Sell 8
     │
     ▼
Stock = 42
     │
     ▼
Restock 20
     │
     ▼
Stock = 62
     │
     ▼
Query Low-Stock Items
```

This demonstrates the central responsibility of the API: maintaining and exposing the current state of warehouse stock.

---

## Design Decisions

### PostgreSQL Instead of In-Memory Storage

Stock data represents persistent business state, so it belongs in a relational database rather than application memory.

### SQLAlchemy ORM

SQLAlchemy provides the mapping between Python objects and relational database records while still allowing explicit SQL-style querying.

For example:

```python
select(Item).where(Item.id == id)
```

represents a database query rather than a normal Python comparison.

### Pydantic Validation

Validation happens at the API boundary before invalid request data reaches the business logic.

For example:

```python
quantity: int = Field(gt=0)
```

ensures that stock operations cannot request zero or negative quantities.

### Database Constraints

Important invariants are also enforced at the database level.

This creates an additional layer of protection rather than relying entirely on application code.

---

## What This Project Demonstrates

This project is intentionally small, but it covers several foundations required by larger backend systems:

```text
HTTP
 │
 ├── Routing
 ├── Request validation
 ├── Response serialization
 ├── HTTP errors
 │
 ▼
Application
 │
 ├── Business rules
 ├── State changes
 │
 ▼
ORM
 │
 ├── Models
 ├── Queries
 ├── Persistence
 │
 ▼
PostgreSQL
 │
 ├── Constraints
 ├── Transactions
 └── Persistent state
```

The goal was not to build a huge application. The goal was to understand the mechanics behind a real API and its interaction with a relational database.

---

## Future Improvements

Possible production-level extensions include:

* Database session dependency management
* Atomic stock updates and concurrency control
* Database migrations with Alembic
* Automated test suite
* Authentication and authorization
* Structured logging
* Docker and Docker Compose
* Pagination
* Stock movement history
* Audit logging
* Automated low-stock alerts
* Background jobs
* CI/CD

These are deliberately outside the scope of the initial implementation.

---

## Status

**Completed — Core API**

The project currently implements the complete core warehouse stock workflow with FastAPI and PostgreSQL.

Future improvements can extend the system toward a more production-oriented architecture without changing its core purpose.
