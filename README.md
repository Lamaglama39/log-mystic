# log-mystic

This is an access log analysis tool for various OSS.

## Description

Analyze the uploaded access log and display the analysis results.
Let's solve the mystery of access logs together!

## Getting Started

### Dependencies

- Almost all Linux distributions
- Docker
- Docker Compose

For reference,the author uses the following environment.
- WSL2 Ubuntu 22.04.4 LTS
- Docker version 25.0.3
- Docker Compose version v2.24.6-desktop.1

### Installing

* run docker-compose
```
$ git clone https://github.com/Lamaglama39/log-mystic.git
$ cd log-mystic
$ docker-compose up -d
```

### Developer operations

* Container Login
```
$ docker-compose exec app /bin/bash
```

## Project Structure
```
.
├── Dockerfile
├── LICENSE.md
├── README.md
├── app
│   ├── __init__.py
│   ├── main.py
├── docker-compose.yml
├── infrastructure
└── tests
```

## Author

[@Lamaglama39](https://twitter.com/lamaglama39)

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
