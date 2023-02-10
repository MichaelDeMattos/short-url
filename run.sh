#!/usr/bin/bash

now=$(date)
line="========================= $now ========================="

echo $line
echo "Runing git pull to git branch develop"
git pull origin develop

stamp_head_migration=$(cat <<EOF

# If you want to run (migrations + app) use this context
ENTRYPOINT ["/bin/bash", "-c"]
CMD ["/short-url/wait-for-it.sh -h db -p 5432 --strict --timeout=300 -- /short-url/wait-for-it.sh -h redis -p 6379 --strict --timeout=300 -- flask db stamp head && flask db migrate && flask db upgrade && uwsgi --ini short-url.ini"]
EOF
)

only_app=$(cat <<EOF

# If you want to run only this app use this context
ENTRYPOINT ["/bin/bash", "-c"]
CMD ["/short-url/wait-for-it.sh -h db -p 5432 --strict --timeout=300 -- /short-url/wait-for-it.sh -h redis -p 6379 --strict --timeout=300 -- uwsgi --ini short-url.ini"]
EOF
)

argv=$1
if [ "$argv" == 'stamp-head-migration' ]
then
    echo "$stamp_head_migration" >> Dockerfile
else
    echo "$only_app" >> Dockerfile
fi

now=$(date)
echo $line
echo "Runing Docker Build"
sudo docker-compose build

now=$(date)
echo $line
echo "Runing Docker Up"
sudo docker-compose up
