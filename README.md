# Micro-Blog
Simple blog based on microservices architecture and realized on python django-rest-framework

For starting service in <b>Docker</b> you should make folowing steps:
1. <b>Change directory</b> to the root directory of the service:
```
cd LikeService/
```

2. <b>Build</b> docker image from <b>Dockerfile</b>
  ```
  docker build -t <like|post|comment>-service .
  ```
  
3. <b>Run container</b> from image
  ```
  docker run -p <port>:8000 <like|post|comment>-service
  ```
  
Then go to your browser, open ```0.0.0.0:<port>```

So you can create/read/update/delete likes|comments|posts

https://www.djangoproject.com/

https://www.django-rest-framework.org/
