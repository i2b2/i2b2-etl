docker rm -f $(docker ps -a -q)
docker volume rm $(docker volume ls -q --filter dangling=true)
docker network rm i2b2-net

create concept
{
   "code":"LLM1",
   "path":"/LLM/LLM1",
   "type":"assertion",
   "description":"Model trained in Diabetes patients",
   "blob":{
      "MRN":"123"
   }
 }

{
  "input": {
    "path": "/LLM/LLM1",
    "function": "llm_apply"
  },
  "jobType": "llm"
}
