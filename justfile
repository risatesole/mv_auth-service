# Build the greet service
build:
    podman build -t greet-service .

# Run the container detached
run:
    podman run -d -p 8000:8000 --name greet-container greet-service

# Stop the running container
stop:
    podman stop greet-container || true
    # podman rm greet-container || true

# Remove the image (also stop container if running)
clean:
    podman stop greet-container || true
    podman rm greet-container || true
    podman rmi -f greet-service
