# voucher.io

A small application to retrieve available parking vouchers for Leuven.

## Features

- Retrieve a list of parking vouchers usable for SMS parking in Leuven
- Filter vouchers by duration and usage
- Mark vouchers as used so they cannot be selected again
- Web interface for easy voucher lookup and management
- REST API for programmatic access

---

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
- [Python REST API](#python-rest-api)
  - [API Endpoints](#api-endpoints)
- [Web App (JavaScript)](#web-app-javascript)
- [Development](#development)
- [License](#license)

---

## Overview

**voucher.io** consists of:
- A Python-based REST API backend for managing parking vouchers in Leuven.
- A JavaScript-based web application frontend for searching and using vouchers.

---

## Getting Started

### Requirements

- Python 3.10+
- Node.js (for development on the frontend, if needed)
- (Optional) `pipenv` or `venv` for Python virtual environment

### Install & Run

1. **Clone the repository:**

   ```sh
   git clone https://github.com/Skoystah/voucher.io.git
   cd voucher.io
   ```

2. **Install Python dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

3. **Run the server:**

   ```sh
   cd src
   python main.py
   ```

   By default, the API is available at `http://localhost:8000`.

4. **Open the web app:**

   Simply open `app/index.html` in your browser. It will connect to the backend API.

---

## Python REST API

The backend REST API provides endpoints to manage and query parking vouchers.

### API Endpoints

| Method | Endpoint                     | Description                                 | Example Body / Query          |
|--------|------------------------------|---------------------------------------------|-------------------------------|
| GET    | `/vouchers`                  | List all vouchers                           | `?duration=1h&includeUsed=false` |
| POST   | `/vouchers`                  | Add a new voucher                           | `{"code": "LEU123", "duration": "1h"}` |
| PUT    | `/vouchers/{code}`           | Mark voucher as used                        | None                          |

#### Request & Response Examples

- **GET /vouchers**

  Returns a list of vouchers. Optional query parameters:
    - `duration`: Filter by duration (`1h`, `2h`, `4h`, etc.)
    - `includeUsed`: Include vouchers that have already been used (`true` or `false`)

  ```json
  [
    {
      "code": "LEU123",
      "duration": "1h",
      "used": false
    },
    {
      "code": "LEU456",
      "duration": "2h",
      "used": true
    }
  ]
  ```

- **POST /vouchers**

  Add a new voucher.

  Request Body:

  ```json
  {
    "code": "LEU789",
    "duration": "4h"
  }
  ```

  Response:

  ```json
  {
    "code": "LEU789",
    "duration": "4h",
    "used": false
  }
  ```

- **PUT /vouchers/{code}**

  Mark a voucher as used.

  On success: HTTP 200 OK.

#### CORS

CORS headers are enabled for all API endpoints.

---

## Web App (JavaScript)

The frontend is a simple JavaScript single-page app found in `/app`:

- **index.html**: Main HTML page.
- **scripts/main.js**: Contains logic to fetch vouchers from the API, filter results, and mark vouchers as used.
- **css/style.css**: Basic styling.

### Usage

- Open `app/index.html` in your browser.
- Use the form to search for vouchers (by duration, or include used).
- Click "Use voucher" to mark a voucher as used.

#### Example JavaScript usage

The frontend interacts with the REST API using `fetch`, e.g.:

```javascript
// Fetch vouchers
fetch('http://localhost:8000/vouchers?duration=1h')
  .then(res => res.json())
  .then(data => presentVouchers(data));

// Use a voucher
fetch('http://localhost:8000/vouchers/LEU123', { method: 'PUT' });
```

---

## Development

- Python server source code is in `/src`.
  - Entry point: `src/main.py`
  - REST API logic: `src/web/handler.py`, `src/web/server.py`
  - Voucher DB logic: `src/voucher/db.py`
- Frontend source is in `/app`.
  - HTML: `app/index.html`
  - JS: `app/scripts/main.js`
  - CSS: `app/css/style.css`
- Tests in `/tests`.

---

## License

Currently no license. Please contact the repository owner if you wish to use this code.

---

## Author

[Skoystah](https://github.com/Skoystah)

