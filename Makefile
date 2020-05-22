behave:
	pipenv run behave tests/behave

behave-debug:
	pipenv run behave tests/behave --logging-level=DEBUG --no-logcapture
