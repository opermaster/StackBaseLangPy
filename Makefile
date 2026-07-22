all: first second third forth six seven

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

forth.c:
	python .\src\main.py .\examples\forth.txt .\build\forth.c

forth: forth.c
	gcc .\lib\stack.c -o .\build\forth .\build\forth.c  -I .\lib\

fifth.c:
	python .\src\main.py .\examples\fifth.txt .\build\fifth.c

fifth: fifth.c
	gcc .\lib\stack.c -o .\build\fifth .\build\fifth.c  -I .\lib\

six.c:
	python .\src\main.py .\examples\six.txt .\build\six.c

six: six.c
	gcc .\lib\stack.c -o .\build\six .\build\six.c  -I .\lib\
	&.\build\six

seven.c:
	python .\src\main.py .\examples\seven.txt .\build\seven.c

seven: seven.c
	gcc .\lib\stack.c -o .\build\seven .\build\seven.c  -I .\lib\

eight.c:
	python .\src\main.py .\examples\eight.txt .\build\eight.c

eight: eight.c
	gcc .\lib\stack.c -o .\build\eight .\build\eight.c  -I .\lib\
	&.\build\eight
