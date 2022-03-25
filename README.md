# cltl-template

This repo is a template for the other services. Each service has its own repo and a Dockerfile. Their structure will
inherit from this repo.

## Start from this template

To start from this template:

* Create a new empty repository on github with name <MODULE_NAME>.
* Clone the repository
    * To add it as git submodule run

          git submodule add -b --name <MODULE_NAME> https://github.com/leolani/cltl-template.git <MODULE_NAME>
          git submodule set-url <MODULE_NAME> <REMOTE_URL>

    * or clone this repository

          git clone https://github.com/leolani/cltl-template.git 

      Reomve the old remote:

          git remote remove origin

      Add the new emtpy repository and push the main branch:

          git remote add origin <REMOTE_URL>
          git push -u origin main

* Add dependencies on libraries to `setup.py`
* Add dependencies on other components to the makefile, e.g.

        project_dependencies ?= $(addprefix $(project_root)/, cltl-combot emissor)

* Rename the python module from `template` to the desired module name in `src/cltl`, `src/cltl_service` and
  the `setup.py`.
* Add the component as dependency to the parent makefile, the makefile of the app (e.g. the
  [Eliza app](https://github.com/leolani/cltl-eliza-app.git)) and other components that depend on it.
* Ensure the `util/` submodule is checked out in the new component and run `make build` **twice** from the application
  parent. If `util/` is not checked out, run

       git submodule update --init

  in the component's repository. Once the build is done, check if a virtual environment is created in the component and
  a package for the component is published to `cltl-requirements/leolani`. If this is not the case, try to run build the
  application from scratch by running `make clean` and `make build` from the parent repository. If it still fails,
  examine the output of *make* for log messages about the component or errors.
* Commit the changes to all modified components and the parent makefile. Commit the parent and run
       
       git push --recurse-submodules=on-demand
  
  from the parent.
* Customize the component and add it to the application as described below.

## Create a Python component

### API

Create an API with domain data classes and interfaces providing the functionality of the component,
see `src/cltl/api.py`.

Use *dataclasses* for the domain objects and avoid custom methods. This makes it possible to deserialize
to `SimpleNamespace` objects. Otherwise, eventually a custom deserializer to convert from JSON inputs to Python class
instances needs to be used.

Create one or more implementations of the API, see the structure in `src/cltl/`.

### Service

A typical component will be integrated in the application via the event bus of the application, i.e. it will subscribe
to certain topics on which it will receive events, process them and publish new events. Additionally, a component may
provide a REST interface that allows other components to directly call it in a client-server fashion. Data included in
the events should typically follow the EMISSOR data model.

This functionality is provided by a service that handles the invocation of the API with the correct data extracted from
the incoming events/requests and publishes/responds the returned data in the desired format.

The `src/cltl_service` module contains an example service. For other examples take a look at other existing components.

The service also represents the process that is run for the component in an application, either in a containerized
fashion or directly inside a Python application.

### Python package

Create a library package with at your API, implementation and service. In *setup.py* specify only dependencies of the
API as required, and add dependencies of implementation and service as extra requirements. Like this the API can be used
without adding unnecessary dependencies for the user of the API.

When using the package in another component, specify the additional dependency sets with

    cltl-template[impl,service]

in the `setup.py` or`requirements.txt` of that component if needed.

### Docker image

For containerization, create an main class that lets you invoke your service as Python script from the command line and
create a Docker image that runs it. This will provide the REST endpoints and run the event handlers.

## Using a component in applications

### Python application

To use the component service in a Python application, the service must be instantiated with the desired configurations,
started at the start of the application and stopped when the application shut's down. For an example, take a look at
`py-app/app.py` in the [Eliza app](https://github.com/leolani/cltl-eliza-app.git). In that application, services are
setup in Container classes to structure the setup and the dependencies between them. It is not necessary to follow this
pattern, they can also be instantiated, started and stopped directly in the main method.

### Containerized application

WIP

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any
contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->

## License

Distributed under the MIT License. See [`LICENSE`](https://github.com/leolani/cltl-combot/blob/main/LICENCE) for more
information.


<!-- CONTACT -->

## Authors

* [Taewoon Kim](https://tae898.github.io/)
* [Thomas Baier](https://www.linkedin.com/in/thomas-baier-05519030/)
* [Selene Báez Santamaría](https://selbaez.github.io/)
* [Piek Vossen](https://github.com/piekvossen)
