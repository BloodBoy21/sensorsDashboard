FROM python:3.12-alpine

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 3000

ENV PORT=3000

CMD ["python", "main.py"]
