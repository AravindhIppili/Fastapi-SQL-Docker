# Pizzeria

## Documentation

- The project uses Python 3.9.
- The backend is built on [FastApi](https://fastapi.tiangolo.com/). It is uses Uvicorn server, MySQL database and SQL Alchemy ORM.
- Async tasks to change the status of the order is done by [asyincio](https://docs.python.org/3/library/asyncio.html).
- I have used [wait-for-it.sh](https://github.com/vishnubob/wait-for-it/blob/master/wait-for-it.sh) to wait until mysql image is created.
- For logs use command

```bash
  docker logs fastapi-server -f
```

## Installation

Install this project with Docker

```bash
  docker-compose up -d
```

## Note:

- Before Installation check whether ports 3306 ( for mysql) and 8000 (for FastApi server) are free or not.
- Use different ports in docker-compose if they are not free.(Also remember to change the port in .env)
- It is preferred to stop and remove the container if any env variables are changed.

```bash
  docker-compose down
  docker rm <container-id>
  docker-compose up -d
```

## [Swagger](http://localhost:8000/docs)

There is swagger collection for the project.

- After starting the project open endpoint localhost:8000/docs for swagger UI.

## API Reference

#### Health Check

```http
  GET /
```

#### Create an Order

```http
  POST /api/v1/pizza/order
```

| Parameter    | Type    | Description                               |
| :----------- | :------ | :---------------------------------------- |
| `order_data` | `Order` | **Required**. Give complete order details |

#### Get Order Status

```http
  GET /api/v1/pizza/order/{order_id}
```

| Parameter  | Type     | Description                                             |
| :--------- | :------- | :------------------------------------------------------ |
| `order_id` | `string` | **Required**. Order ID to track the status of the order |

## Author

- [@aravindippili](https://www.github.com/AravindhIppili)
- [aravindhippili00@gmail.com](mailto:aravindhippili00@gmail.com)
