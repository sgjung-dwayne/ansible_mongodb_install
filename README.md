# MongoDB Install(w. Ansible)

* 스크립트 사용 전, mongo_vars.yaml을 확인
* CacheSize는 (메모리 - 1GB)/2 로 설정.
* Replica Set에 Primary 설정은 1로 끝나는 호스트명 서버에서 진행.
  * ex) Config : mongocs-prod-srv01
  * ex) Shard : mongod-prod-srv11
* Replica 명은 인자로 받은 서비스명 변수로 진행.
  * ex) svr_name=sgjung -> replSetName: "sgjungRS-1"
* Config/Router 서버는 동일 서버에서 구성.
* Shard 구성 시 노드가 1개 이상일 경우 [mongod-2]. [mongod-3] 항목을 추가한다(mongo.hosts)
   * ex) [mongod-2] -> mongod-qa-srv21(P),mongod-qa-srv22(S),mongod-qa-srv23(S)
   * ex) [mongod-3] -> mongod-qa-srv33(P),mongod-qa-srv32(S),mongod-qa-srv33(S)
* mongo.hosts 파일 내용 중 [mongoc], [mongos]에 대한 호스트명이 없을 경우 Replica Set만 구성
* backup은 운영 환경에서만 구성하고, 3호기에서만 크론탭 설정

#
### Ansible 실행
#####
* QA 
```yml
$ ansible-playbook -i inventories/qa/mongo.hosts install_mongodb.yaml --extra-vars "phase=qa svr_name=(서비스명)" -v
```
* PROD 
```yml
$ ansible-playbook -i inventories/qa/mongo.hosts install_mongodb.yaml --extra-vars "phase=prod svr_name=(서비스명)" -v
```
#
### Install Script Tree 

```yaml
│  mongodb_install.yaml
│
├─inventories
│  ├─prod
│  │      mongo.hosts
│  │      mongo_vars.yaml
│  │
│  └─qa
│          mongo.hosts
│          mongo_vars.yaml
│
└─roles
    ├─backup # 백업
    │  ├─files
    │  │      mongo_backup.py
    │  │
    │  └─tasks
    │          main.yaml
    │          set_backup.yaml
    │
    ├─common # 공통 OS
    │  ├─files
    │  │      uninstall.sh
    │  │
    │  └─tasks
    │          main.yaml
    │          set_os_mongo.yaml
    │
    ├─mongoc # Config
    │  ├─files
    │  │      mongo.key
    │  │
    │  ├─tasks
    │  │      main.yaml
    │  │      set_mongoc.yaml
    │  │
    │  └─templates
    │          mongoc.conf.j2
    │          mongoc.logrotate.j2
    │          mongoc.repl.j2
    │          mongoc.user.j2
    │          shutdown_mongoc.sh
    │          startup_mongoc.sh
    │
    ├─mongod 
    │  ├─files
    │  │      mongo.key
    │  │
    │  ├─tasks
    │  │      main.yaml
    │  │      set_mongod.yaml
    │  │
    │  └─templates
    │          mongod.conf.j2
    │          mongod.logrotate.j2
    │          mongod.repl.j2
    │          mongod.user.j2
    │          shutdown.sh
    │          startup.sh
    │
    ├─mongos # Router
    │  ├─files
    │  │      mongo.key
    │  │
    │  ├─tasks
    │  │      main.yaml
    │  │      set_mongos.yaml
    │  │
    │  └─templates
    │          mongos.addshard.j2
    │          mongos.conf.j2
    │          mongos.logrotate.j2
    │          shutdown_mongos.sh
    │          startup_mongos.sh
    │
    └─pmm
        ├─tasks
        │      main.yaml
        │      set_pmm.yaml
        │
        └─templates
                pmm-agent.service.j2
```