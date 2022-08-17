#!/bin/sh -x

# Mysql Server starten und setup
sh -c "/etc/init.d/mysql restart"
sh -c "mysql -u root -Be 'SOURCE /home/garderosinstall/db_setup.sql'"
sh -c "mysql -u root -Be 'SOURCE /home/garderosinstall/examples/database/schema.sql'"
# sh -c "mysql -u root -Be 'SOURCE /home/garderosinstall/examples/database/example_content.sql'"	# Klappt nicht, wird aber eigentlich auch nicht gebraucht

# Tomcat starten
sh -c "/etc/tomcat/bin/catalina.sh run"
