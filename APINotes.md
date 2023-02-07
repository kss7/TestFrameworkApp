# Simple Users API

This API allows us to work with users DB.

## Endpoints

- [Status](#Status)
- [Register](#Register)
- [Login](#Login)
- [Allusercount](#Allusercount)
- [Users](#Users)
- [User](#Get Specific user)
- [Delete](#Delete an user)


## Status

**`GET /api`**

Returns 401 status, with message as below.
Use it to check status if the API server is running.

Example response:
```
{
  "message": "Unauthorized access, please login"
}
```

This indicates that the API is running as expected.
No response or any other response indicates that the API is not running.


## Register
Some endpoints require authentication. You need a registered user to obtain an access token.

The endpoints that require authentication expects a bearer token sent in the `x-access-token` header.

For Example: `x-access-token: TOKEN`

The Register API will register/add an user to the system.
The request body needs to be in JSON format.

**`POST /api/register`**

Sample Request:
```
{
"email": "userx@userx",
"password":"1234"
}
```
**Headers**

| Name           | value            | 
|----------------|------------------|
| `Content-Type` | application/json |


**Parameters**

| Name        | Type    | In   | Required | Description            |
|-------------|---------|------|----------|------------------------|
| `email`     | string  | body | Yes      | Email ID               |
| `password`  | string  | body | Yes      | Password               |


**Status codes**

| Status code     | Description                      |
|-----------------|----------------------------------|
| 201 OK          | Indicates a successful response. |
| 422 Bad Request | Indicates existing email.        |

Example response:

```
{
    "email": "userx@userx",
    "id": "4"
}
```

## Login

**`POST /api/login`**

Login API to get the bearer token.
The request body needs to be in JSON format.

The response body will contain the access token.

Sample Request:
```
{
"email": "admin@admin",
"password":"1234"
}
```
**Headers**

| Name           | value            | 
|----------------|------------------|
| `Content-Type` | application/json |


**Parameters**

| Name        | Type    | In   | Required | Description            |
|-------------|---------|------|----------|------------------------|
| `email`     | string  | body | Yes      | Email ID               |
| `password`  | string  | body | Yes      | Password               |

**Status codes**

| Status code   | Description                                    |
|---------------|------------------------------------------------|
| 200 OK        | Indicates a successful response.               |
| 401 Not found | Indicates Username or Password doesn't exists. |

Example Response:
````
{
    "msg": "admin@admin logged in",
    "status": 200,
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9....",
    "userId": "1"
}
````

## Allusercount

Returns the count of all users in the system.

**`GET /api/allusercount`**

**Headers**

| Name     | value            | 
|----------|------------------|
| `Accept` | application/json |

**Parameters**

No parameters are accepted for this request.

**Status codes**

| Status code        | Description                                |
|--------------------|--------------------------------------------|
| 200 OK             | Indicates a successful response.           |
| 406 Not Acceptable | Indicates wrong header "Accept".           |
| 404 Not Found      | Request with wrong URL, or "/" in the end. |

Example Response:
````
{
  "count": 3,
  "status": {
    "message": "success",
    "status": 200
  }
}
````

## Users

Get all users in the system.
And get specific user with ID.
Requires token

**`GET /api/users`**
**`GET /api/users?id=1`**

**Headers**

| Name             | value                                         | 
|------------------|-----------------------------------------------|
| `x-access-token` | access token from a successful login response |

**Parameters**

| Name       | Type   | In    | Required | Description |
|------------|--------|-------|----------|-------------|
| `id`       | int    | query | No       | User Id     |


**Status codes**

| Status code | Description           |
|-------------|-----------------------|
| 200 Ok      | successful response.  |

Example response:

```
{
    "email": "admin@admin",
    "id": "1"
}
```

## Get Specific user

Get user with ID.

**`GET /api/user/:Id`**

**Headers**

| Name             | value                                         | 
|------------------|-----------------------------------------------|
| `x-access-token` | access token from a successful login response |

**Parameters**

| Name    | Type    | In   | Required | Description            |
| --------|---------| ---- | -------- |------------------------|
| `Id`    | int     | path | Yes      | Specifies the user id. |

**Status codes**

| Status code            | Description                |
|------------------------|----------------------------|
| 200 Ok                 | successful response.       |
| 404 Not Found          | User Id not exists.        |
| 500 ERROR              | Token expired/invalid.     |
| 405 Method Not allowed | Request with wrong method. |
| 401 Unauthorized       | Token missing.             |

Example response:

```
{
    "email": "admin@admin",
    "id": "1"
}
```


### Delete an user

Deletes a user from the system.

**`DELETE /api/delete`**

Sample Request:
```
{
"id": 4
}
```

**Headers**

| Name             | value                                         | 
|------------------|-----------------------------------------------|
| `x-access-token` | access token from a successful login response |

**Parameters**

| Name     | Type   | In   | Required | Description                |
|----------|--------|------| -------- |----------------------------|
| `Id`     | int    | body | Yes      | Specifies the id to delte. |

**Status codes**

| Status code      | Description                             |
|------------------|-----------------------------------------|
| 200 Ok           | The user has been deleted successfully. |
| 404 Not found    | The user is not available               |
| 401 UNAUTHORIZED | Token missing                           |
| 500 ERROR        | Token is expired/invalid                |

Example Response:
````
{
    "email": "userx@userx",
    "id": "4"
}
````