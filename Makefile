# Variables
DOCKER_COMPOSE = docker-compose

# Default target: build and start the services
.PHONY: all
all: build up

# Build the Docker images
.PHONY: build
build:
	$(DOCKER_COMPOSE) build

# Start the services in the background (detached mode)
.PHONY: up
up:
	$(DOCKER_COMPOSE) up -d

# Stop the services
.PHONY: down
down:
	$(DOCKER_COMPOSE) down

# View logs for all services
.PHONY: logs
logs:
	$(DOCKER_COMPOSE) logs -f

# Clean up Docker containers, images, and networks
.PHONY: clean
clean:
	$(DOCKER_COMPOSE) down --rmi all --volumes --remove-orphans

# Display the status of the services
.PHONY: status
status:
	$(DOCKER_COMPOSE) ps
