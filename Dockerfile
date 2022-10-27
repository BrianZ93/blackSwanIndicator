FROM python:3.10.3

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "./main.py", "./vix.py"]