Bot został stworzony na przeglądarkę mozilla firefox, w systemie linux ubuntu 20.04, pisany w python wersji 3.8.
# Uruchamianie
``./run`` lub przez Controller.py
# Instalacja
``./build `` - instaluje poniższe biblioteki, należy jeszcze samodzielnie
 zainstalować [_geckodriver_](https://github.com/mozilla/geckodriver/releases)

### Biblioteki  
```pip install pyrebase```
```pip install selenium```
```pip install PyQt5```

## Geckodriver ( 3 czerwiec 2020).
Jedynym problem jest Geckodriver (dla firefoxa).
W module features znajduje się geckodriver w wersji 0.26 dla aktualnie najnowszej wersji firefoxa 76.0.1 (64-bit)

##### Instrukcja geckodriver :
1. Należy znaleźć i pobrać najnowszą wersję sterownika
 [geckodriver newest version](https://github.com/mozilla/geckodriver/releases), przykładowo:

    ```wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz```
    
2. Następnie rozpakować

    ```tar -xvzf geckodriver*```
3. Nadać prawa pliku wykonywalnego

    ``chmod +x geckodriver``
4. Dodać ścieżkę sterownika do PATH

    ``export PATH=$PATH:/path-to-extracted-file/.``

[ASK UBUNTU POMOCNY LINK GECKODRIVER](https://askubuntu.com/questions/870530/how-to-install-geckodriver-in-ubuntu)

## Campaign - ID
Aby zdobyć campaign- id nadchodzącej wyprzedaży, 
należy znaleźć ją w sekcji " Wkrótce u nas "
 pojawiającej się po zalogowaniu na stronie zalando longue.
 Kliknąć prawym przyciskiem myszy i wybrać opcję inspect element. Następnie w source code należy odszukać ID.
Jest oznaczone na poniższym zdjęciu.
![Alt text](features/campaign_id_instruction.png?raw=true "Title")

## Krótki opis stanu projektu na:


# 2020.04.26 po I tygodniu

Zacznę od ogólnego streszczenia problemu. (drop - wyprzedaż, zrzut ciuchów jednej marki).
Istnieją różne strony, które oferują zgrupowania takich dropów, np zalando ma swoją stronę zajmującą się takimi sprawami - zalando-longue.
Działa to na zasadzie, że np 5 dni wcześniej jest ogłoszenie mailowe, że drop ciuchów marki Ralph Lauren ma być o 6:00 rano. Tylko, co w tym takiego ciekawego i w czym tkwi problem?
W zasadzie są to często są bardzo duże zniżki nawet do 80%. Buty marki vans warte 300 zł można było kupić za 70zł.
Problem tkwi w tym, że nie tylko my wiemy o tych dropach i wszystkie te przedmioty sprzedają się w ciągu kilku-kilkunastu minut, dzieje się tam istne szaleństwo, rozmiary znikają w mgnieniu oka.
Jedną z (według mnie) ciekawych solucji jest napisanie Shopping Bota.
Bot miałby wchodzić na stronę logowac sie, znajdywać dropa po tagu "Ralph" i teraz przechodzić wszystkie towary i sprawdzać czy są zgodne z  oczekwianiami
np "zielona","koszula" ,"ralph" ,"L". Program nie musi nic kupować teoretycznie, dodaje akceptowalne przedmioty do koszyka, w którym może przedmiot egzystować (chyba z pół godziny).
Wtedy po 10-15 minutach botowania wchodzę na swoje konto do koszyka i selekcjonuje przedmioty, które chcę mieć lub nie.
Wiem, że to raczej nielegalne, ale istnieją też różne grupy na facebook'u, w których można zarabiać na tzw. proxy tzn, że przedmiot z koszyka sprzedaje się np 50zł drożej,
bo jest już niedostępny w zalando -longue, a w normalnej cenie ten towar jest wart 2x więcej, lub jest dla kogoś wyjątkowy.
W takim dropie wtedy bierze się wszystko co potencjalnie jest interesujące.
Wrzuca się rzeczy z koszyka jako post na grupę i wtedy świadomie ludzie kupują pośrednio te przedmioty przez np. mnie (proxy) 50zł drożej wiedząc po ile były na zalando.

Podkreślam, że w moim przypadku taka sytuacja nigdy nie miała miejsca, ale wiem że tak się dzieje:).

Bota też można upgradować w rózne sposoby,
- zamiast jednego odpalic kilka,
- jeden bot na kazda strone,
- zmodyfikowac o odpalanie go zdalnie
- poszerzyć o strony zagraniczne jak ASOS
- ogólny monitoring maili od zalando longue
- ustawianie automatyczne bota na  daty z maili,
- prosty interfejs graficzny
Modyfikacji i usprawnień można wymyślić naprawdę wiele ciekawych rozszerzeń.

Ogólnie:
 na pewno mamy zamiar wykorzystać
- _Selenium_,
- _geckodriver do firefox'a
- pięknie wszystko opiszemy w readme, aby każdy mógł skorzystać
- BeautifulSoup 4 do badania struktury html, bs4
- PyQt5 - interfejs graficzny
- pyvirtualdisplay otwiranie przeglądarki w tle. (silent mode)
- smtplib do wysyłania maili

i pewnie wiele innych ,o których się dowiemy na drodze projektowej.


# 2020.05.03 po II tygodniu

- Głębsza analiza struktur Zalando,
- opanowanie podstawowej teorii, dokumentacji Selenium,
- logowanie na stronę 
- wyłączanie irytujących bannerów.

# 2020.05.10 po III tygodniu
Główne (schmeta wersja beta) okno GUI w PyQt5, drobne zapoznanie z PyQt5.
Obsługa błędów przy :
- nie znalezieniu elementu,
- błąd ładowania strony,
Specyfikacja przedmiotów. :-
- selekcja marek
- selekcja rozmiarów
- selekcja kategorii(Struktury):
	- single 2bQSu
	- multiple 2bQSu
	- single 23fgc
- funkcja wysyłająca maile informujące



# 2020.05.17 po IV tygodniu

Zakończony został frontend, zostały drobne szlify i funkcjonalności.
Główne okno zostało zupełnie zmienione, stare było mało przemyślane.
Przenalizowanie ponowne strategii dodawania przedmiotów do koszyka.( bruteforce)
Zapewniona została komunikacja pomiędzy botem a interfejsem.

- panel logowania
- główne okno interfejsu
- controller do komunikacji pomiędzy oknami
- dynamiczne listy zapewniające możliwość filtrowania
- ikony aplikacji

Doszliśmy do większych lub mniejszych zmian w strukturze działania (Zachowania) naszego bota.

 - optymalizację rozmiarów,
 - ustawiwanie cen maksmylanych dla itemu (final version),
 - ustawianie marek (final version),
 - dodawanie przedmiotów do koszyka ( aż do osiągniecią shopping_cart max size)

Wszystko jest na końcowych dotarciach, cały szkielet stoi i działa uniwersalnie( dla wszystkich wyprzedaży).



# 2020.05.24 po V tygodniu

- funkcja pozwalająca na wysyłanie maila informującego o zakończeniu zakupów przez bota lub o osiągnięciu maksymalnego rozmiaru koszyka.( gdyby ktoś na przykład nie chciał czekać przy komputerze lub
limit ilości w koszyku był ogromny i była by równie duża ilość przedmiotów do zakupienia)
- funkcja określająca procentowo skategoryzowanie przedmiotu - rozmiar, cena, marka itd.
- funkcja pozwalająca na czasowe zaprogramowanie bota. (np na uruchomienie jutro o 6:00 rano ).
- dodawanie przedmiotu w wielu rozmiarach. ( L, M bot nie jest już ograniczony do jednego rozmiaru)
- pomysł i implementacja na zmianę sposobu karegoryzowania przedmiotów, na uniezależnienie  bota od struktury dynamicznie zmieniających się kategorii :
    - przy pobieraniu hrefów po wyscrollowaniu itemów pobierąć atrybut .text i sprawdzać czy w liście kategorii z interfejsu znajduje się ten przedmiot
- sygnał informujący o zakończeniu działania botowania
- kolekcjonowanie wszystkich itemów ( dynamiczny koszyk w interfejsie ( nie jestem pewny czy nie jest zbędny))
- UPGRADE projekt.txt ( jest bardziej czytelny! :D)
- modyfikacja gui 
    - dodanie sliderów 
- zaimplementowane zostały funkcjonalności buttonów start,stop
- program teraz działa na osobnych subprocesach? 
    - przy wciskaniu startu osobny procces tworzy nowy startuje nowy obiekt bota, (mozna ich otworzyc kilka
na kilka konfiguracji)
    - stop oprócz terminacji processu wyłącza przeglądarki i czyści zużywane wcześniej zasoby
- potężny clean up w main_window - front
- front -> dokumentacja funkcji

# 2020.05.29 po VI tygodniu 
- podłączenie aplikacji do nierelacyjnej bazy danych ( NoSQL) - firebase, wykorzystujemy bibliotekę pyrebase
- ustalenie struktury przechowywanych dokumentów
- ustalenie reguł w konsoli firebase
- rejestracja kont firebase w interfejsie pyqt5 i walidacja
- logowanie do konta firebase
- obsługa błędów z firebase
- dokumentacja nowo powstałych metod
- zapisywanie konfiguracji w bazie danych dla unikatowego użytkownika
- odczytywanie konfiguracji usera
- komunikacja interfejs - firebase
- readme ++ ( instrukcja) 
- skrypt budujący
- skrypt uruchamiający

## Przydatne linki
[firebase](https://firebase.com)
[pyrebase](https://github.com/thisbejim/Pyrebase/blob/master/README.md?fbclid=IwAR0MfG6lXHNXciGdLzK0AdW7lkIUWmNrHd4jQvUjrV8heOXVvvIu2SK1Usw)
[geckodriver askubuntu](https://askubuntu.com/questions/870530/how-to-install-geckodriver-in-ubuntu)
[selenium](https://selenium-python.readthedocs.io/)
[PyQt5](https://pypi.org/project/PyQt5/)
[Python Scripts](https://realpython.com/run-python-scripts/)
