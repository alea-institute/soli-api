# SOLI API

This project provides a public API for the [SOLI](https://openlegalstandard.org) (Standard for Open Legal Information) ontology.

**If you just want to access the API, you don't need to run this project yourself.  The API is freely available to the public,
including open CORS `*` origins, at [https://soli.openlegalstandard.org/](https://soli.openlegalstandard.org/).**

For example, you can view the `Lessor` class:

* [HTML](https://soli.openlegalstandard.org/R8pNPutX0TN6DlEqkyZuxSw/html)
* [JSON-LD](https://soli.openlegalstandard.org/R8pNPutX0TN6DlEqkyZuxSw/jsonld)
* [Markdown](https://soli.openlegalstandard.org/R8pNPutX0TN6DlEqkyZuxSw/markdown)
* [OWL XML](https://soli.openlegalstandard.org/R8pNPutX0TN6DlEqkyZuxSw/xml)
* [JSON](https://soli.openlegalstandard.org/R8pNPutX0TN6DlEqkyZuxSw)



## Overview

The SOLI API allows users to interact with the SOLI ontology, providing endpoints for searching, retrieving class information, and exploring the taxonomy.

## Swagger UI and OpenAPI Specification

The Swagger UI documentation can be found at [https://soli.openlegalstandard.org/docs](https://soli.openlegalstandard.org/docs).

The OpenAPI spec file can be found at [https://soli.openlegalstandard.org/openapi.json](https://soli.openlegalstandard.org/openapi.json).

## Running Locally with Docker and Caddy

To run the SOLI API locally using Docker and Caddy, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/your-repo/soli-api.git
   cd soli-api
   ```

2. Build the Docker image:
   ```
   docker build -t soli-api-ubuntu2404 -f docker/Dockerfile .
   ```

3. Check your configuration

View the `config.json` file to ensure that the configuration is correct for your environment.


3. Run the Docker container:

```
docker run -v $(pwd)/config.json:/app/config.json --publish 8000:8000 soli-api-ubuntu2404:latest
```

If you've changed the port in the `config.json` file, make sure to update the port in the `--publish` flag as well.

4. Reverse proxy with Caddy (optional)

- Ensure you have [Caddy](https://caddyserver.com/) installed on your system.
- Create a `Caddyfile` in the project root with the following content:
  ```
  <your.domain>> {
          encode gzip
          reverse_proxy localhost:8000
  }
  ```

5. Start Caddy:
   ```
   caddy run
   ```

Now you can access the API at `your.domain` (make sure to add this to your hosts file if testing locally).

## API Documentation

Once the API is running, you can access the Swagger UI documentation at `https://soli.openlegalstandard.org/docs`.

## Configuration

The API can be configured using the `config.json` file. Modify this file to change settings such as the SOLI source, API metadata, and binding options.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
