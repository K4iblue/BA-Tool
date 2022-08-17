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
RUN mkdir /etc/tomcat/
WORKDIR /etc/tomcat
COPY apache-tomcat-9.0.65.tar.gz /etc/tomcat/apache-tomcat-9.0.65.tar.gz
RUN tar xvfz apache*.tar.gz
RUN mv apache-tomcat-9.0.65/* /etc/tomcat/.
WORKDIR /etc/tomcat/webapps

# Start mysql server and setup database
RUN chown -R mysql:mysql /var/lib/mysql
RUN usermod -d /var/lib/mysql/ mysql
#ADD my.cnf /etc/mysql/conf.d/my.cnf
#RUN chmod 644 /etc/mysql/conf.d/my.cnf

# Create garderos folder
WORKDIR /home/
RUN mkdir garderosinstall
WORKDIR /home/garderosinstall

# Unpack Garderos stuff
COPY Configserver-C963_G958_L954.tgz /home/garderosinstall/Configserver-C963_G958_L954.tgz
COPY db_setup.sql /home/garderosinstall/db_setup.sql
RUN tar -xvf /home/garderosinstall/Configserver-C963_G958_L954.tgz --directory /home/garderosinstall
RUN tar -xzvf /home/garderosinstall/db_and_libs.tgz --directory /home/garderosinstall

# Deploy the configserver webapp:
WORKDIR /etc/tomcat/webapps/
RUN mkdir configserver
RUN cd /etc/tomcat/webapps/configserver
RUN jar xvf /home/garderosinstall/configurator-r963.war

# Deploy the grsadmin webapp:
WORKDIR /etc/tomcat/webapps/
RUN mkdir grsadmin
WORKDIR /etc/tomcat/webapps/grsadmin
RUN jar xvf /home/garderosinstall/grsadmin-r958.war

# Deploy the logging webapp (not mandatory):
WORKDIR /etc/tomcat/webapps/
RUN mkdir logging
WORKDIR /etc/tomcat/webapps/logging
RUN jar xvf /home/garderosinstall/logging-r954.war

# Database: Install mysql-java connector within the Tomcat lib directory
RUN wget https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-5.1.49.tar.gz
RUN tar -xzvf mysql-connector-java-5.1.49.tar.gz
RUN cp mysql-connector-java-5.1.49/mysql-connector-java-5.1.49.jar /etc/tomcat/lib/
#RUN cp mysql-connector-java-5.1.49/mysql-connector-java-5.1.49.jar /etc/tomcat/webapps/grsadmin/WEB-INF/lib/	# Extra

# Configuration of configserver
RUN cp /home/garderosinstall/examples/etc/server.xml /etc/tomcat*/
#COPY server.xml /opt/tomcat/server.xml

# Start tomcat and mysql
COPY start.sh /home/garderosinstall/start.sh
WORKDIR /home/garderosinstall/
RUN chmod 777 start.sh
CMD ["./start.sh"]
