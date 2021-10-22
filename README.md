# test-task-backend


#Docker 

##build image

docker build -t test-task/backend:latest .

##create container on port 5000
docker run -d -p 5000:5000   --name test-task-backend test-task/backend