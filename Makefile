# Docker variables
image_name=cryptographic-estimators:latest
documentation_path=$(shell pwd)

tools:
	@sage -python -m pip install setuptools==63.0 wheel==0.38.4 sphinx==5.3.0 furo prettytable scipy

lib:
	@sage setup.py install && sage -python -m pip install .

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
	@python3 scripts/create_new_estimator.py

run-deatach:
	@docker run -d --name container-for-docs -it cryptographic-estimators sh 

stop-container:
	@docker stop container-for-docs

generate-documentation:
	@docker exec container-for-docs make doc

mount-volume: 
	@docker run --mount type=bind,source=${documentation_path}/docs,target=/home/cryptographic_estimators/docs cryptographic-estimators:latest

docker-doc:
	@make mount-volume && make run-deatach && make generate-documentation && make stop-container