FROM python
WORKDIR /usr/src/app
COPY . .
EXPOSE 8000
CMD ["python", "-m", "pip", "install", "--upgrade", "pip"]
RUN pip install -r requirements.txt
CMD [ "python", "manage.py", "migrate" ]
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]