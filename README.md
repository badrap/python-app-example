# Python Example App

A small Python-based example of how to create a Badrap app that:

- Offers an UI to display the state of an installation.
- Updates the state of an installation based on UI input.
- Collects the assets of the owner of the installation (i.e. the user that has installed the app).

## Development

**Note**: The development environment works on MacOS and Linux. You may encounter problems with Windows.

Launch the development server that will restart on each code change. Docker Compose will also launch the API emulator that acts as a frontend to the Python service.

```sh
$ docker-compose up --build
```

If everything went well, open the API emulator frontend by directing your browser to http://localhost:4004.

### Running the Collector in Development

```sh
docker-compose run --rm app python -m app.collector
```

#### Feeding Test Data for the Collector

You can use the `/i/{name}/external_assets` endpoints to feed external assets
for an installation (`{name}` is the installation name visible in your
browser location bar, e.g. `0`).

"External assets" in this context mean assets that the app itself hasn't
created - e.g. assets that a Badrap user would have manually claimed. External assets aren't currently visible in the emulator, and they're only accessible & modifiable through APIs.

Add an external asset while the emulator is running for the installation name `0`:

```sh
curl -H "Content-Type: application/json" -d '{ "type": "ip", "value": "1.2.3.4" }' http://localhost:4040/i/0/external_assets
```

Possible values for key `"type"` are `"ip"`, `"domain"` and `"email"`. The value for key `"value"` has to be an IPv4/6 address, a domain name or an email address, respectively.

To list all external assets:

```sh
curl http://localhost:4040/i/0/external_assets
```

To delete a certain external asset with the id `{id}`:

```sh
curl -X DELETE http://localhost:4040/i/0/external_assets/{id}
```

## Production

### Building for Production

```sh
$ docker build -t app .
```

### Running the HTTP Service in Production

- `API_URL` should point to the Badrap API endpoint that the app talks with.
- `API_TOKEN` should be the Badrap API token that has been generated for the app.

```sh
$ docker run --rm -e API_URL=https://badrap.io/api -e API_TOKEN=123456789 -p 5000:5000 app
```

### Running the Collector in Production

```sh
$ docker run --rm -e API_URL=https://badrap.io/api -e API_TOKEN=123456789 app python -m app.collector
```
