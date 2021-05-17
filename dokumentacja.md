## Dokumentacja projektu

### Back-end 

##### Logowanie

1. W celu stworzenia funkcjonalności logowania się zostały zaimportowane funkcje *authenticate, login* z *django.contrib.auth*.

2. Zostały dodane odpowiednie ścieżki w *users/urls.py* (login/, success/, logout/).
3. W funkcji *index_view* zostało zaimplementowane pobieranie od użytkownika, przy użyciu formularza (*index.html*), emaila (*email*) i hasła (*password*), które następnie są sprawdzane czy znajdują się w bazie użytkowników. Jeśli tak- użytkownik zostaje zalogowany (*login(request, user)*), w przeciwnym wypadku wyświetlany jest komunikat o niepoprawnych danych. 
4. W przypadku poprawnego zalogowania użytkownik zostaje przekierowany do widoku sukcesu (*redirect('user-success')*) - strona domowa (*main.html*).

##### Wylogowywanie

1. W celu stworzenia funkcjonalności wylogowania się, została zaimportowana funkcja *logout*  z *django.contrib.auth*.
2. Po naciśnięciu odpowiedniego przycisku funkcja *user_logout* wylogowuje użytkownika i zostaje on przekierowany na stronę główną - *index.html*.

##### Odzyskiwanie hasła

1. Dodane zostały odpowiednie ścieżki: *request-reset-link/*, *user/<user_uid>/reset-password/<token>*, *link-send/*.
2. Zaimportowany został *PasswordResetTokenGenerator* oraz z *django.core.mail*- *send_mail*.
3. Po wejściu w *request-reset-link/*  Poprzez formularz (*reset_password.html*) w klasie *RequestResetPasswordEmail*, pobierany jest od użytkownika adres email (*email*), na który ma zostać wysłany link do zresetowania hasła.
4. Jeśli podany email znajduje się w bazie użytkowników zostaje wygenerowany odpowiedni link i wysłany mailem. Użytkownik zostaje poinformowany o wysłaniu linka (funkcja *link_send* z widokiem *link_send.html*)
5. Po kliknięciu w link z maila, użytkownik zostaje przekierowany do widoku zmiany hasła (*set_new_password.html*)- klasa *CompletePasswordReset* poprzez formularz pobiera od użytkownika nowe hasło (*password*) i prosi o potwierdzenie go (*password2*).
6. Jeśli hasła się zgadzają, zmiany zostają zapisane a użytkownik zostaje przekierowany na stronę główną (*redirect('user-login')*) gdzie może się zalogować nowym hasłem. W przeciwnym wypadku widok zostaje wyrenderowny ponownie.

### Front-end

### Testy

### Baza danych

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