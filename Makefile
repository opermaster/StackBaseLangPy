output.c:
	python .\src\main.py

output: output.c
	gcc .\build\stack.c -o .\build\output .\build\output.c &.\build\output
