FROM python:3.8
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
RUN python setup.py install
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["./nomadapp_back/flask_api.py"]
