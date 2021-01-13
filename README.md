# Python Example App

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
