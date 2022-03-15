# cltl-template

This repo is a template for the other services.
Each service has its own repo and a Dockerfile.
Their structure will inherit from this repo.

## Start from this template

To start from this template:
* Create a new empty repository on github with name <MODULE_NAME>.
* Clone the repository
  * To add it as git submodule run
    
        git submodule add --name <MODULE_NAME> https://github.com/leolani/cltl-template.git <MODULE_NAME>
        git submodule set-url <MODULE_NAME> <REMOTE_URL>
  
  * or clone this repository

        git clone https://github.com/leolani/cltl-template.git 

    Reomve the old remote:

        git remote remove origin
    
    Add the new emtpy repository and push the main branch:
    
        git remote add origin <REMOTE_URL>
        git push -u origin main

* Add dependencies on libraries to `setup.py`
* Add dependencies on other components to the makefile.
* Rename the python module from `template` to the desired MODLE_NAME.
* Add the component as dependency to the app makefile

## For a typical Python component

### API

Create an API with domain data classes and an interface providing the functionality of the component.

Use *dataclasses* for the domain objects and avoid custom methods. This makes it possible to deserialize
to `SimpleNamespace` objects. Otherwise you eventually need to use a custom deserializer to convert from
JSON inputs to Python class instances. 

### Command line

Create an main class that let's you invoke your service as Pyhton script from the command line that can also
be used to run it inside a Docker container.

### Python package

Create a library package with at your API, implementation and service. 
In setup.py specify only dependencies of the API as required, and add dependencies of implementation
and service as extra requirements. Like this the API can be used without adding unnecessary dependencies
for the user of the API.

When using the package in an other component, specify the additional dependency sets with

    cltl-template[impl,service]

in the `requirements.txt` of that component if needed.

### Docker image

Create a Docker image that runs your compoenent, including the required REST endpoints/Event handlers.

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- LICENSE -->
## License

Distributed under the MIT License. See [`LICENSE`](https://github.com/leolani/cltl-combot/blob/main/LICENCE) for more information.


<!-- CONTACT -->
## Authors

* [Taewoon Kim](https://tae898.github.io/)
* [Thomas Baier](https://www.linkedin.com/in/thomas-baier-05519030/)
* [Selene Báez Santamaría](https://selbaez.github.io/)
* [Piek Vossen](https://github.com/piekvossen)
