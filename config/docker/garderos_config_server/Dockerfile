FROM ubuntu:20.04
USER root

ENV DEBIAN_FRONTEND noninteractive
EXPOSE 8080
EXPOSE 3306

# Update container
RUN apt-get update -y

# Download necessary packages ( not needed atm)
RUN apt-get install wget mysql-server default-jdk -y 

# Install tomcat and start service
RUN mkdir /opt/tomcat/
WORKDIR /opt/tomcat
COPY apache-tomcat-9.0.65.tar.gz /opt/tomcat/apache-tomcat-9.0.65.tar.gz
RUN tar xvfz apache*.tar.gz
RUN mv apache-tomcat-9.0.65/* /opt/tomcat/.
WORKDIR /opt/tomcat/webapps

# Start mysql server and setup database
RUN chown -R mysql:mysql /var/lib/mysql
RUN usermod -d /var/lib/mysql/ mysql

# start does now work yet
RUN /etc/init.d/mysql restart

# Create garderos folder
WORKDIR /home/
RUN mkdir garderosinstall
WORKDIR /home/garderosinstall

# Database: Install mysql-java connector within the Tomcat lib directory
RUN wget https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-5.1.49.tar.gz
RUN tar -xzvf mysql-connector-java-5.1.49.tar.gz
RUN cp mysql-connector-java-5.1.49/mysql-connector-java-5.1.49.jar /opt/tomcat/lib/

# Unpack Garderos stuff
COPY Configserver-C963_G958_L954.tgz /home/garderosinstall/Configserver-C963_G958_L954.tgz
COPY db_setup.sql /home/garderosinstall/db_setup.sql
RUN tar -xvf /home/garderosinstall/Configserver-C963_G958_L954.tgz --directory /home/garderosinstall
RUN tar -xzvf /home/garderosinstall/db_and_libs.tgz --directory /home/garderosinstall

# Copy sql files into db
#RUN mysql -u root < /home/garderosinstall/db_setup.sql
#RUN mysql -u root < /home/garderosinstall/examples/database/schema.sql

# Deploy the configserver webapp:
WORKDIR /opt/tomcat/webapps/
RUN mkdir configserver
RUN cd /opt/tomcat/webapps/configserver
RUN jar xvf /home/garderosinstall/configurator-r963.war

# Deploy the grsadmin webapp:
WORKDIR /opt/tomcat/webapps/
RUN mkdir grsadmin
WORKDIR /opt/tomcat/webapps/grsadmin
RUN jar xvf /home/garderosinstall/grsadmin-r958.war

# Deploy the logging webapp (not mandatory):
WORKDIR /opt/tomcat/webapps/
RUN mkdir logging
WORKDIR /opt/tomcat/webapps/logging
RUN jar xvf /home/garderosinstall/logging-r954.war

# Configuration of configserver
COPY server.xml /opt/tomcat/server.xml
#RUN cp /home/garderosinstall/examples/etc/server.xml /opt/tomcat/

# Start tomcat and mysql
COPY start.sh /home/garderosinstall/start.sh
WORKDIR /home/garderosinstall/
RUN chmod 777 start.sh
CMD ["./start.sh"]
#CMD ["/opt/tomcat/bin/catalina.sh", "run"]

#RUN wget https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-5.1.49.tar.gz
#RUN tar -xzvf mysql-connector-java-5.1.49.tar.gz
#RUN cp mysql-connector-java-5.1.49/mysql-connector-java-5.1.49.jar /usr/share/tomcat9/lib/

# Start mysql
#RUN usermod -d /var/lib/mysql/ mysql
#RUN /etc/init.d/mysql restart
#RUN service mysql start

#Basic security - enable HTTPS
#RUN cd /etc/tomcat*/
#RUN keytool -genkey -alias <your-server-name-or-IP> -keysize 4096 -keyalg RSA -keypass garderos -validity 365 -keystore config.keystore -storepass garderos