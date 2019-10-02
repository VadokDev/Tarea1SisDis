# Hola
## Integrantes
- Gonzalo Fernández 2016735xx-x
- Sebastián Godínez 201673520-8

## Consideraciones:
- Al ejecutar `docker-compose up` se muestra por pantalla el Log de los distintos componentes.
- Para ejecutar multiples instancias de DataNode consideramos el flag `--scale`, quedando:\
`sudo docker-compose up --scale data=3`
- Para ver los archivos pedidos, accedemos al container con:\
`sudo docker exec -it <container name> /bin/bash`