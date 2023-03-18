# scrape-tree-locate

Build docker image:
`docker build --no-cache . -t treelocatebot`

Run scraping
`docker run --name treel -v archives:/code/archives -it -d treelocatebot`

Check running containers
`docker ps`

Restart container
`docker restart treel`

Stop container
`docker stop treel`

Check logs
`docker logs -f treel`

