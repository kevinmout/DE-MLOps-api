# DE-MLOps-api

## Commands

### Install FastAPI:

```

pip install fastapi[standard]
```

### Run

```
fastapi run app/main.py --port 4000
```

Set environment variables:

1. Please copy contents of .env.example.
2. Create a new file called .env
3. Check the url of your website.
4. Replace this in .env.

To run in docker:

```
docker build -t python-api .
```

```
docker run -d --name my-api -p 80:80 -e  MY_APP_URL=http://localhost:3000 python-api
```
