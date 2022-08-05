#!/bin/sh
sh -c "/etc/init.d/mysql restart"
sh -c "/opt/tomcat/bin/catalina.sh run"

#
#sh -c "mysql -u root < /home/garderosinstall/db_setup.sql"
#sh -c "mysql -u root < /home/garderosinstall/examples/database/schema.sql"
#sh -c "mysql -u root -p < /home/garderosinstall/examples/database/example_content.sql