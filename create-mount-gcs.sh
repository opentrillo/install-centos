#!/usr/bin/env bash

PROJECTID=`gcloud projects list | awk 'FNR>1 {print$1}'`
echo $PROJECTID

bucketName=trillo-${PROJECTID}
echo $bucketName

groupId=`cut -d: -f3 < <(getent group sftpusers)`

tee -a /etc/fstab << END
${bucketName} /gcs gcsfuse rw,allow_other,uid=65534,gid=${groupId},file_mode=0775,dir_mode=0775,implicit_dirs
END

mount ${bucketName}

