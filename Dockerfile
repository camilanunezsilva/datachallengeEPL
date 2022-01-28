FROM python:3.9.6
ENV APP_DIR /
WORKDIR $APP_DIR
COPY . $APP_DIR
RUN pip3 install -r requirements.txt

CMD [ "python3", "src/main.py" ]
