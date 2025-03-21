back_run:
	flask --app back/tree run

front_run:
	npm start --prefix ./front

back_test:
	pytest back/
