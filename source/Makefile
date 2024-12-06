web-build:
	docker build --tag testing-sys-web web/

web-run:
	docker run -p 8000:8000 testing-sys-web

make_i18n:
	cd web && django-admin makemessages -l ru_RU -l en_US

update_i18n:
	cd web && django-admin compilemessages

start_rabbit:
	export UID=$(id -u)
	export GID=$(id -g)
	docker-compose -f docker-compose.dev.yaml up rabbitmq

build:
	docker build --tag ts-web web/
	docker build --tag ts-runner runner/

runner-run:
	docker-compose -f docker-compose.dev.yaml up runner