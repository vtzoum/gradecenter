#########################
#0. SOS DB backup 
#########################
dbFile="db.sqlite3.$(date +%F-%R)"
sudo cp -a  db.sqlite3 "db.sqlite3.$(date +%F-%R)"

#########################
#0. RSYNC
#########################
#Copy/Sync a Directory on Local Computer
# rsync HOME -> DEST
pathSource=/var/www/html/gradecenter-DEVELOP/db-bk043-2017.s
pathDest=/var/www/html/gradecenter-DEVELOP/db-bk043-2017
sudo cp -a  db.sqlite3 "db.sqlite3.$(date +%F-%R)"
rsync -avzh --dry-run -progress  --exclude '*.sqlite3' /media/tzoumak/CRUZER64G/Web-SITES-Code/DJANGO-python/APPS/gradecenter-DEVELOP/ /var/www/html/gradecenter-DEVELOP/

#########################
#GIT pull new code
#########################
sudo git pull 

#########################
#Change DB File Perms
#########################
sudo chown www-data:www-data db.sqlite3
sudo chmod 755 db.sqlite3

#########################
#Change UPLOADS Dir Perms
#########################
uploadsDir=uploads
sudo chown www-data:www-data uploads
sudo chmod 755 uploads
