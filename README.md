# Shell Emulator with Virtual File System (GUI)

## Описание проекта

**Shell Emulator** — это эмулятор командной строки с графическим интерфейсом, имитирующий работу shell в UNIX-подобной ОС. Эмулятор принимает образ виртуальной файловой системы в формате `.tar` и позволяет пользователям выполнять команды в привычном shell-стиле.

Этот проект создан для работы с виртуальной файловой системой без необходимости распаковки архива пользователем. Логирование всех действий осуществляется в формате CSV, включая пользователя, выполняемые команды и результаты.

## Функциональные возможности

- Графический интерфейс пользователя (GUI) с полем для вывода команд и результатов.
- Работа с виртуальной файловой системой, загружаемой из `.tar`-архива.
- Логирование всех команд в файл CSV с указанием времени, пользователя и результата выполнения.
- Поддержка базовых команд:
  - `ls` — вывод содержимого текущей директории.
  - `cd <path>` — переход в указанную директорию.
  - `exit` — завершение работы эмулятора.
- Дополнительные команды:
  - `tac <file>` — отображение содержимого файла в обратном порядке.
  - `touch <file>` — создание или обновление времени последнего изменения файла.

## Используемые технологии

- **Python 3** — основной язык программирования.
- **Tkinter** — для реализации графического интерфейса.
- **TAR-файлы** — для работы с виртуальной файловой системой.
- **CSV** — для записи лога действий.

## Установка и запуск

### Требования
- Python 3.7+
- Установленная библиотека `Tkinter` (входит в стандартную библиотеку Python).

### Запуск

Для запуска эмулятора используйте следующую команду в терминале:

```bash
python main.py --username user --computername my-computer --tar dz1.tar --log actions_log.csv
```

## Пример использования 
- ![image](https://github.com/user-attachments/assets/bd2ae524-b27f-4d81-a895-9510357e33a3)


