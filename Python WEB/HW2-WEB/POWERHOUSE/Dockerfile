FROM python:3.11.6
ENV POETRY-MTH /main
WORKDIR $POWERHOUSE
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python", "powerhouse_assistant//main.py"]