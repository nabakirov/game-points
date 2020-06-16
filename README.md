# game-points

To change user points create transaction
to raise points use *add* transaction type
to exchange points use *exchange* transaction type

## Environment variables
* SECRET_KEY=secret
* DEBUG=True/False
* DATABASE_URL=sqlite:///secret/db.sqlite
* ALLOWED_HOSTS=*
* RESOURCES_DIR=resources/

## Authorization
You will be given access and refresh tokens from login or signup API
You have to submit access token in headers of request   
```Authorization: Bearer <access token>```   
access token lives short time, but can be refreshed by refresh token   

## Pagination
to control pagination use query params
```
?limit=100&offset=400
```
paginated response will look like
```json5
{
  "count": "int",            // count of all elements
  "next": "str or null",     // url for next "page"   
  "previous": "str or null", // url for previous "page"   
  "results":[]               // data
}
```

## Models
### user
```json5
{
  "id": "int",            
  "username": "str",         
  "photo": "str",       // nullable, url
  "date_joined": "str", // timestamp
  "interests": "str",   // nullable
  "points": "str",      // decimal
}
```
### transaction
```json5
{
  "id": "int",
  "user": "int",
  "type": "str",        // add, exchange
  "value": "str",       // decimal
  "date": "str",        // timestamp
  "description": "str"  // nullable
}
```
### detailed transaction
```json5
{
  "id": "int",
  "user": "user",
  "type": "str",        // add, exchange
  "value": "str",       // decimal
  "date": "str",        // timestamp
  "description": "str"  // nullable
}
```
[user](#user)

## API
### POST */user/v1/signup/*
signup
#### access - *public*
request
```json5
{
  "username": "str",      // required, firebase access token
  "password": "str",      // required
  "interests": "str",     // optional,
  "photo": "bytes"        // optional
}
```
response
```json5
{
  "access": "str",
  "refresh": "str",
  "user": "user"
}
```
[user](#user)

### POST */user/v1/login/*
login
#### access - *public*
request
```json5
{
  "username": "str",      // required, firebase access token
  "password": "str",      // required
}
```
response
```json5
{
  "access": "str",
  "refresh": "str",
  "user": "user"
}
```
[user](#user)

### POST */auth/v1/refresh/*
refresh access token
#### access - **public**
```json5
{
  "refresh": "str",   // required
}
```
response
```json5
{
  "access": "str"
}
```

### GET */user/v1/profile/*
get profile
#### access - *authorized*
[response](#user)

### PATCH/PUT */user/v1/profile/*
update profile
#### access - *authorized*
request
```json5
{
  "username": "str",
  "interests": "str",
  "photo": "bytes"
}
```
[response](#user)

### DELETE */user/v1/profile/*
delete profile
#### access - *authorized*
response - status code 204

### POST */user/v1/profile/password/*
update password
#### access - *authorized*
request
```json5
{
	"old_password": "str",
	"new_password": "str"
}
```
response status code 200

### GET */user/v1/users/*
list of users
#### access - *authorized*
paginated response
```json5
{
  // pagination data
  "result": [
    "user",
  ]
}
```
[user](#user)

### GET */user/v1/users/<id>/*
get user by id
#### access - *authorized*
[response](#user)

### GET */point/v1/transactions/*
list of transaction related to user
#### access - *authorized*
paginated response
```json5
{
  // pagination data
  "result": [
    "transaction"
  ]
}
```
[transaction](#transaction)

### GET */point/v1/transactions/<id>/*
detailed transaction related to user
#### access - *authorized*
[response](#detailed-transaction)

### POST */point/v1/transactions/*
create transaction
#### access - *authorized*
request
```json5
{
	"type": "str",      // add, exchange
	"value": "int",     // positive decimal
    "description": "str" // nullable
}
```
response
```json5
{
  "id": "int",
  "type": "str",
  "value": "str",
  "date": "str",
  "description": "str"
}
```
