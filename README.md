# MachineLearningProject1
# Used Command 
```
1. 
```
```
2. python -m venv env
```
```
3. ls
```
```
4. cd foldename
```
```
5. code . (open vs code using cmd)
```
```
6. use miro whiteboard
```





# git command 
```
1. git clone link
```
```
2. git add .
```
```
3. git push origin main
```
```
4. git --version
```
```
5. git pull
```
```
6. conda create -p venv python==3.7 -y  /python -m venv venv 
```
``` 
7. conda activate venv / venv/Scripts/Activate.ps1 
```
``` 
8. pip install -r requirements.txt
```


# git command
```
1. git add .
```
```
2. git status
```
```
3. git restore <file> /git remove <file>.
```
```
4. git commit -m "first commit"
```
```
5. git branch -M main
```
```
6. git push -u origin main
```
```
7. git log
```
```
8. git remote -v (to check url/github link)
```
```
9. git branch
```

# For Heroku account
```
1. gmail = pramodkhavare200@gmail.com
2. api_key = 38c10d28-d90e-430f-9869-1607883ce7a1
3. app_name = machinelearning-app
```

# Docker file command
```
1. docker status
2. docker build -t<image_name>:<tagname> .
  docker build -t ml_project:latest .
```
> Note : Image name for docker must lowercase

To list docker image
```
docker images
```

Run Docker Image
```
docker run -p 5000:5000 -e PORT=5000 <Image_id>
```

To check running docker container
```
docker ps
```

To stop docker container
```
docker stop <container_id>
```