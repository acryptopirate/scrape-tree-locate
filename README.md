# scrape-tree-locate

Build docker image:
`docker build --no-cache . -t treelocatebot`

Run web server
`docker run --name treel -p 80:80 -it -d --restart=always treelocatebot`

Check running containers
`docker ps`

Restart container
`docker restart treel`

Stop container
`docker stop treel`

Check logs
`docker logs -f treel`

