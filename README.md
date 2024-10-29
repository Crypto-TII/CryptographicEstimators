<div align="center">
    <img src="https://github.com/user-attachments/assets/bbe49f32-5e62-49a7-bb41-b28f1864833d" alt="estimators-logo" width=100 height=100></img>
</div>

# CryptographicEstimators

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Crypto-TII_CryptographicEstimators&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Crypto-TII_CryptographicEstimators)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=Crypto-TII_CryptographicEstimators&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=Crypto-TII_CryptographicEstimators)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=Crypto-TII_CryptographicEstimators&metric=bugs)](https://sonarcloud.io/summary/new_code?id=Crypto-TII_CryptographicEstimators)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=Crypto-TII_CryptographicEstimators&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=Crypto-TII_CryptographicEstimators)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=Crypto-TII_CryptographicEstimators&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=Crypto-TII_CryptographicEstimators)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Crypto-TII_CryptographicEstimators&metric=coverage)](https://sonarcloud.io/summary/new_code?id=Crypto-TII_CryptographicEstimators)

## Introduction 🎉

This library provides bit complexity estimators for cryptographic problems, as well as some cryptographic schemes.
Currently, the implemented estimators are:

- ### Problem Estimators  
  - Multivariate Quadratic
  - Binary Syndrome Decoding
  - Syndrome Decoding over Fq
  - Permuted Kernel
  - Permutation Equivalence
  - Linear Equivalence
  - MinRank 
  - Regular Syndrome Decoding

- ### Scheme Estimators
  - [BIKE](https://bikesuite.org)
  - [MAYO](https://pqmayo.org)
  - [UOV](https://www.uovsig.org)


This project is meant to be run through a terminal. You can also access the estimators through [this](https://estimators.crypto.tii.ae/) user friendly 
and installation-free web application.

---
## Pre-requisites ✔️

You would need to have Python installed in your machine.

---
## Installation 🛠

Once you've Python installed you can go to this project folder and run `make install` in a terminal. This will install
`cryptographic_estimators` library locally. If you encounter some permission error please try again adding `sudo` 
as a prefix.


---
## Running the project ✈️
Open the Python interpreter in a terminal and try importing the library as the following example.
```python
>>> from cryptographic_estimators.SDEstimator import SDEstimator                                                                
>>> SD = SDEstimator(n=15, k=10, w=5)                                                                                                   
>>> SD.table() 
```

---
## Documentation 📝

The documentation can be found online [here](https://crypto-tii.github.io/CryptographicEstimators/). In addition, it can be generated locally by running `make doc`
or through docker by running `make docker-doc`. Once it is generated, open `docs/build/html/index.html` to see the documentation.  

Additionally, we provide a User Guide [here](https://github.com/Crypto-TII/CryptographicEstimators/blob/main/docs/User_Guide.ipynb).

---
## Contributing 🖊️
The aim of this project is to be maintained by the community. We want you to help us grow this library, so please feel free to submit your pull request following the [CONTRIBUTING.md](./docs/CONTRIBUTING.md) document. 

---

## Contact 🖊️
If you need any help about contributing to this project feel free to contact us 
at `cryptographic_estimators at tii.ae`

---

<!--### Usage -->


