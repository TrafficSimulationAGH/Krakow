# Obwodnica IV
Symulacja ruchu drogowego na obwodnicy IV Krakowa.

# Tutorial GIT
Ogólne zasady, konwencje i tipy:
- repozytorium (repo) - projekt przechowywany w folderze, gdzie znajduje się folder ukryty `.git`;
- branch - gałąź, domyślnie `master`, pozwala na prowadzenia równoległych wersji projektu; każdy posiada swoją gałąź o nazwie `dev/[imie]`, a co jakiś czas będziemy aktualizować postępy na `master`;
- commit - zapisany stan plików; element historii repo; staramy się utrzymywać zasadę: 1 etap pracy 1 commit (np. dodano rozdział dokumentacji / rozszerzono opis);
- stage - pliki przygotowane do dodania jako commit;

Polecenia:
- `git --help` - pomoc; można łączyć np. `git clone --help`; wersja kompaktowa pomocy `git -h` (nie zawsze dostępna);
- `git clone [adres url/ssh] [opcjonalnie: folder docelowy]` - zielony przycisk u góry strony pozwala zmieniać link między SSH a HTTP; SSH używamy jeśli skonfiurowaliśmy klucz .pub `ssh-genkey` w ustawieniach konta github; HTTP zadziała wszędzie, ale wymaga podania hasła przy każdym dostępie do repozytorium zdalnego;
- `git status` - podsumowanie aktualnych zmian w repo; wyświetla aktualny stage;
- `git add .` - dodaje wybrane foldery i pliki do stage; `.` oznacza aktualny folder;
- `git commit` - zatwierdź zmiany; pojawi się edytor z podsumowaniem i poprosi o wpisanie komentarza, tytułu commita;
- `git branch` - lista branchy; aktualna zaznaczona `*`;
- `git checkout <cel>` - zmień branch lub przeskocz w historii repo do innego commita; tego używamy przede wszystkim do zmiany branch, zmiana commita dla zaawansowanych;
- `git pull origin <branch>` - pobierz zdalne zmiany z branch; **UWAGA:** trzeba się upewnić, że pobieramy ten sam branch, na którym jesteśmy, w innym przypadku zaktualizujemy aktualny o zmiany z innego i trudno to cofnąć, postępujemy świadomie;
- `git push origin <branch>` - wyślij zmiany na zdalne repo z branch; **UWAGA:** jak wyżej;

> Wszystkie polecenia wykonujemy w folderze projektu!

Pozostałe polecenia dodam w swoim czasie, tyle wystarczy, aby zacząć.

