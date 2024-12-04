FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80
CMD ["gunicorn", "-b", "0.0.0.0:80", "app:app"]