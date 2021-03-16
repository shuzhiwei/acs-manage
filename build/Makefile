export PROJECT_NAME=acs-manage
export VERSION=v1
export NODE_PORT=8085
export CONTAINER_PORT=8080

build:
	docker build -t $(PROJECT_NAME):$(VERSION) -f ./Dockerfile ../

run:
	docker run --name $(PROJECT_NAME) -d -p $(NODE_PORT):$(CONTAINER_PORT) \
	--restart=always --cpus 1 -m 1024m \
	-v /opt/data/docker-apps-logs/$(PROJECT_NAME)/:/tmp/ \
	-e host=$${host} \
	-e port=$${port} \
	-e user=$${user} \
	-e password=$${password} \
	-e database=$${database} \
	$(PROJECT_NAME):$(VERSION)

restart:
	docker rm -f $(PROJECT_NAME)
	docker run --name $(PROJECT_NAME) -d -p $(NODE_PORT):$(CONTAINER_PORT) \
	--restart=always --cpus 1 -m 1024m \
	-v /opt/data/docker-apps-logs/$(PROJECT_NAME)/:/tmp/ \
	-e host=$${host} \
	-e port=$${port} \
	-e user=$${user} \
	-e password=$${password} \
	-e database=$${database} \
	$(PROJECT_NAME):$(VERSION)

clean:
	docker images | grep none | awk '{print $$3}' | xargs docker rmi 
