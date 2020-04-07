# Obwodnica IV
Symulacja ruchu drogowego na obwodnicy IV Krakowa.

## Tutorial Git
Quicktip:
- apply changes `git add .` then `git commit`
- check current branch `git branch`
- update your branch from master `git checkout dev/[imie]` then `git merge master`
- apply your work to master `git checkout master` then `git merge dev/[imie]`
- sync from remote repository `git checkout master||dev/[imie]` then `git pull origin <SOURCE-BRANCH>`
- sync to remote repository `git push origin <BRANCH-TO-SYNC>`

Ogólne zasady, konwencje:
- repozytorium (repo) - projekt przechowywany w folderze, gdzie znajduje się folder ukryty `.git`;
- branch - gałąź, domyślnie `master`, pozwala na prowadzenia równoległych wersji projektu; każdy posiada swoją gałąź o nazwie `dev/[imie]`, postępy przesyłamy sobie przez `master` (czyli jeśli Michal chce od Szymona to `dev/Szymon->master->dev/Michal`);
- commit - zapisany stan plików; element historii repo; staramy się utrzymywać zasadę: 1 etap pracy 1 commit (np. Extended descriptions);
- stage - pliki przygotowane do dodania jako commit;
- używamy języka angielskiego - poza dokumentacją;

Polecenia:
- `git --help` - pomoc; można łączyć np. `git clone --help`; wersja kompaktowa pomocy `git -h` (nie zawsze dostępna);
- `git clone <adres url/ssh> [opcjonalnie: folder docelowy]` - zielony przycisk u góry strony pozwala zmieniać link między SSH a HTTP; SSH używamy jeśli skonfiurowaliśmy klucz .pub `ssh-genkey` w ustawieniach konta github; HTTP zadziała wszędzie, ale wymaga podania hasła przy każdym dostępie do repozytorium zdalnego;
- `git status` - podsumowanie aktualnych zmian w repo; wyświetla aktualny stage;
- `git diff [opcja:HEAD]` - różnice względem ostatniego commitu; opcja HEAD pozwala porównać, jeśli wykonamy już `git add`;
- `git add .` - dodaje wybrane foldery i pliki do stage; `.` oznacza aktualny folder;
- `git commit` - zatwierdź zmiany; pojawi się edytor z podsumowaniem i poprosi o wpisanie komentarza, tytułu commita;
- `git branch` - lista branchy; aktualna zaznaczona `*`;
- `git checkout <cel>` - zmień branch lub przeskocz w historii repo do innego commita; tego używamy przede wszystkim do zmiany branch, zmiana commita dla zaawansowanych;
- `git merge <branch>` - pobierz zmiany z innego branch do aktualnego; staramy się wymieniać tylko z `master`, czyli do master lub od master do siebie;
- `git log` - historia commitów;
- `git pull origin <branch>` - pobierz zdalne zmiany z branch; **UWAGA:** trzeba się upewnić, że pobieramy ten sam branch, na którym jesteśmy, w innym przypadku zaktualizujemy aktualny o zmiany z innego i trudno to cofnąć, postępujemy świadomie;
- `git push origin <branch>` - zaktualizuj branch na githubie; nie powinno zależeć od aktualnego brancha;

> Wszystkie polecenia wykonujemy w folderze projektu!

## Conflicts
Konflikty uniemożliwiają poprawnie zakończyć zmian `commit`. Mogą pojawić się po wykonaniu `pull` lub `merge`, a ich aktualny stan widać po wykonaniu `git status`. Status to podstawowe narzędzie, w którym sprawdzimy czy problem został rozwiązany.

Krok po kroku:
- `git status` - wyświetli pliki skonfliktowane;
- edytujemy skonflikotwane pliki, w zależności od edytora sekcja kolizji może być różnie zaznaczona (tekst / kolor), ja polecam Visual Studio Code, czyścimy ręcznie lub używamy propozycji programu (VS CODE) tak aby został tylko ten kod, który jest poprawny;
- `git add .` - przygotwujemy zmiany;
- `git status` - konflikt powinien być rozwiązany;
- `git commit` - zatwierdzamy naprawioną wersję;

> Pierwszy konflikt na jaki możecie trafić to `doc/proposal/proposal.pdf`. W tym przypadku wystarczy usunąć plik i wygenerować na nowo z poziomu texStudio.

