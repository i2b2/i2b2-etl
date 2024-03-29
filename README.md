# Build docker image locally & Start i2b2-etl
clone the i2b2-etl & Mozilla repo 

git clone https://github.com/i2b2/i2b2-etl.git 

git clone https://github.com/i2b2/i2b2-cdi-qs-mozilla.git

## Copy Mozilla folder inside i2b2-etl repo
cp -r  mozilla-i2b2-etl/Mozilla/  i2b2-etl/

cd i2b2-etl

## Build the docker image locally 
docker build -t i2b2/i2b2-etl:local-v1 . 

## Update the etl tag & start i2b2-etl container
open i2b2-etl-docker/postgres/.env file 

update i2b2-etl tag to local-v1

## Remove the existing i2b2-etl docker container 
docker rm -f i2b2-etl

## Start the new i2b2-etl container 
docker-compose up -d i2b2-etl 

## To execute the test cases

Start a bash shell inside the i2b2-etl container
```shell
$ docker exec -it i2b2-etl bash
python -m unittest discover -s i2b2_cdi/test/
```

# i2b2-etl
i2b2-etl provides a command line interface and api interface to import, delete concepts and facts and encounters.

## Deploy i2b2 with etl container
refer to i2b2-docker project repo to deploy i2b2 with etl container

## Executing the I2B2-ETL 

```shell
Start a bash shell inside the i2b2-etl container
$ docker exec -it i2b2-etl bash

For ease of documentation use etl as an alias for command invocation
$ alias etl="python -m i2b2_cdi ${ARGS}"
```
### I2B2-ETL commands
Below commands helps to play with I2B2-ETL

### Help
This will list all possible operation of i2b2-etl
```shell
$ etl --help
OR
$ etl -h
```

### Delete concepts
```shell
$ etl concept delete -c <env-file>
```

### Load concepts
```shell
$ etl concept load -c <env-file> -i <input-dir>
```

> **_Note:_** File name should have pattern like *_concepts.csv

### Delete facts
```shell
$ etl fact delete -c <env-file>
```

### Load facts
Load facts with concept_cd validation.
```shell
$ etl fact load -c <env-file> -i <input-dir>
```
Load facts with no concept_cd validation.
```shell
$ etl fact load -c <env-file> -i <input-dir> --disable-fact-validation
```
> **_Note:_** File name should have pattern like *_facts.csv



### Delete patients
```shell
$ etl patient delete -c <env-file>
```

### Load patients
```shell
$ etl patient load -c <env-file> -i <input-dir>
```

### Delete encounters
```shell
$ etl encounter delete -c <env-file>
```

### Load encounters
```shell
$ etl encounter load -c <env-file> -i <input-dir>
```

### Create project and user
Create new project & user along with password , also assign new project to new user.
```shell
$ etl project add -c <config-file> --project-name <project-name> --project-user-password <project-user-password>
```

### Load data into project
Copy data from one project to another.
```shell
$ etl project load -c <config-file> --project-name <project-name> 
```
### Change user password
Change password for user in i2b2
```shell
$ etl project password -c <config-file> --user <user-id> --password <password>
```

###  How to Cite
Wagholikar KB, Ainsworth L, Zelle D, et.al. I2b2-etl: Python application for importing electronic health data into the informatics for integrating biology and the bedside platform. **Bioinformatics**. 2022 Oct 14;38(20):4833-4836. 


### License

Copyright 2023 Massachusetts General Hospital.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.



