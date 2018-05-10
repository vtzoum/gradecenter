#########################
#0. SOS DB backup 
#########################
dbFile=db.sqlite3
sudo cp -a  /var/www/html/grade-center-app/db.sqlite3 /home/teacher/Desktop/db.sqlite3.CRONED
sudo cp -a  /var/www/html/grade-center-app/db.sqlite3 "db.sqlite3.$(date +\%F-\%R)"

#########################
#GIT pull new code
#########################
#########################
#Change DB File Perms
#########################
#sudo chown www-data:www-data db.sqlite3
#sudo chmod 755 db.sqlite3
#########################
#Change UPLOADS Dir Perms
#########################
uploadsDir=uploads

