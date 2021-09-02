FROM python:3.8

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN python -m pip install -r requirements.txt
#RUN pip install -U numpy
# Expose port 5000
EXPOSE 8080
ENV PORT 8080

CMD python index.py
