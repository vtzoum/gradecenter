#touch 0000.txt
#rsync -avzh --dry-run -progress  --exclude '*.sqlite3*' /media/tzoumak/CRUZER64G/Web-SITES-Code/DJANGO-python/APPS/gradecenter-DEVELOP/ /var/www/html/gradecenter-DEVELOP/
rsync -avzh --dry-run -progress  --exclude '*.sqlite3*' ./ /var/www/html/gradecenter-DEVELOP/ 

