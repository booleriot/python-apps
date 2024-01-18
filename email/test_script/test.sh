curl --ssl smtps://smtp.163.com \
     --mail-from hbnugeek@163.com \
     --mail-rcpt 3187088047@qq.com \
     --upload-file ./email.txt \
     --user 'hbnugeek@163.com:LKDIYGCUEPFQLXXB' \
     -k -v
# curl --url smtp://smtp.163.com:465 \
#      --ssl-reqd \
#      --mail-from hbnugeek@163.com \
#      --mail-rcpt 3187088047@qq.com \
#      --upload-file ./email.txt \
#      --user 'hbnugeek@163.com:LKDIYGCUEPFQLXXB' -v
