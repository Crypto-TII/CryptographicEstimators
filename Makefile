# Docker variables
IMAGE_NAME = estimators-lib:latest
DOCUMENTATION_PATH = $(shell pwd)
SAGE = sage
PACKAGE = cryptographic_estimators
UNAME := $(shell uname -m)

tools:
	@sage -python -m pip install setuptools==63.0 wheel==0.38.4 sphinx==5.3.0 furo prettytable scipy pytest pytest-xdist python-flint 

lib:
	@python3 setup.py install && sage -python -m pip install .

install:
	@make tools && make lib

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

add-copyright:
	@python3 scripts/create_copyright.py

add-estimator:
	@python3 scripts/create_new_estimator.py && make add-copyright

append-new-estimator:
	@python3 scripts/append_estimator_to_input_dictionary.py

### Docker commands

generate-documentation:
	@docker exec container-for-docs make doc

mount-volume-and-run: 
	@docker run --name container-for-docs --mount type=bind,source=${DOCUMENTATION_PATH}/docs,target=/home/cryptographic_estimators/docs -d -it ${IMAGE_NAME} sh

docker-build-x86:
	@docker build -t ${IMAGE_NAME} .

docker-build-m1:
	@docker buildx build -t ${IMAGE_NAME} --platform linux/x86_64 .

docker-build:
ifeq ($(UNAME), arm64)
	@make docker-build-m1
else
	@make docker-build-x86
endif 

docker-run: docker-build
	@docker run -it --rm ${IMAGE_NAME}

stop-container-and-remove:
	@echo "Cleaning any previous container...."
	@docker stop $(container_name) || true
	@docker rm $(container_name) || true

docker-doc: docker-build
	@make stop-container-and-remove container_name="container-for-docs" \
		|| true
	@make mount-volume-and-run && make generate-documentation && make stop-container-and-remove container_name="container-for-docs"

docker-test: CONTAINER_NAME := "sage-doctests-container"
docker-test: docker-build
	@make stop-container-and-remove container_name=${CONTAINER_NAME} \
		|| true
	@echo "Running Sage doctests..."
	@docker run --name ${CONTAINER_NAME} --rm -it ${IMAGE_NAME} sh -c "\
		sage -t --long --timeout 3600 --force-lib \
		cryptographic_estimators/DummyEstimator/ \
		cryptographic_estimators/LEEstimator/ \
		cryptographic_estimators/MAYOEstimator/ \
		cryptographic_estimators/MREstimator/ \
		cryptographic_estimators/PEEstimator/ \
		cryptographic_estimators/PKEstimator/ \
		cryptographic_estimators/UOVEstimator/ \
		# cryptographic_estimators/base_algorithm.py \
		# cryptographic_estimators/base_constants.py \
		# cryptographic_estimators/base_estimator.py \
		# cryptographic_estimators/base_problem.py \
		# cryptographic_estimators/estimation_renderer.py \
		# cryptographic_estimators/helper.py \
		# cryptographic_estimators/SDEstimator/ \
		# cryptographic_estimators/MQEstimator/ \
		# cryptographic_estimators/SDFqEstimator/ \
		# cryptographic_estimators/RegSDEstimator/ \
		" \
		&& echo "All tests passed." \
		|| echo "Some test have failed, please see previous lines."


