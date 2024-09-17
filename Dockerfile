FROM python:3.10-slim


RUN apt-get update && \
    apt-get install -y gcc g++ make && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*



# Устанавливаем pip (если он не был убстановлен)
# Это обычно необязательно, если вы используете официальный образ Python
RUN python3 -m ensurepip --upgrade


WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "ml-pipeline.py" ]