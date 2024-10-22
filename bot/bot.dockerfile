FROM python:3.12
WORKDIR /usr/src/app
COPY requirements.txt ./
COPY service_acc_keys.json ./
RUN pip install --no-cache-dir -r requirements.txt
ADD ./ ./
CMD [ "python", "./bot.py" ]