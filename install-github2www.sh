
#########################
#GIT CLone repo
#########################
#sudo git pull 
sudo git clone https://github.com/vtzoum/gradecenter 

#########################
#Install Python packages
#########################
sudo pip install ./gradecenter/requirements.txt

#########################
#Change Perms
#########################
#Change Root dir Perms/Owns
sudo chown www-data:www-data ./gradecenter
sudo chmod 755 ./gradecenter

cd gradecenter/
#Change DB File Perms
sudo chown www-data:www-data db.sqlite3
sudo chmod 755 db.sqlite3

#Change UPLOADS Dir Perms
sudo chown www-data:www-data uploads
sudo chmod 755 uploads

#########################
#APACHE2 Conf
#########################
sudo cat <<EOT >> /etc/apache2/sites-available/000-default.conf
########################################
# Application SERVER Instance (:8000) 
# Dir (./gradecenter)
########################################
Listen 8000
NameVirtualHost *:8000
<VirtualHost *:8000>
    ServerAdmin webmaster@mydomain.com
    ServerAlias www.mydomain.com
    
    #Application entry point 
    WSGIScriptAlias / /var/www/html/gradecenter/index.wsgi
    Alias /static/ /var/www/html/static/
    
    <Location "/static/">
        Options -Indexes
    </Location>

</VirtualHost>
EOT

#Restart APACHE2
sudo service apache2 restart

