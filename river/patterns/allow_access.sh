PORT=$(python3 -c "import socket;s=socket.socket();s.bind(('', 0));print(s.getsockname()[1]);s.close()")
echo $PORT > $RIVER_HOME/.river/jobs/$uuid_job_id/job.port
echo $(hostname) > $RIVER_HOME/.river/jobs/$uuid_job_id/job.host