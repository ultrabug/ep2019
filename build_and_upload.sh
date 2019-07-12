#! /bin/bash

BRANCH=$(grep ref .git/HEAD | sed 's@.*/\(.*\)@\1@g')
echo "pushing ${BRANCH} image"

docker build -t registry.numberly.in/ajm/trello-to-graphql:${BRANCH} . && \
docker push registry.numberly.in/ajm/trello-to-graphql:${BRANCH}
