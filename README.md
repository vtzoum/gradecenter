# gradecenter
Εφαρμογή Διαχείρισης Βαθ.Κέντρων Πανελλαδικώς Εξεταζόμενων Μαθημάτων

Προδιαγραφές Εγκατάστασης
--------------------
Οι οδηγίες αφορούν σε εγκατάσταση με τις εξής προδιαγραφές:
Ubuntu 14.04
Apache2
sqlite
mod-wsgi
Django 1.09

Επιπλέον υπάρχει μια σειρά από αντικείμενα (UI Frameworks, Themes)
που απαιτούντια για το User Interface της εφαρμογής: 
Bootstrap
Font-Awesome-4.7.0
Flat-Admin-Bootstrap-Theme
JQXWidgets

*Είναι απαραίτητο να έχουμε πρόσβαση διαχειριστή στο ΛΣ

Οδηγίες Εγκατάστασης
--------------------
Μεταφερόμαστε στο Document Folder του Apache2
cd /var/www/html

Κατεβάζουμε την εφαρμογή μαζί με τα αντικείμενα.
sudo git clone https://github.com/vtzoum/gradecenter

Εγκαθοστούμε τα προαπαιτούμενα της εφαρμογής
sudo pip install -r gradecenter/requirements.txt

Αλλάζουμε ιδιοκτησία+δικαιώματα στον ριζικό φάκελο της εφαρμογής
sudo chown www-data:www-data gradecenter
sudo chmod 755 gradecenter

Αλλάζουμε ιδιοκτησία+δικαιώματα σε ΒΔ
cd gradecenter
sudo chown www-data:www-data db.sqlite3
sudo chmod 755 db.sqlite3

Αλλάζουμε ιδιοκτησία+δικαιώματα σε φάκελο για uploads 
sudo chown www-data:www-data uploads
sudo chmod 755 uploads

Δηλώνουμε την εφαρμογή στις ρυθμίσες του Apache2 (Conf.)
(Λογικά στο /etc/apache2/sites-available/000-default.conf)
########################################
# START Application SERVER Instance (:8000) 
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
########################################
# END Application SERVER Instance (:8000)
########################################
Κάνουμε επανεκκίνηση στον #Restart Apache2
sudo service apache2 restart

Εφόσον γνωρίζουμε την ip του μηχανήματός μας, 
ανοίγουμε ένα Browser και δηλώνουμε δ/νση 
http://ip:8000/gradecenter


