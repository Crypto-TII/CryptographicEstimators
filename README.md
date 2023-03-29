# Cryptographic estimators

## Introduction 🎉

This library provides bit security estimators and asymptotic complexity estimators for cyrptographic problems. So far it covers the binary Syndrome Decoding Problem (SDEstimator) and the Multivaritate Quadratic Problem (MQEstimator).

## Getting Started 🚀
This project is meant to be run through a terminal or inside a docker container.

---
## Pre-requisites ✔️
### Local
You would need to have Sage installed in your machine. For this follow the instructions described [here](https://www.sagemath.org/). 
### Docker
You would need to have Docker installed in your machine. For this follow the instructions described [here](https://www.docker.com/products/docker-desktop/).

---
## Installation 🛠
### Local
Once you've Sage installed you can go to this project folder and run `make install` in a terminal. This will install `cryptographic_estimators` library globally. If you encounter some permission error please try again adding `sudo` as a prefix.

### Docker
If you don’t have sage installed in your machine you can start with our dockerized app. First you will need to have running the DockerDesktop app, then open a new terminal, go to the project folder and run `make docker-build` or if you have Apple Silicon M1 Chip `make docker-build-m1`.

> Note: This process may take up to 15 or 20 minutes depending on your bandwith and  computer capacity.


---
## Running the project ✈️
### Local
Open the Sage interpreter in a terminal and try importing the library as the following example.
```python
sage: from cryptographic_estimators.SDEstimator import SDEstimator                                                                
sage: sd = SDEstimator(15,10,5)                                                                                                   
sage: sd.estimate() 
```
### Docker
Open a terminal and execute `make docker-run` to start the container, then you can run `sage` as if it were in local
```python
root@31d20617c222:/home/cryptographic_estimators# sage
┌────────────────────────────────────────────────────────────────────┐
│ SageMath version 9.0, Release Date: 2020-01-01                     │
│ Using Python 3.8.10. Type "help()" for help.                       │
└────────────────────────────────────────────────────────────────────┘
sage: from cryptographic_estimators.SDEstimator import SDEstimator                                                                                                                 
sage:  
```

---
## Documentation 📝
To generate the documentation locally you can run `make doc` and then open to `/docs/build/html/index.html` to view it. Or you can also generated the documentation through docker via running `make docker-doc`

---
## Contributing 🖊️
The aim of this project is to be maintained by the community. We want you to help us grow this library, so please feel free to submit your pull request following the [CONTRIBUTING.md](./docs/CONTRIBUTING.md) document. Also if you need any help about how to edit the `input_dictionary.json` visit [this playground](https://github.com/Crypto-TII/cryptographic_estimators_ui).
 
---

<!--### Usage -->


