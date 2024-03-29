FROM python:3.12-alpine

# Создаем директорию для кода приложения
RUN mkdir /app

# Устанавливаем рабочую директорию в /app
WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

# Копируем текущий каталог в /app/ внутри контейнера
COPY . /app/
# Порт, к которому будет привязан контейнер
EXPOSE 8000

# Команда для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
