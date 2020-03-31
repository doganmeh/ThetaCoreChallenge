export PROJNAME="ThetaCoreChallenge"

sudo -u postgres psql -c "create database $PROJNAME"
sudo -u postgres psql -c "create user $PROJNAME with password '$PROJNAME' superuser"