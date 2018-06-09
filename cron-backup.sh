#!/bin/sh 
#########################
#0. TIME (aka WHEN to execute)
#########################
#Cron Job every weekday during working hours
#This example checks the status of the database every weekday (i.e excluding Sat and Sun) during the working hours 9 a.m to 6 p.m.
#00 09-18 * * 1-5 /home/ramesh/bin/check-db-status

######################### 
#1. ACTIONS (aka WHAT to execute)
#########################
dbDB='db.sqlite3'
dbDBCopy="db.sqlite3.$(date +\%F-\%R)"
path='/var/www/html/grade-center-app/'
#c=$a$b
#echo $c
#sudo cp -a  /var/www/html/grade-center-app/db.sqlite3 /var/www/html/grade-center-app/db.sqlite3.CRONED	#OK
#sudo cp -a  /var/www/html/grade-center-app/db.sqlite3 "/var/www/html/grade-center-app/db.sqlite3.$(date +\%F-\%R)"

sudo cp -a  $path$dbDB $path$dbDBCopy							#OK
sudo cp -a  $path$dbDBCopy "/media/teacher/BK043-32G/db_Production/"$dbDBCopy
wput -u $path$dbDBCopy ftp://bk043@boarhost.com:1234bk043@boarhost.com			#OK

#sudo cp -a  $path$dbDB /var/www/html/grade-center-app/db.sqlite3.CRONED1		#OK
#sudo cp -a  $path$dbDB /var/www/html/grade-center-app/db.sqlite3.CRONED2		#OK
#sudo cp -a  $path+"db.sqlite3" /var/www/html/grade-center-app/db.sqlite3.CRONED3	#OK


#########################
#2. TIME EXPLANATION (what it measn)
#########################
#*     *     *     *     *  YOURCOMMAND
#-     -     -     -     -
#|     |     |     |     |
#|     |     |     |     +----- Day in Week (0 to 7) (Sunday is 0 and 7)
#|     |     |     +------- Month (1 to 12)
#|     |     +--------- Day in Month (1 to 31)
#|     +----------- Hour (0 to 23)
#+------------- Minute (0 to 59)
