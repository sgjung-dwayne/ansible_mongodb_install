#! /usr/bin/python3 
import os, sys, datetime, os.path, tarfile 
from pymongo import MongoClient
import pymongo 
import tailer, shutil 
import json, requests 
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))) 

DIR='/log/backup/' 
def create_folder(host): 
    directory = (DIR+host) 
    if not os.path.exists(directory): 
        os.makedirs(directory) 
    return directory 

def create_sub_folder(host, today):
    sub_directory = (DIR+host+'/'+today)
    if not os.path.exists(sub_directory):
        os.makedirs(sub_directory + '/data') 
    return sub_directory
 
def check_master(host,port,username, password): 
    client = MongoClient ("mongodb://%s:%s@%s:%s/" % (username, password, host, port)) 
    db = client['test'] 
    info = client.admin.command("isMaster")
    p= info['primary'] 
    s= info['hosts'] 
    s.remove(p)

    if len(s) == 2: 
        return s[1] 
    elif len(s) == 1: 
        return s[0] 
    else: 
        print('Not Exists Secondary') 
        exit()

def make_tarfile(tar_name,sub_directory): 
    with tarfile.open(tar_name, "w:") as tar: 
        tar.add(sub_directory, arcname=os.path.basename(sub_directory)) 
        shutil. rmtree(sub_directory)

def delete_old_directory(path_target, days): 
    for f in os.listdir(path_target): 
        f = os.path.join(path_target, f) 
        current = datetime.datetime.now().timestamp() 
        old = os.stat(f).st_mtime < current - (days * 24 * 60 * 60) 
        if old: 
            try: 
                os.remove(f) 
                print(f, 'is deleted') 
            except OSError: print(f,'can not delete') 

def send_alert_to_slack(messages): 
    url= "" 
    send_data = { 
        "channel": "", 
        "text": messages
    } 
    send_text = json.dumps(send_data) 
    requests.post(url, data=send_text.encode('utf-8'))

def run_backup(host,port,today): 
    username = "mgobackup" 
    password = "Backup!0124" 
    secondary = check_master(host, port, username, password) 
    secondary1 = secondary.split(':') 
    print('===============================================') 
    print('MongoDB Dump Backup Started at secondary ( {}:{} )'.format(secondary1[0], secondary1[1]))
    print('===============================================\n')

    start_backup = datetime.datetime.today().strftime("%Y:%m:%d H:%M") 
    message = ("*MongoDB Dump Backup*\n\n>*Host* : {}\n>*Time* : {} ~ ".format(secondary1[0], start_backup)) 
    db_backup_command = ('tar -zcvf %s /db/mongo ' % (sub_directory+'/db.tar.gz'))
    data_backup_command = ('/db/mongo/bin/mongodump --host %s --port %s --readPreference=secondary -ư%s -p%s --authenticationDatabase admin --out %s --gzip --oplog >> %s.log 2>&1' % (secondary1[0], secondary1[1], username,password, (sub_directory+'/data'), sub_directory))
    
    try: 
        print('Command --> {})'.format(db_backup_command)) 
        os.system(db_backup_command) 

        print('Command --> {})'.format(data_backup_command)) 
        os.system(data_backup_command) 

        end_backup = datetime.datetime.tòday().strftime("%H:%M") 
        message += ("{}". format (end_backup)) 
        send_alert_to_slack(message) 

    except Exception as e: 
        print('[-] An unexpected error has occurred') 
        print('[-] '+ str(e) ) 
        print('[-] EXIT') 
        message = str(e) 
        send_alert_to_slack(message) 

# main 
if __name__ == "__main__":


    today = datetime.datetime.today().strftime("%Y%m%d%H%M") 
    if (not(len(sys.argv) == 3)): 
        print('[-] Incorrect number of arguments') 
        print('python backup.py [secondary-host] [secondary-port] [username] [password]')
        print('python backup.py [secondary-host] [secondary-port]') 
        exit() 
    else: 
        host = sys.argv[1] 
        port = sys.argv[2] 
        create_folder(host) 
        sub_directory = create_sub_folder(host, today) 
        run_backup(host,port,today) 
        make_tarfile(sub_directory + '.tar',sub_directory) 
        
    log_file_name = ('{}.log'.format(sub_directory)) 
    lines = tailer.tail(open(log_file_name),1) 
    if 'Failed' in lines[0]: 
        print(lines) 
        message = lines 
    else: 
        print('===================================================')
        print("{} Mongodump Successfully Finished!!".format(host)) 
        print('===================================================') 


    delete_old_directory(DIR+host, 3) 



