COMPOSE := docker compose -f docker/docker-compose.yml

.PHONY: image shell test build run clean
image:  ## build the dev image
	$(COMPOSE) build dev
shell:  ## interactive shell in the container (use `cb` / `ct` / `ros2 launch ...` inside)
	$(COMPOSE) run --rm dev
build:  ## colcon build in the container
	$(COMPOSE) run --rm dev bash -ic 'cb'
test:   ## colcon build + test in a clean runtime container
	$(COMPOSE) run --rm test
run:    ## launch both nodes
	$(COMPOSE) run --rm dev bash -ic 'cb && ros2 launch py_node_template workshop.launch.py'
clean:  ## remove colcon artefacts
	rm -rf build install log
