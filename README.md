# MongoDB Install

* CacheSize는 (메모리 - 1GB)/2 로 설정.
* Replica Set에 Primary 설정은 1로 끝나는 호스트명인 서버에서 진행.
  * ex) Config : mongocs-prod-srv01
  * ex) Shard : mongod-prod-srv11
* Replica 명은 인자로 받은 서비스명 변수로 진행.
  * ex) svr_name=sgjung - replSetName: "sgjungRS-1"
* Config/Router 서버는 동일 서버에서 구성.
* mongo.hosts 파일 내용 중 [mongoc], [mongos]에 대한 호스트명이 없을 경우 Replica Set만 구성
* backup은 운영 환경에서만 구성하고, 3호기에서만 크론탭 설정

#
### Ansible 실행
#### - Anible 실행 전 qa/prod 공통 변수에 admin 계정 정보를 작성(inventories/qa/mongo_vars.yaml)
#### - Shard가 1개 노드 이상일 경우 [mongod-2]. [mongod-3] 항목을 추가한다.(inventories/qa/mongo.hosts)


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
├─inventories
│  ├─prod
│  └─qa
└─roles
    ├─backup
    ├─common
    ├─mongoc
    ├─mongod
    ├─mongos
    └─pmm
```