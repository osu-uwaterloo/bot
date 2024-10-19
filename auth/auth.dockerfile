FROM python:3.12
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY config.py app.py ./
CMD ["uvicorn", "app:app", "--reload", "--host", "0.0.0.0"]