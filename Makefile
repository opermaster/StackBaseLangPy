all: first second third

first.c:
	python .\src\main.py .\examples\first.txt .\build\first.c

first: first.c
	gcc .\lib\stack.c -o .\build\first .\build\first.c  -I .\lib\
	&.\build\first

second.c:
	python .\src\main.py .\examples\second.txt .\build\second.c

second: second.c
	gcc .\lib\stack.c -o .\build\second .\build\second.c  -I .\lib\
	&.\build\second

third.c:
	python .\src\main.py .\examples\third.txt .\build\third.c

third: third.c
	gcc .\lib\stack.c -o .\build\third .\build\third.c  -I .\lib\
	&.\build\third
