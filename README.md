## MachineLearningProject1
1. [Github Account](https://github.com/pramodkhavare/MachineLearningProject1.git)

# Used Command in cmd

```
python -m venv env
```

```
ls
```

```
cd foldername
```

```
code . (open vs code using cmd)
```

```
python setup.py install
```
```
pip install -r requirements.txt
```
```
pip install -e.
```
Install ipkernel
```
pip install ipkernel
```



# git command 
```
git clone link
```

```
git add .
```

```
git push origin main
```

```
git --version
```

```
git pull
```

```
conda create -p venv python==3.7 -y  /python -m venv venv 
```

``` 
conda activate venv / venv/Scripts/Activate.ps1 
```

``` 
pip install -r requirements.txt
```

```
git add .
```

```
git status
```

```
git restore <file> /git remove <file>.
```

```
git commit -m "first commit"
```

```
git branch -M main
```

```
git push -u origin main
```

```
git log
```

```
git remote -v (to check url/github link)
```

```
git branch
```

# For Heroku account
```
gmail = pramodkhavare200@gmail.com
api_key = <>
app_name = machinelearning-app
```

# Docker file command
```
docker status
docker build -t<image_name>:<tagname> .
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