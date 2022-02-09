<!--
Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
This program and the accompanying materials  are made available under the terms 
of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
the terms of the Healthcare Disclaimer.
-->
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

Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
This program and the accompanying materials  are made available under the terms 
of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
the terms of the Healthcare Disclaimer.# i2b2-etl
