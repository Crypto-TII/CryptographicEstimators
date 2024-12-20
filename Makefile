## Docker variables
IMAGE_NAME = estimators-lib:latest
DOCUMENTATION_PATH = $(shell pwd)
PACKAGE = cryptographic_estimators
MACHINE_ARCHITECTURE := $(shell uname -m)

DOCTESTS_COMMAND = pytest --doctest-modules -n auto -vv $(PACKAGE)/
DOCTESTS_FAST_COMMAND = pytest --skip-long-doctests  --doctest-modules -n auto -vv $(PACKAGE)/
KAT_TESTS_COMMAND = pytest -n auto -vv tests/test_kat.py
FUNCTIONAL_TESTS_COMMAND = pytest --doctest-modules -n auto -vv \
													 tests/test_sd.py \
													 tests/test_mq.py


## Local commands
install:
	@pip3 install -e .

doctests-fast:
	@${DOCTESTS_FAST_COMMAND}

doctests:
	@${DOCTESTS_COMMAND}

kat-tests:
	@${KAT_TESTS_COMMAND}

functional-tests:
	@${FUNCTIONAL_TESTS_COMMAND}

tests-all: functional-tests doctests kat-tests

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
ifeq ($(MACHINE_ARCHITECTURE), arm64)
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

docker-doctests: CONTAINER_NAME := "pytest-container"
docker-doctests: docker-build
	@make stop-container-and-remove container_name=${CONTAINER_NAME} \
		|| true
	@echo "Running doctests..."
	@docker run --name ${CONTAINER_NAME} --rm ${IMAGE_NAME} sh -c "${DOCTESTS_COMMAND}"

docker-doctests-fast: CONTAINER_NAME := "pytest-container"
docker-doctests-fast: docker-build
	@make stop-container-and-remove container_name=${CONTAINER_NAME} \
	    || true
	@echo "Running short doctests..."
	@docker run --name ${CONTAINER_NAME} --rm -it ${IMAGE_NAME} sh -c "${DOCTESTS_FAST_COMMAND}"

docker-kat-tests: CONTAINER_NAME := "pytest-container"
docker-kat-tests: docker-build
	@make stop-container-and-remove container_name=${CONTAINER_NAME} \
		|| true
	@echo "Running KAT..."
	@docker run --name ${CONTAINER_NAME} --rm ${IMAGE_NAME} sh -c "${KAT_TESTS_COMMAND}"

docker-functional-tests: CONTAINER_NAME := "pytest-container"
docker-functional-tests: docker-build
	@make stop-container-and-remove container_name=${CONTAINER_NAME} \
		|| true
	@echo "Running functional tests..."
	@docker run --name ${CONTAINER_NAME} --rm ${IMAGE_NAME} sh -c "${FUNCTIONAL_TESTS_COMMAND}"

docker-tests-all: CONTAINER_NAME := "pytest-container"
docker-tests-all: docker-functional-tests docker-doctests docker-kat-tests

docker-pytest-cov:
	pytest -v --cov-report xml:coverage.xml --cov=${PACKAGE} tests/

docker-generate-kat: docker-build
	@docker run --name kat-container -v ./tests:/home/cryptographic_estimators/tests --rm ${IMAGE_NAME} sh -c \
		"sage tests/external_estimators/generate_kat.py"
	@make docker-build

