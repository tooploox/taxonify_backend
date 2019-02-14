#!/bin/bash
set -e

# lame function for parsing mongo connection string
# into user password and db name
function parse_user_password_and_db() {
  connection_string=$1

  IFS=':' read -ra parts <<< $connection_string

  user=${parts[1]}
  user="${user:2}"

  password_and_stuff=${parts[2]}
  IFS="@" read -ra parts <<< $password_and_stuff
  password=${parts[0]}

  rest=${parts[1]}
  IFS="/" read -ra parts <<< $rest
  db=${parts[1]}

}

parse_user_password_and_db $MONGO_CONNECTION_STRING

mongo $db <<EOF
db.createUser({
  user:  '$user',
  pwd: '$password',
  roles: [{
    role: 'readWrite',
    db: '$db'
  },
  {
    role: 'dbAdmin',
    db: '$db'
  }]
})
EOF
