# Makefile

# Docker-related variables
IMAGE_NAME :=cyborgslament/reading-wrapped
DOCKER_FILE1 := client/Dockerfile
DOCKER_FILE2 := server/Dockerfile
CONTAINER_NAME := reading-wrapped-container
DOCKER_COMPOSE_FILE := docker-compose.yml

# Build Docker image
build-1:
	docker build -t $(IMAGE_NAME) -f $(DOCKER_FILE1) .

# Build Docker image with Dockerfile2
build-2:
	docker build -t $(IMAGE_NAME) -f $(DOCKER_FILE2) .

# Run Docker container
run:
	docker run --name $(CONTAINER_NAME) -p 8080:80 -d $(IMAGE_NAME)

# Run Docker container with Docker Compose
compose-up:
	docker-compose -f $(DOCKER_COMPOSE_FILE) up -d

# Stop and remove Docker container
stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)

# Stop and remove Docker container with Docker Compose
compose-down:
	docker-compose -f $(DOCKER_COMPOSE_FILE) down

# Remove Docker image
clean:
	docker rmi $(IMAGE_NAME)

# Remove all stopped containers and unused networks
prune:
	docker system prune -a
