
script.c: main.py
	python main.py

script: script.c
	gcc -o script script.c
