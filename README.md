
# Roshid-server

Roshid is a community-driven, conversation-based social commerce platform. It is an open-source platform that automates the backend of your social media-based businesses.
<p align="center">
    <img src="frontend\src\assets\roshid-logo-bn.png"
        height="200">
</p>
<p align="center">Website:  <a href="https://roshid.com" alt="website"> Roshid.com</a>
</p>


## Run Locally (for development)

1 . Clone the project

```bash
  git clone https://github.com/siam19/roshid.git
```

2 . Go to the project directory

```bash
  cd roshid
```
3 . Pull `.env` file [template](https://gist.github.com/siam19/9789825d676d27ebc24212b51d127556) in root directory of the project. Fill it with your credentials. 

```bash
curl -o .env https://gist.githubusercontent.com/siam19/9789825d676d27ebc24212b51d127556/raw/fa195912faece84ac55347c77271116b02e37bd2/roshid_env_file
```

4 . To run the application you must have [docker installed](https://docs.docker.com/engine/install/).
```bash
  docker-compose up --build -d
```
this builds the docker containers and `-d` runs it in detached mode. 




## Features

- Records and processes order with just a screenshot of the conversation 
- Has integration with local delivery services allowing you to automatically sends a pickup request upon a new order. 
- User can add products and prices and roshid will keep track of sales.
## Feedback

If you have any feedback, please reach out to us at fake@fake.com

