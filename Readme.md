# API Documentation

This document provides details about the APIs available in this application.

## Base URL

All API endpoints are relative to the base URL: `http://localhost:8000/api/`

## Authentication

For endpoints that require authentication, include a valid JWT token in the request headers:

```bash
Authorization: Bearer <your_token_here>
```


## Endpoints

### 1. Create User

- **URL**: `/createuser`
- **Method**: POST
- **Data**:
  ```json
  {
    "username": "Prashant",
    "email": "prashant@gmail.com",
    "password": "password"
  }


OR

```json
        {
        "username": "Vishal",
        "email": "Vishal93@gmail.com",
        "password": "password",
        "referral_code": "Prashant_qdd6_magicpitch"
        }
```

---

### 2. Login User

- **URL**: `/login`
- **Method**: POST
- **Data**:

```json
    {
      "email": "prashant@gmail.com",
      "password": "password"
    }   
```

---


### 3. Get all User

- **URL**: `/getusers`
- **Method**: GET
- **Authorization**: Required
- **Description**: Retrieves all Users Information.

```link
curl -X GET http://localhost:8000/api/getusers -H "Authorization: Bearer <your_token_here>"
```

OR `if using thunderclient or Post man`
```bash 
http://localhost:8000/api/getusers
```
---

### 3. Get User by ID

- **URL**: `/getuser/<User ID>`
- **Method**: GET
- **Authorization**: Required
- **Description**: Retrieves Information of a perticular Person.

```bash
curl -X GET http://localhost:8000/api/getuser/<User ID> -H "Authorization: Bearer <your_token_here>"
```

OR `if using thunderclient or Post man`
```bash 
http://localhost:8000/api/getusersbyid/<User ID>
```
---

### 4. Get User Referrals

- **URL**: `/referrals`
- **Method**: GET
- **Authorization**: Required
- **Description**: Retrieves referrals for the authenticated user.

```bash
curl -X GET http://localhost:8000/api/referrals -H "Authorization: Bearer <your_token_here>"
```

OR `if using thunderclient or Post man`
```bash 
http://localhost:8000/api/referrals
```

---
## Error Handling

- **400 Bad Request**: Invalid request format or missing required parameters.
- **401 Unauthorized**: Missing or invalid authentication token.
- **404 Not Found**: Resource not found.
- **500 Internal Server Error**: Server encountered an unexpected condition.

--

