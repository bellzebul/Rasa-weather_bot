# Weather bot 


### Setup

1. Clone repo.
2. Open terminal from root dir of project.
3. Build docker images:\
   `docker build -t rasa_server .`\
   `docker build -t action_server -f actions/Dockerfile .`
4. Create network:\
   `docker network create rasa_network`
5. From first terminal run:\
    `docker run -v PATH_TO_ACTIONS_DIR:/app --network rasa_network --name action_server -p 5055:5055 action_server`
6. And from second:\
    `docker run -it -v PATH_TO_ROOT_DIR:/app -p 5005:5005 --net rasa_network rasa_server /bin/bash`\
   where write \`rasa shell`



### A little bit about bot

If the bot doesn't understand your intent, it won't say anything. \
After asking for the weather, you should thank the bot and then ask a new question. Without thanking the bot, it will not work again. \
The bot responds to a small number of cities. If you enter a city and the bot asks you to enter a location, try another location. (works well on such cities as Lviv, Kiev, Odessa, Paris, Tokyo).\
Bot can help with the weather for today, tomorrow and the day after tomorrow.\
If you don't enter a date, the bot will give you the weather for today.
