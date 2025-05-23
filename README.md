<h3 align="center">HRF - Universe Home Task submission </h3>

  <table>
    <thead>
        <tr>
            <th>Step</th>
            <th>Task Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Part 1: Create a table in the database to store "days to hire" statistics.</strong></td>
            <td></td>
        </tr>
        <tr>
            <td>1.1</td>
            <td>Statistics should be per country(also global for the world) and per standard job.</td>
        </tr>
        <tr>
            <td>1.2</td>
            <td>It should contain average, minimum, and maximum days to hire.</td>
        </tr>
        <tr>
            <td>1.3</td>
            <td>Also, it should contain a number of job postings used to calculate the average. We use this value to measure statistics quality. If the number of job postings is small, values can be inaccurate.</td>
        </tr>
        <tr>
            <td><strong>Part 2: Write a CLI script to calculate "days to hire" statistics and store it in a created table</strong></td>
            <td></td>
        </tr>
        <tr>
            <td>2.1</td>
            <td>Minimum days to hire is 10 percentile. <br>
Maximum days to hire is 90 percentile.<br>Average days to hire is an average of remaining values after cutting 10 and 90 percentiles.</td>
        </tr>
        <tr>
            <td>2.2</td>
            <td>Number of job postings is a number of rows used to calculate an average.</td>
        </tr>
        <tr>
            <td>2.3</td>
            <td>Do not save resulted row if a number of job postings is less than 5. Allow passing this threshold as a parameter.</td>
        </tr> <tr><td>2.4</td><td>For each country and standard job create a separate row in a table.</td></tr>        </tr> <tr><td>2.5</td><td>Also, create a row for world per standard job. Job postings with country_code equal to NULL should be included in this calculation.<br>Overwrite existing rows in the table. We need only the latest statistics.</td></tr>
        <tr>
            <td><strong>Part 3: Create REST API with one endpoint to get "days to hire" statistics.</strong></td>
            <td></td>
        </tr>
        <tr>
            <td>3.1</td>
            <td>
    Endpoint should accept standard_job_id and country_code as request parameters.<br>
    If country_code is not specified, return statistics for the world.
</td>
        </tr>
        
</table>
</div>



<!-- ABOUT THE PROJECT -->
## About The Project
The solution is fully containerized and offers cross-platform dependency management. All the CLI commands are sent into running container application.



`Poetry` - dependency and package manager used to manage dependencies and virtual env on the project.

`Makefile` (*NIX build tool `make`) - was used to shortcut project linters, syntax formatters, checking vulnerabilities and etc...

`FastAPI` - used for web API route implementation

`Pydantic` - was used for serialization and data validation

`Celery` - installed but not fully utilized for asynchronous message broker communication and data insertion. 

`RabbitMQ` - underline message broker for `Celery` support.

`Uvicorn` - application server to accept socket network requests and redirect to the implemented route.

`Environment variables` - `.env` file central configuration management.

`Volumes` - used for hot-reload and live sync of local vs container hosts.

`Alembic` - used for database DDL and migrations.

`SQLAlchemy` - ORM, but mostly SQLAlchemy Core is prioritized due to complexity and inner SQL Queries.


  
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


### Installation & Deployement

with Make build tool
  ```sh
  make build-images
  make up-container
  make apply-migrations 
  ```

without Make build tool
  ```
  docker-compose -f docker-compose.yml build 
  docker-compose -f docker-compose.yml up

alembic upgrade head
  ```




<!-- USAGE EXAMPLES -->
## Usage

`http://0.0.0.0:8000` - base URL for API </br></br>
`/hire_stats` - `GET` endpoint Accepting (Query `paramsstandard_job_id`*required, `country_code`-optional) </br></br>
```docker compose exec app python entrypoint.py -d -t 5``` - CLI command and flags to trigger statistics calculations. All calculations are batched </br></br>
`-d` or `--days_to_hire` - flag to trigger calculation/recalculation (upsert)</br></br>
`-t` or `--threshold` - optional flag to pass threshold of hire days integer value as an argument. Default value is = `5` </br></br>




<!-- CONTACT -->
## Contact

Arif Garayev - [Email](mailto:garayevarif@gmail.com)

Project Link: [Repository](https://github.com/arifgarayev/hrf-universe-home-task)

