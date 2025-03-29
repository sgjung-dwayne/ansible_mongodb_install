
numactl --interleave=all {{mongo_bin_dir}}/bin/mongod -f {{mongo_bin_dir}}/conf/{{mongoc_conf_file_name}}