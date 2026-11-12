FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY static ./static

RUN useradd --no-create-home --shell /usr/sbin/nologin ctf
USER ctf

ENV PORT=5000
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request,os;urllib.request.urlopen('http://127.0.0.1:'+os.environ.get('PORT','5000')+'/health')"
CMD ["sh", "-c", "gunicorn -b 0.0.0.0:${PORT} -w 2 app:app"]
