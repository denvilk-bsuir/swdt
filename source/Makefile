web-build:
	docker build --tag testing-sys-web web/

web-run:
	docker run -p 8000:8000 testing-sys-web

make_i18n:
	cd web && django-admin makemessages -l ru_RU -l en_US

update_i18n:
	cd web && django-admin compilemessages