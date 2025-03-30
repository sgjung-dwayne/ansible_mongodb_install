
kill -9 $(ps aux | grep {{mongos_conf_file_name}} | grep -v grep | awk '{print $2}')