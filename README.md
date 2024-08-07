## Sample BDD Tests for *Azure-Samples/node-todo* web application build in python using behave and selenium frameworks

Web application source code could be found here: https://github.com/Azure-Samples/node-todo

Key technologies used in the project:
* [Python 3.7+](https://en.wikipedia.org/wiki/Python_(programming_language))
* [Gherkin language](https://en.wikipedia.org/wiki/Cucumber_(software)#Gherkin_language)
* [Behave](https://behave.readthedocs.io/en/latest/)
* [Selenium](https://selenium-python.readthedocs.io)
* [Docker (docker-compose)](https://docs.docker.com/compose/)

Run with *Docker*:
* `docker build -t node-todo-bdd .`
* `docker run --rm --privileged --name node-todo-bdd node-todo-bdd`

Run with *python-behave*:
* Install *python3*, *pip3* and *virtualenv*
* `python3 -m venv venv-todo-bdd`
* `source venv-todo-bdd/bin/activate`
* `pip3 install -r requirements.txt`
* `SELENIUM_DRIVER=firefox behave`

Structure:
* [app/](https://github.com/nazarii-piontko/ToDo-BDD/tree/master/app) - contains docker and/or docker-compose files necessary to start an application under the test.
* [asserts/](https://github.com/nazarii-piontko/ToDo-BDD/tree/master/asserts) - contains classes used for asserting, e.g. general asserts or asserts on selenium element(s).
* [features/](https://github.com/nazarii-piontko/ToDo-BDD/tree/master/features) - contains feature files in Gherkin language.
* [infrastructure/](https://github.com/nazarii-piontko/ToDo-BDD/tree/master/infrastructure) - contains code to support test, e.g. start/stop application, start/stop selenium, provide configuration, etc.
* [pages/](https://github.com/nazarii-piontko/ToDo-BDD/tree/master/pages) - contains classes which encapsulate access to page dependent data, e.g. click on link, get input value, etc.
* [steps/](https://github.com/nazarii-piontko/ToDo-BDD/tree/master/steps) - contains steps implementation for feature files.
* [tools/](https://github.com/nazarii-piontko/ToDo-BDD/tree/master/tools) - contains different scripts and apps required to run test in different environments

---
Web application work example video:

![Application](application.gif)

Read more at my blog:

[BDD Part 1](https://www.npiontko.pro/2024/06/24/bdd-1.html)

[BDD Part 2](https://www.npiontko.pro/2024/06/30/bdd-2.html)
