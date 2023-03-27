FROM python:3.10.10
ENV POETRY-MTH /main
WORKDIR $POWERHOUSE
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python", "powerhouse_assistant//main.py"]