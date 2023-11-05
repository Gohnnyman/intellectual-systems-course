# Лабораторна робота #1 "База знань"

Запускати наступним чином:

``` bash
python3 main.py <path-to-facts> <path-to-rules>
```

Далі програма в stdin очікує предикат у вигляді рядка, у відповідь 
вона виведе в stdout зміні для яких цей предикат виконується, приклад:

``` bash
python3 main.py resources/facts.txt resources/rules.txt
hasChild
	 family:JohnDoe  ->  family:TomDoe
	 family:JaneDoe  ->  family:TomDoe
	 family:JohnDoe  ->  family:EmilySmith
	 family:JaneDoe  ->  family:EmilySmith
	 family:TomDoe  ->  family:SaraDoe
```

Для завершення програми введіть `exit`
