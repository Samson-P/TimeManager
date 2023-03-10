# TimeManager
An application for calculating the time spent in a certain type of activity with the possibility of primary analysis, demonstration and export of statistics

Техническое задание:

Проект был создан в 2020 г.

Разделим все посчитанное время на:
	education
	work experience (execution)

При сохранении круга нужно указать:
	W_edu 
	W_exe 

Это веса, показывающие, какая часть времени была затрачена на реализацию конструктивных функций мозга, связанных с формулировкой мысли, формирование абстрактных объектов в голове, учебу. Вообще говоря, на составление новых связей в мозге или на создание, генерирование новых объектов. Какая часть времени была затрачена на исполнение, применение полученных навыков, на отработку тех ментальных механизмов, которые были натренированы в процессе обучения.

Пример. Цель – написать TM. Задачи:
	Продумать структуру приложения, вид графического интерфейса, обработку введенных в интерфейс данных, представление данных, изучение соответствующих плану библиотек языка python

	Написание программы (кодинг) – формализация абстрактных мыслей в программные/материальные единицы (временной интервал – начало отсчета времени, конец отсчета; род деятельности – текст (название рода деятельности); придуманные возможности интерфейса – графическая модель его вида), использование скиллов по программированию (работа со средой разработки PyCharm, представление придуманных объектов в форме питоновских объектов, работа с объектами посредству кода), 

Эти задачи могут решаться в параллель, важно в конце адекватно расставить веса для каждого процесса. Допустим, я программировал 6 часов, 1/3 времени по ощущениям я потратил на решение первой задачи. Остальные 2/3 времени я потратил на формализацию идей и написание программы. Итого в скилл у меня запишется 4 часа (чем больше я программирую, тем лучше это будет получаться), в учебу пойдет 2 часа (чем больше я думаю, придумываю, тем выше станет моя обучаемость).
Это можно реализовать ползунком. 

При чем процесс применения/исполнения/использования знаний/умений/навыков не полностью привязан к процессу обучения. Я затратил какую-то часть времени на придумывание проекта, но когда я его реализовывал, писал, я мог использовать знания, полученные задолго до того.
Оформим мысль:
 
Представление статистики по проекту (гипотетически):
 	По оси OY откладывается гистограмма, высота столба – время (сума кругов за сутки) посвященная проекту.
Еще одно представление данных о затраченном времени (пусть срок – полгода):
 
Видно, что execution в большинстве преобладает. Однако рывками education все-таки отнимает внушительные части. Виден спад деятельности в середине. Там education сравнимо с нулем, а execution сильно упало, может быть там были каникулы, какой-то перерыв, или упадок сил. В конце виден взрыв деятельности. При чем education отнимает почти половину, это может говорить о начале интенсивной учебы и скорее всего там начинаются новые проекты.
