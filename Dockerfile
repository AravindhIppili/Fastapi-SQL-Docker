FROM python:3.9

WORKDIR /app

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install

COPY ./ /app

RUN chmod +x /app/wait-for-it.sh

EXPOSE 8000
 
CMD ["./wait-for-it.sh", "mysql:3306", "-t", "20", "--", "pipenv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
