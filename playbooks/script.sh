Log=log/file
> $Log
uptime >> $Log
sleep 60 &&
uptime >> $Log
echo "Script is completed" >> $Log

