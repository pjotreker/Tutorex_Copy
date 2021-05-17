#dokumentacja projektu
### Back-end 

### Front-end

###Testy

###Baza danych
<p>Baza danych działa na serwerze Heroku.
Jest to rozwiązanie chmurowe. 
W projekcie korzystamy z planu "Hobby-dev", który oferuje limit 10.000 krotek w tabeli, 1 GB miejsca na dane i 20 slotów na połączenia z bazą.
Baza danych opiera się na systemie zarządzania bazami danych PostgreSQL.
Baza została podłączona do projektu w pliku "settings.py".</p>
<p>
Dane:<ol>
<li>Host: ec2-52-19-170-215.eu-west-1.compute.amazonaws.com</li>
<li>Database: d2hevt4sscj1g7</li>
<li>User: bfadhmhbmjxfmh</li>
<li>Port: 5432</li>
<li>Password: -</li>
<li>URI: postgres://bfadhmhbmjxfmh:b0d452b1886cd23d29fb4341abc541929d8c5ee55b668c65d1daf9bc25567630@ec2-52-19-170-215.eu-west-1.compute.amazonaws.com:5432/d2hevt4sscj1g7</li>
<li>Heroku CLI: heroku pg:psql postgresql-triangular-25080 --app tutorex-test</li></ol></p>

<p>Bazą można zadządzać dzięki zainstalowaniu lokalnie programu pgAdmin i zalogowaniu się danymi podanymi wyżej.</p>