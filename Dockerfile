FROM python:3.8
COPY requirements.txt /

RUN python3 -m pip install --upgrade --force-reinstall pip
RUN pip install -r requirements.txt
RUN pip install Flask==1.1.2
RUN pip install gunicorn==20.1.0

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

CMD exec gunicorn app:app --timeout 3600 -b 0.0.0.0:5000 --workers=1