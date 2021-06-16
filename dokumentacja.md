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

##### Tworzenie przez nauczyciela klasy

1. W celu umożliwienia nauczycielowi zakładania klas, stworzony został __model *Classroom*__ z nastęującymi polami: classroom_id (*int* kod klasy potzrebny by nauczyciel mógł zaprosić ucznia do klasy; nie jest to klucz podstawowy!), subject(*string* o maksymalnej długości 255), name(*string* o maksymalnej długości 80), owner (klucz obcy do obiektu nauczyciela), age_range_min, age_range_max(oba *int*, ograniczenie: większe od 0 ale mniejsze od 99), time_frame_start, time_frame_end (oba typu *date*), lessons (pole 'many to many') i students (pole 'many to many') .
2. Dodawanie klasy jest obsługiwane przez widok *CreateClassroom* przy pomocy "create_classroom.html", w którym nauczyciel uzupełnia pole obowiązkowe: nazwa klasy (*name* w modelu *Classroom*) oraz może opcjonalnie podać wartości pozostałch pól: temat klasy (*subject*), minimalny i maksymalny wiek uczniów klasy (odpowiednio: *age_range_min, age_range_max*) oraz zakres czasu w jakim działać będzie klasa (odpowiednio *time_frame_start, time_frame_end*- te pola są jednak tylko informacją dla nauczyciela/ucznia, podanie ich nie skutkuje np. kasowaniem klasy po danym terminie). Reszta pól (*classroom_id i owner*) uzupełniana jest automatycznie.
3. Po udanym zapisaniu klasy w bazie danych nauczyciel zostaje przekierowany na adres *classroom-created/<classroom_id>* gdzie przy pomocy "classroom_created_success.html" wyświetlany jest *classroom_id* (kod klasy), które nauczyciel następnie przekazuje uczniowi. 
4. W przypadku niepowodzenia strona dodawania klasy jest renderowana ponownie.

##### Zgłaszanie przez ucznia chęci dołączenia do klasy

