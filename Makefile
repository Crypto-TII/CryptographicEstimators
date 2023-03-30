# Docker variables
image_name=estimators-lib:latest
documentation_path=$(shell pwd)
container_name="container-for-docs"
SAGE=sage

tools:
	@sage -python -m pip install setuptools==63.0 wheel==0.38.4 sphinx==5.3.0 furo prettytable scipy pytest

lib:
	@python3 setup.py install && sage -python -m pip install .

install:
	@make tools && make lib

docker-build:
	@docker build -t ${image_name} .

docker-build-m1:
	@docker buildx build -t ${image_name} --platform linux/x86_64 .

docker-run: 
	@docker run -it --rm ${image_name}

testfast:
	@sage setup.py testfast

testall: install
	@sage setup.py testall

clean-docs:
	@rm -rf docs/build docs/source docs/make.bat docs/Makefile

create-sphinx-config:
	@sphinx-quickstart -q --sep -p TII-Estimators -a TII -l en --ext-autodoc docs

create-rst-files:
	@python3 scripts/create_documentation.py

create-html-docs:
	@sphinx-build -b html docs/source/ docs/build/html

doc:
	@make clean-docs && make create-sphinx-config && make create-rst-files && make create-html-docs

add-estimator:
	@python3 scripts/create_new_estimator.py && make add-copyright

append-new-estimator:
	@python3 scripts/append_estimator_to_input_dictionary.py

stop-container-and-remove:
	@docker stop $(container_name) && docker rm $(container_name)

generate-documentation:
	@docker exec container-for-docs make doc

mount-volume-and-run: 
	@docker run --name container-for-docs --mount type=bind,source=${documentation_path}/docs,target=/home/cryptographic_estimators/docs -d -it ${image_name} sh

docker-doc:
	@make mount-volume-and-run && make generate-documentation && make stop-container-and-remove container_name="container-for-docs"

docker-test:
	@docker run --name container-for-test -d -it ${image_name} sh && docker exec container-for-test sage -t --long -T 3600 --force-lib cryptographic_estimators && docker stop container-for-test && docker rm container-for-test

docker-testfast:
	@docker run --name container-for-test -d -it ${image_name} sh && docker exec container-for-test sage -t cryptographic_estimators && make stop-container-and-remove container_name="container-for-test"

add-copyright:
	@python3 scripts/create_copyright.py

docker-pytest:
	@docker run --name pytest-estimators -d -it ${image_name} sh && docker exec pytest-estimators sh -c "sage --python3 -m pytest -vv && ${SAGE} tests/test_sdfq.sage && ${SAGE} tests/test_le_beullens.sage && ${SAGE} tests/test_le_bbps.sage && ${SAGE} tests/test_pe.sage && ${SAGE} tests/test_pk.sage"  && make stop-container-and-remove container_name="pytest-estimators"
