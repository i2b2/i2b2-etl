alias docker='sudo docker'
docker stop $(docker ps -q) && docker rm $(docker ps -aq) && docker volume rm $(docker volume ls -q) && docker system prune -a --volumes --force
sudo service postgresql stop

git clone https://github.com/i2b2/i2b2-etl
cd i2b2-etl
git checkout ml-deploy
cd deployment/pg/
sudo docker compose up -d i2b2-llm
sudo docker logs -f i2b2-llm

see http://<ip>>/webclient/
login: demo\demo:Etl@2021
see http://<ip>>:5000/swagger/
login: demo\demo:Etl@2021



create concept
{
   "code":"LLM1",
   "path":"/LLM/LLM1",
   "type":"assertion",
   "description":"my LLM model",
   "blob":{
      "par1":"123"
   }
 }

post job
{
  "input": {
    "path": "/LLM/LLM1"
  },
  "jobType": "llm"
}

vi ../../i2b2_cdi/ML/llmEngine.py 
docker rm -f  i2b2-llm ;docker compose up -d i2b2-llm; docker logs -f i2b2-llm