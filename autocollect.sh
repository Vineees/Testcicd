#!bin/bash
date
sudo chmod 755 -R /home/production/Morea/
. /home/production/Morea/env/bin/activate
python3 /home/production/Morea/manage.py collectstatic

deactivate