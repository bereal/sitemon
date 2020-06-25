# Sitemon

A distributed service that monitors a list of sites and saves
the status to the PostgreSQL database.

The site scanner (a.k.a. producer) communicates with the
status persistence logic (a.k.a. consumer) via Apache Kafka.


## Design overview

* The service is built as a single Python package, but producer and consumer
can be run separately by different command-line arguments.

* Site data is stored into a single table, which keeps the latest status
for each site: url, response code etc.

* The code is using Dependency Inversion as the main design principle.
Low-level HTTP, Kafka and PostgreSQL logic is isolated into separate classes.

* Avro is used as the data transfer protocol.

* Because Kafka producer and consumer parts are inherently coupled by the message format
and serialization logic, low-level Kafka consumer and producer wrappers belong
to the same Python module `sitemon.kafka`.

* Because the task in inherently io-bound, I am using `asyncio`-based APIs for
both PostgreSQL and Kafka.

* Missing parts: 1) proper logging, 2) graceful shutdown.


## Code overview

The most important files are:

    sitemon
    ├── kafka               - low-level Kafka wrappers
    │   ├── consumer.py
    │   ├── producer.py
    │   └── schema.py       - data object and Avro serialization
    ├── main.py             - main command-line entry
    ├── scanner
    │   ├── config.py
    │   └── scanner.py      - site scanner logic
    └── status
        ├── config.py
        ├── persistence.py  - PostgreSQL low-level logic
        └── worker.py       - consumer loop


## Installation and running

The service is packaged and installed using the python standard `setuptools`.

To install the service:

    $ make install

To run the producer:

    $ sitemon producer -c /path/to/producer/config.yaml

To run the consumer:

    $ sitemon consumer -c /path/to/consumer/config.yaml

To build a .whl package:

    $ make wheel

Examples of the configuration files are in `example_config`.
A Docker image is also available and can be used to run both producer and consumer.


## Testing

Producer part includes some amount of high-level logic, such as analyzing the site state.
That part is covered by unit tests with mocks.

To run the unit tests:

    $ make test

(That also makes sure that dependencies are installed.)

After all the low-level logic was moved to wrappers, it turned out that the consumer part
is nothing but calling those messaging and persistence layers in a loop. So I decided to
rely on integrated tests here. The docker-compose environment for tests includes:

 * Kafka (self-contained image from Spotify, old, but enough for the job)
 * PostgreSQL
 * httpbin
 * producer
 * consumer

To run the integrated test:

    $ make compose  # give it some time to start
    $ make test-integrated

The integrated test relies on the `example_config` files.
In a bigger scale the expected test results would likely also be configured.