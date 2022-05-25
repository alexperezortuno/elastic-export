# pylastic-report

| Flag | Default | Description |
|---|---| --- |
| -h or --help |   | Show this help message and exit. |
| -u or --h | | |

###Example commands to run:

````shell
python main.py -u localhost -i testing-* -p 9200 -g 2022-03-01T00:00:00 -l 2022-03-30T23:59:59 -q "i_test:*TEST*"
````

### To build binary executable in linux:

````shell
make
````

or run command:

````shell
pyinstaller -F --clean --noconfirm -n pylastic_report main.py
````

and copy the binary to the /usr/bin folder.