1. W celu umożliwienia uczniowi dołączenia do klasy, pod adresem *join-classroom/* przy użyciu formularza "join_classroom.html" uczeń wpisuje otrzymany przez nauczyciela kod klasy.
2. W celu przetrzymywania informacji o chęci dołączenia danego ucznia do klasy, został stworzony model *StudentClassRequest* z polami *classsroom_id* i *student_id* (oba klucze obce). *classsroom_id* jest pobierane od ucznia z formularza ("join_classroom.html"), natomiast *student_id* uzupełniane jest automatycznie. 
3. Po udanym zapisaniu informacji w bazie danych uczeń przekierowywany jest do "request_sent.html". 

##### Modyfikowanie klasy

1. W celu umożliwienia nauczycielowi wprowadzania zmian w danych klasy zaimplementowany został widok *ModifyClassroom* dostępny pod adesem 'show-classrooms/display-classroom/modify-classroom/<class_id>' (*modify_classroom.html*) Gdzie w formularzu domyślnie wpisane są aktualne wartości zmiennych (formularz wygląda dokłanie tak jak przy zakładaniu klasy).
2. Po wprowadzaniu zmian i poprawnym zapisaniu ich przez system, nauczyciel zostaje przekierowany do widoku wszystkich klas 'show-classrooms/'.
3. W przypadku niepowdzenia zwracane jest *HttpResponseForbidden*

##### Wyświetlanie klasy

1. Wyświetlenie klasy odbywa się dzięki użyciu klasy ShowClassrooms.
2. W widoku klas pojawiają się klasy przypisane tylko do aktualnie zalogowanego użytkownika serwisu.

##### Usuwanie klasy

1. Po naciśnięciu odpowiedniego przycisku w widoku klasy nauczyciel ma możliwość usunięcia danej klasy - widok *DeleteClassroom* ('show-classrooms/display-classroom/delete-classroom/<class_id>'; nie ma potrzeby podawania niczego, musi ew. potwierdzić swoją decyzję).
2. Po wprowadzaniu zmian i poprawnym zapisaniu ich przez system, nauczyciel zostaje przekierowany do widoku wszystkich klas 'show-classrooms/'.
3. W przypadku niepowdzenia zwracane jest *HttpResponseForbidden*.

##### Dodawanie lekcji w klasie

1. W celu umożliwienia nauczycielowi dodania lekcji w klasie, został stworzony model *Lesson* z polami: *date*, *hour*, *subject*, *descriprion, note, owner, classroom, lesson_done* (odpowiednio typu: DateField, TimeField, CharField, CharField, CharField, klucz obcy typu TeacherProfile, klucz obcy typu Classroom i BooleanField).
2. pod adresem 'show-classrooms/display-classroom/<classroom_id>/add-lesson' został dodany  template 'add_lesson.html', który umożliwia wypełnienie pól *date*, *hour*, *subject*, *descriprion, note oraz *lesson_done*. Reszta pól uzupełniana jest automatycznie w widoku widok *AddLesson()*, w którym to jest tworzony i zapisywany rekord lekcji.
3. Po udanym utworzniu lekcji nauczyciel zostaje przekierowny na widok klasy, w której utworzył lekcję.
4. Jeśli tworzenie lekcji się nie powiedzie zostaje wyświetlony odpowiedni komunikat.

##### Powiadomienia

1. W celu implementacji funkcji powiadomień została zainstalowana biblioteka django-notifications-hq
2. Powyższa biblioteka dostarczała podstawową funkcjonalność powiadomień, jednak w celu dostosowania ich działania do tworzonej aplikacji niezbędne okazało się dokonanie rozbudowy
3. Została dodana ścieżka *user/notifications*, kierująca użytkownika do widoku jego powiadomień za ostatnie 7 dni
4. Został dodany endpoint *api/user/notifications/* zwracający w formacie JSON powiadomienia za ostatnie 7 dni włącznie
5. Zostały dodane funkcje napisane w Javascript wysyłające co 10 sekund request GET na endpoint z punktu 4 i aktualizujące listę powiadomień
6. Została dodana funkcja w Javascript wysyłająca po kliknięciu w powiadomienie request na endpoint *notifications/mark-as-read/<id_powiadomienia>* w celu oznaczenia powiadomienia jako przeczytane.
7. Zostały dodane klasy widoków AcceptJoinClassroom i RejectJoinClassroom, umożliwiające dodanie ucznia do klasy gdy powiadomienie tego dotyczy

### Front-end

##### Strona startowa

1. Utworzona została strona startowa *index.html*: pasek górny *id=tuiHeader* z przyciskami do logowania *id=loginButton* oraz rejestracji *id=signupButton*. Okno logowania *id=loginWindow* pozwala zalogować się na swoje konto, lub też przejść do strony rejestracji *register.html* lub przypomnieć zapomniane hasło. W tle strony startowej wyświetlany jest pokaz slajdów *id=tui-slideshow* wraz z opisem funkcjonalności oferowanych przez aplikację.
2. Strona rejestracji *register.html* podzielona jest na dwie części: *id=registrationPage1* w której przyszły użytkownik wybiera typ konta oraz *id=registrationPage2* gdzie podawane są dane osobowe: imię, nazwisko, data urodzenia, hasło wraz z jego potwierdzeniem oraz hasło rodzicielskie w przypadku konta rodzicielskiego. Zostało zaimplementowane również automatyczne porównywanie wprowadzanych haseł i wyświetlanie komunikatu, jeśli nie są one identyczne.
3. Strona odzyskiwania hasła *mail_to_remind_password.html* z poziomu strony startowej wygląda następująco: wyświetla się okno *id=passwordChangeWindow*, w którym użytkownik podaje swój adres mailowy. Na adres wysyłany jest link do strony odzyskiwania hasła *password_change.html*, gdzie użytkownik dwukrotnie wpisuje swoje nowe hasło i potwierdza zmianę.
4. Wszystkie powyżej wymienione pliki html znajdują się w folderze *start*.

##### Strona główna (po zalogowaniu) oraz konto użytkownika

5. Na potrzeby interfejsu po zalogowaniu został stworzony plik bazowy o nazwie *main.html* w którym znajduje się pasek górny *id=tuiHeader* wspólny dla wszystkich widoków: powiadomień, harmonogramu, zapisów, klas oraz konta użytkownika. Cały plik style czerpie z pliku *main_styles.css*, który to plik jest w nagłówku wszystkich pozostałych plików.
6. Strona konta użytkownika to plik *account.html*. Główny jej komponent to okno *id=tui-account_box*, w którym można edytować dane użytkownika (przyciskiem *id=editDataButton*), a także zmienić swoje hasło *id=changePasswordButton* oraz usunąć konto *id=deleteAccountButton*. Dwie ostatnie akcje wykonuje się poprzez linka wysłanego na maila.
7. Rozpoczęto implementację strony powiadomień *notification.html* konfigurując okno *id=tui-notification_box*, w którym wyświetlać się będą kafelki powiadomień.

##### Strona powiadomień oraz strona widoku klas

8. Zakończono tworzenie strony powiadomień *id=tui-notification_page* wraz z przykładową templatką powiadomienia *class=notification_sample* dla prośby o dołączenie do klasy (po stronie nauczyciela) oraz dla zaakceptowania prośby o dołączenie do klasy (po stronie ucznia). Strona powiadomień została wykonana responsywnie i będzie poszerzana o kolejne rodzaje powiadomień w kolejnych sprintach.
9. Stworzono ogólny widok wszystkich klas, które prowadzi nauczyciel *class=class_of_teacher* lub klas, do których należy uczeń *class=class_of_student*. Wszystkie klasy zawierają się w kontenerze *class=grid-container id=classesContainer*, który to wraz z *id=classesTopBar* zawiera się w stronie klas *id=tui-classes_page*.

##### Widok tworzenia klasy i dołączania do klasy

10. Tworzenie klasy zawarte jest w pliku z widokiem wszystkich klas *classesTeacher.html* i tak naprawdę jest podwidokiem, o id *id="createNewClassBar"*. Podczas tworzenia nowe klasy uzupełnia się pola nazwa klasy *id="nameOfNewClassCodeInput"* oraz opis klasy *id="descriptionOfNewClassCodeInput"*, a także pola pomocnicze, takie jak maksymalna i minimalna liczba uczniów w klasie oraz data rozpoczęcia i zakończenia klasy.
11. Dołączanie do klasy analogicznie, jest podwidokiem o id *id="joinNewClassBar"* zawartym w pliku *classesStudent.html*. Kod klasy wpisuje się w input o id *id="joinNewClassCodeInput"*.

##### Widok pojedynczej klasy

12. Widok pojedynczej klasy został stworzony w pliku *class.html*, a sama klasa oznaczona jest *id="tui-class_box"*. Informacje, które wyświetlają się w widoku to nazwa i opis klasy (*id="nameOfTheClassBox"* oraz *id="descriptionOfTheClassBox"*), oba te pola są rozwijane na wypadek długości tekstu przekraczającej wysokość elementu. Poniżej zawarte zostały widoki pokazujące listę lekcji przypisanych do klasy *id="listOfClassLessonsBox"*, uczniów dodanych do klasy *id="listOfClassStudentsBox"* oraz informacje o klasie *id="classInfoContainer"*.
13. Zaimplementowano również buttony przeznaczone do edycji pól klasy *id="editClassButton"*, do usunięcia uczniów z klasy *id="deleteStudentsFromClassButton"*, a także do usunięcia samej klasy *id="deleteClassButton"*. Z poziomu pojedynczej klasy można też utworzyć nową lekcję, a służy do tego button *id="addLessonButton"* zawarty w podwidoku listy lekcji, w elemencie *id="listOfClassLessonsBox"*.

##### Tworzenie i widok lekcji

14. Po klinięciu buttona DODAJ LEKCJĘ *id="addLessonButton"* ukazuje się wysuwany widok tworzenia lekcji *id="newLessonView"*.
15. Przy tworzeniu lekcji (*id="newLessonBox"*) uzupełnia się w formie (*id="createNewLessonForm"*) odpowiednie pola: tytuł, opis i notatkę do lekcji, a także datę i godzinę rozpoczęcia lekcji w harmonogramie.
16. Widok pojedynczej lekcji został stworzony w pliku *lesson.html*, a sama klasa oznaczona jest *class="tui-lesson_page"*. Powrót do widoku klasy znajduje się w elemencie *id="returnLessonBar"*, natomiast nawigowanie między lekcjami w elemencie *id="navLessonBar*.
17. Wszystkie informacje o lekcji znajdują się w elemencie *id="tui-lesson_box"*. Przesłane materiały wyświetlane są w elemencie *id="filesForTheLessonBox"*, natomiast zadania domowe w *id="homeworkForTheLessonBox"*.
18. Do edycji pól lekcji służy button *id="editLessonButton"*, do dodania materiałów *id="addFileToLessonButton"*, do usunięcia materiałów *id="deleteFileFromLessonButton"*, do dodania zadania domowego *id="addHomeworkToLessonButton"*, do usunięcia zadania domowego *id="deleteHomeworkFromLessonButton"*, a do usunięcia lekcji *id="deleteLessonButton"*.

### Testy

Testy automatyczne realizowane są przy pomocy wbudowanego w Django modułu **django.test**.

Testy sprawdzają podstawy działania aplikacji:

- ładowanie widoków (uzyskiwanie odpowiedniej ścieżki przy pomocy funkcji *reverse*, zwracanie kodu **200**)
- ładowanie poprawnych templates (odpowiedni plik HTML do konkretnego widoku)
- rejestracja przykładowych użytkowników (nauczyciel, uczeń, rodzic z uczniem, zwracanie kodu **302**)
- logowanie przykładowych użytkowników (zwracanie kodu **302** w przypadku powodzenia oraz kodu **200** w przypadku niepowodzenia - kiedy logowanie nie powiedzie się, załadowana zostaje strona logowania, na której wyświetlona jest informacja o niepowodzeniu)
- edytowanie danych przez użytkownika (zwracanie kodu **200** w przypadku powodzenia oraz kodu **403** (odmowa dostępu) w przypadku próby zmiany danych innego użytkownika)
- tworzenie nowej klasy (podanie części danych lub wszystkich możliwych, zwracanie kodu **302** w przypadku powodzenia)
- dołączanie do klasy poprzez wpisanie kodu klasy przez ucznia (zwracanie kodu **200**)
- akceptowanie oraz odrzucanie prośby ucznia o dołączenie do klasy (zwracanie kodu **200** w obu przypadkach)
- modyfikowanie danych klasy przez nauczyciela (zwracanie kodu **302** w przypadku powodzenia)
- usuwanie klasy przez nauczyciela (zwracanie kodu **302** w przypadku powodzenia)
- dodawanie lekcji przez nauczyciela (zwracanie kodu **200**)
- modyfikowanie lekcji przez nauczyciela (zwracanie kodu **302** w przypadku powodzenia)

Testy związane ze stroną główną i użytkownikami (logowanie, rejestracja, edycja profilu) znajdują się w pliku *users/tests.py*, natomiast związane z powiadomieniami, klasami i lekcjami w pliku *lessons/tests.py*. W pliku *calendar-google/tests.py* znajdują się testy związane z wyświetlaniem kalendarza.



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

### Google API
Tutorex jest połączony z Google API Cloud oraz Google API Calendar. W pliku tutorex/Google_cloud.py znajdują się funkcje odpowiedzialne za połączenie z serwerami zewnętrznej aplikacji. Na portalu https://console.cloud.google.com/ i po zalogowaniu się na konto google - tutorex.helpdesk@gmail.com jest możliwa zmiana ustawień uprawnień i przekierowań URL.
Kalendarz jest wyświetlany dzięki odpowiednim linkom i widokom utworzonym w Django. Odpowiednie pliki odpowiedzialne za to znajdują się w folderze calendar_google.

### Ciągła integracja i dostarczanie

Kod aplikacji jest przechowywany na prywatnym repozytorium w serwisie Github.com, do którego mają dostęp wszyscy członkowie zespołu deweloperskiego. W ramach ciągłej integracji w serwisie Github została przeprowadzona konfiguracja testów automatycznych - są one uruchamiane przy każdym **push** oraz **pull request** na branch **master** (wykorzystany wbudowany moduł Actions).

Utworzone zostały dwie wersje aplikacji:

- tutorex-test.herokuapp.com - aplikacja dla zespołu do pracy nad projektem
- tutorex-app.herokuapp.com - aplikacja właściwa, na którą będą trafiały kolejne wydania aplikacji (alpha, beta etc) i która jest przeznaczona dla klientów

Deployment aplikacji jest przeprowadzony przy użyciu serwisu Heroku, który został połączony z repozytorium w serwisie Github (branch **master** dla aplikacji testowej oraz branch **deploy** dla aplikacji właściwej). Proces dostarczania aplikacji został skonfigurowany w następujący sposób:

1. **push** na odpowiedni branch
2. uruchomienie testów automatycznych w serwisie Github
3. jeżeli wszystkie testy zostały zakończone pozytywnie, uruchomiona zostaje kompilacja kodu w serwisie Heroku (jeżeli któryś z testów nie powiódł się kolejne kroki nie są wykonywane)
4. jeżeli kompilacja się powiodła, nowy build zostaje załadowany na odpowiedniej domenie (w przypadku niepowodzenia na stronie zostaje poprzedni poprawnie skompilowany build oraz zostaje wysłane powiadomienie o niepowodzeniu na email jednego z członków zespołu).