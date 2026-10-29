# Docker
## Start:
First make sure you create the docker image via:
```bash
make docker-fuzzing
```

Next you can run it via:
```bash 
docker run --rm cf-fuzzer ./tests/fuzzing/fuzz.py --sd 
```
