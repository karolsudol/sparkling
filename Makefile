.PHONY: up stop clean run logs ps

# Start the cluster (Master + Worker)
up:
	docker-compose up -d --build

# Stop the containers without removing them
stop:
	docker-compose stop

# Clean everything: containers, volumes, and local images
clean:
	docker-compose down -v --rmi local --remove-orphans

# Run the Hello World application
run:
	docker-compose run --rm spark-app

# View logs
logs:
	docker-compose logs -f

# Check status
ps:
	docker-compose ps
