<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/arifgarayev/remofirst">
    <img src="img/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Real-Time Chat Application with Django, WebSocket, PostgreSQL, and Kafka</h3>

  <table>
    <thead>
        <tr>
            <th>Step</th>
            <th>Task Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Part 1: Django REST API</strong></td>
            <td></td>
        </tr>
        <tr>
            <td>1.1</td>
            <td>Set up a Django project with a REST API</td>
        </tr>
        <tr>
            <td>1.2</td>
            <td>Create a model for user accounts, including fields for username, email, and password. Implement user registration and authentication
using Django's built-in authentication system</td>
        </tr>
        <tr>
            <td>1.3</td>
            <td>3. Create a model for chat messages, including sender, receiver, timestamp, and message content.</td>
        </tr>
        <tr>
            <td>1.4</td>
            <td> Implement API endpoints for: <br> - Sending and receiving chat messages <br> - User registration and login. <br> - Retrieving chat history for a specific user </td>
        </tr>
        <tr>
            <td><strong>Part 2: WebSocket Integration</strong></td>
            <td></td>
        </tr>
        <tr>
            <td>2.1</td>
            <td>Integrate WebSocket functionality using Django Channels to enable real-time chat</td>
        </tr>
        <tr>
            <td>2.2</td>
            <td>Implement WebSocket consumers for handling chat messages in real time</td>
        </tr>
        <tr>
            <td>2.3</td>
            <td>Update the REST API to send and receive chat messages via WebSocket</td>
        </tr>
        <tr>
            <td><strong>Part 3: Database Integration</strong></td>
            <td></td>
        </tr>
        <tr>
            <td>3.1</td>
            <td>Configure Django to use PostgreSQL as the database backend</td>
        </tr>
        <tr>
            <td>3.2</td>
            <td>Create necessary database tables and migrations for user accounts and chat messages</td>
        </tr>
        <tr>
            <td>3.3</td>
            <td>pdate API endpoints to store and retrieve data from PostgreSQL</td>
        </tr>
        <tr>
            <td><strong>Part 4: Kafka Integration</strong></td>
            <td></td>
        </tr>
        <tr>
            <td>4.1</td>
            <td>Set up Kafka as a message broker</td>
        </tr>
        <tr>
            <td>4.2</td>
            <td>Integrate Django with Kafka to publish and consume chat messages asynchronously</td>
        </tr>
        <tr>
            <td>4.3</td>
            <td>Implement Kafka consumers to handle chat messages in real time</td>
        </tr>
        <tr>
            <td>4.4</td>
            <td>Update the WebSocket consumers to interact with Kafka for message handling</td>
        </tr>
        <tr>
            <td><strong>Part 5: Dockerization</strong></td>
            <td></td>
        </tr>
        <tr>
            <td>5.1</td>
            <td>Dockerize the entire Django application, including all dependencies (PostgreSQL, Kafka, etc.)</td>
        </tr>
        <tr>
            <td>5.2</td>
            <td>Create a Docker Compose file to manage the containers and their interactions</td>
        </tr>
        <tr>
            <td>5.3</td>
            <td> Ensure that the application can be run seamlessly within Docker containers</td>
        </tr>
    </tbody>
</table>
</div>



<!-- ABOUT THE PROJECT -->
## About The Project
This project is about Real-Time bi directional client communication - more precisely chatting like appication.

`Poetry` - dependency and package manager used to manage dependencies and virtual env on the project.

`Makefile` (*NIX build tool `make`) - was used to shortcut project linters, syntax formatters, checking vulnerabilities and etc...

`Swagger UI` - used for documentation & testing of the endpoints. You can use any other WebSocket client to connect WebSocket server host. Project doesn't contain any client side (no front end) markup to handle connections.

`Django Channels` - was used as an underlying base layer of the WebSocket protocol. 

Underneath `Django Channels` - is capable to apply a queue like brokers to handle messages asynchronously (like `Redis Queue`). 
However, I was not able find any native integration of `Django Channels` and `Apache Kafka` (per task requirement), therefore default `InMemoryChannelLayer` is used with refactored whole chatting architecure.

`Session cookies` (signed) - are used to authenticate user and issue a `session_id` on the client side (per requirement default `django-auth` must be used).

`Environment variables` - are located in the `.env` file of every project layer. Mostly this file overrides global container's environment vars. However some globals are considered not to take a part in `.env` file.

`CGI Application sever (GUnicorn)` - had an issue with binding both for `WebSocket` and `HTTP` host, therefore development server is used (default `manage runserver`).

`ApplyKafkaProducerMiddleware` - additional middleware layer was added in order to iject `singleton` kafka producer object into a `request` object, before every request on a predefined endpoints.

`volumes` - In order to persist data in the container, `volumes` was used for `database`, `logging`, `static server files`, `kafka socket`

`BCryptSHA256PasswordHasher` - used as a default hash algorithm.

Inspiration was to strictly stick to `DDD` and `Clean Architecture`. Hence some part of projects and folder-structure might be implicitly abstracted than usual `Django`'s `MVT`. 

`Apache Kafka Consumer service` - is a python project `path=./consumer` a dedicated service on a dedicated container environmet, listening for message broker on a certain topic, consuming broker's produced messages as a seperate service.


## Endpoints design

<br />
<br />
<div align="center">
  <a href="img/use-case.png">
    <img src="img/endpoints.png">
  </a>

<br />

## Use-case scenario system design visualization

<br />
<br />
<div align="center">
  <a href="img/use-case.png">
    <img src="img/use-case.png">
  </a>
  <br />
  
<br />

[![Use-case walkthough video](https://img.youtube.com/vi/P8Bw_ZuU6lc/hqdefault.jpg)](https://www.youtube.com/watch?v=P8Bw_ZuU6lc)

## Entity-relations diagram visualization

<br />
<br />
<div align="center">
  <a href="img/erd.png">
    <img src="img/erd.png">
  </a>

<br />


<!-- GETTING STARTED -->
## Getting Started

How to set up your project locally.
To get a local copy up and running follow these simple example steps.
First, clone the repository.
Docker Deamon is used to manage project deployments.

### Prerequisites

Docker Deamon must be installed and enabled.
Make build tool preferred, but not required

Docker Deamon - GNU/Linux
  ```
  apt install docker-ce
  sudo systemctl start docker
  sudo systemctl enable docker
  ````
Docker Deamon - MacOS ARM
  ```
  curl https://desktop.docker.com/mac/main/arm64/Docker.dmg --output ./Docker.dmg
  ````

Docker Deamon - MacOS Intel
  ```
  curl https://desktop.docker.com/mac/main/amd64/Docker.dmg --output ./Docker.dmg
  ````


### Installation & Deployement

with Make build tool
  ```sh
  make build-images
  make run-containers
  ```

without Make build tool
  ```
  docker-compose -f docker-compose.yml build 
  docker-compose -f docker-compose.yml up
  ```




<!-- USAGE EXAMPLES -->
## Usage

Navigate `http://0.0.0.0:8000` - in the browser, you will automatically redirected to the `Swagger UI` documentation page. Default port both for HTTP and WebSocket is `8000`



<!-- CONTACT -->
## Contact

Arif Garayev - [Email](mailto:garayevarif@gmail.com)

Project Link: [Repository](https://github.com/arifgarayev/remofirst)

