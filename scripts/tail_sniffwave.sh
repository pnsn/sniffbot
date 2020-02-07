#/usr/bin/env bash
source ../sniffbot/.env
nohup ssh $EWORM_USER@$EWORM_HOST sniffwave $EWORM_RING wild wild wild wild | awk '{print $1,$11,$12,$20,$21,$22,$23,$24}' >$SNIFF_LOG &