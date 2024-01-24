# Goodchain README

## Installation requirements
1. install python 
2. install pip
3. run the following command: `pip install -r requirementes.txt`

## Run Goodchain
1. navigate to the root directory 
2. run: `docker-compose up --scale blockchain-server=2 --build`
3. To have more nodes, change the number from 2 to any number
4. Go into Docker desktop and use the CLI from the running docker container
5. Should be under container group goodchain.
