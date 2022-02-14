# cltl-template

This repo is a template for the other services.
Each service has its own repo and a Dockerfile.
Their structure will inherit from this repo.

## Start from this template

To start from this template:
* Create a new empty repository on github with name <MODULE_NAME>.
* Clone this repository
  ```
  git clone https://github.com/leolani/cltl-template.git 
  ```
  or to add it as git submodule
  ```
  git submodule add --name <MODULE_NAME> https://github.com/leolani/cltl-template.git <MODULE_NAME>
  git submodule set-url <MODULE_NAME> <REMOTE_URL>
  ```
* Reomve the old remote:
  ```
  git remote remove origin
  ```
* Add the new emtpy repository and push the main branch:
     ```
  git remote add origin <REMOTE_URL>
  git push -u origin main
  ```    

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

Create a library package with at your API, implemntation and service. 
In setup.py specify only dependencies of the API as required, and add dependencies of implementation
and service as extra requirements. Like this the API can be used without adding unneded dependecies
for the user of the API.

### Docker image

Create a Docker image that runs your compoenent, including the required REST endpoints/Event handlers.

