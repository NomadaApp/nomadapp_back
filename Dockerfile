FROM python:3.8
ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
RUN python setup.py install
ENV PORT 5000
# EXPOSE ${PORT}
# WORKDIR $APP_HOME/nomadapp_back
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 nomadapp_back/flask_api:app
# CMD exec python flask_api.py