docker-testfast: CONTAINER_NAME := "sage-doctests-container"
docker-testfast: docker-build
	@make stop-container-and-remove container_name=${CONTAINER_NAME} \
		|| true
	@echo "Running short Sage doctests..."
	@docker run --name ${CONTAINER_NAME} --rm -it ${IMAGE_NAME} sh -c "\
		sage -t --timeout 3600 --force-lib \
		cryptographic_estimators/DummyEstimator/ \
		cryptographic_estimators/LEEstimator/ \
		cryptographic_estimators/MAYOEstimator/ \
		cryptographic_estimators/MREstimator/ \
		cryptographic_estimators/PEEstimator/ \
		cryptographic_estimators/PKEstimator/ \
		cryptographic_estimators/UOVEstimator/ \
		# cryptographic_estimators/base_algorithm.py \
		# cryptographic_estimators/base_constants.py \
		# cryptographic_estimators/base_estimator.py \
		# cryptographic_estimators/base_problem.py \
		# cryptographic_estimators/estimation_renderer.py \
		# cryptographic_estimators/helper.py \
		# cryptographic_estimators/SDEstimator/ \
		# cryptographic_estimators/MQEstimator/ \
		# cryptographic_estimators/SDFqEstimator/ \
		# cryptographic_estimators/RegSDEstimator/ \
		" \
		&& echo "All tests passed." \
		|| echo "Some test have failed, please see previous lines."

docker-doctests: CONTAINER_NAME := "pytest-container"
docker-doctests: docker-build
	@make stop-container-and-remove container_name=${CONTAINER_NAME} \
		|| true
	@echo "Running doctests..."
	@docker run --name ${CONTAINER_NAME} --rm ${IMAGE_NAME} sh -c "\
		pytest --doctest-modules -n auto -vv -s \
		cryptographic_estimators/SDEstimator/ \
		cryptographic_estimators/MQEstimator/ \
		cryptographic_estimators/SDFqEstimator/ \
		cryptographic_estimators/base_algorithm.py \
		cryptographic_estimators/base_constants.py \
		cryptographic_estimators/base_estimator.py \
		cryptographic_estimators/base_problem.py \
		cryptographic_estimators/estimation_renderer.py \
		cryptographic_estimators/helper.py \
		cryptographic_estimators/RegSDEstimator/ \
		# cryptographic_estimators/DummyEstimator/ \
		# cryptographic_estimators/LEEstimator/ \
		# cryptographic_estimators/MAYOEstimator/ \
		# cryptographic_estimators/MREstimator/ \
		# cryptographic_estimators/PEEstimator/ \
		# cryptographic_estimators/PKEstimator/ \
		# cryptographic_estimators/UOVEstimator/ \
		"

docker-doctests-fast: CONTAINER_NAME := "pytest-container"
docker-doctests-fast: docker-build
	@make stop-container-and-remove container_name=${CONTAINER_NAME}
	@echo "Running short doctests..."
	@docker run --name ${CONTAINER_NAME} --rm -it ${IMAGE_NAME} sh -c "\
		pytest --skip-long-doctests  --doctest-modules -n auto -vv cryptographic_estimators/"

docker-kat-tests: CONTAINER_NAME := "pytest-container"
docker-kat-tests: docker-build
	@make stop-container-and-remove container_name=${CONTAINER_NAME}
	@echo "Running KAT..."
	@docker run --name ${CONTAINER_NAME} --rm ${IMAGE_NAME} sh -c "\
		pytest --doctest-modules -n auto -vv \
		tests/test_kat.py \
		"

docker-functional-tests: CONTAINER_NAME := "pytest-container"
docker-functional-tests: docker-build
	@make stop-container-and-remove container_name=${CONTAINER_NAME}
	@echo "Running functional tests..."
	@docker run --name ${CONTAINER_NAME} --rm ${IMAGE_NAME} sh -c "\
		pytest --doctest-modules -n auto -vv \
		tests/test_sd.py \
		tests/test_mq.py \
		"

docker-tests-all: CONTAINER_NAME := "pytest-container"
docker-tests-all: docker-functional-tests docker-doctests docker-kat-tests

docker-pytest-cov:
	pytest -v --cov-report xml:coverage.xml --cov=${PACKAGE} tests/

docker-generate-kat:
	@docker run --name kat-container -v ./tests:/home/cryptographic_estimators/tests --rm ${IMAGE_NAME} sh -c \
		"sage tests/external_estimators/generate_kat.py"
	@make docker-build
