docker build -f Dockerfile -t speech-recog-ml-task:v1.0.0 .
docker run --rm --network host -p 5000:5000 --name=speech-recog-ml-task-t speech-recog-ml-task:v1.0.0