# CT0090

```bash
FLASK_APP=gateway/app flask run --host=0.0.0.0 --port=8080
FLASK_APP=news/app flask run --host=0.0.0.0 --port=1234
FLASK_APP=forecast/app flask run --host=0.0.0.0 --port=1235
```
## Register
You need to submit a **POST** request to `localhost:5000/api/v1/register` providing a JSON with the following structure:
```json
{
    "username": "username",
    "password": "password"
}
```
If the user is successfully created, you will receive a response with the following structure:
```json
{
    "access_token": "access-token"
}
```

## Login
In order to login you need to submit a **POST** request to `localhost:5000/api/v1/login` and inserting the access token in the header:
```bash
    "x-access-token": "access-token"
```
