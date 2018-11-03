FROM python:3.6
EXPOSE 8000

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt
COPY . /app
ENV DATABASE_URL postgres://va-checker@db/va-checker
ENV SECRET_KEY ''
ENV DJANGO_ENV ''
RUN chmod +x bash/run-prod.sh
CMD bash/run-prod.sh