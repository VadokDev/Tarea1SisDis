# Hola
## Integrantes
- Gonzalo Fernández 2016735xx-x
- Sebastián Godínez 201673520-8

## Consideraciones:
- Para compilar y ejecutar se tiene que hacer dentro de la carpeta de la Actividad a evaluar.
### Actividad 1:
- El archivo *log.txt* se guarda en la carpeta "Servidor" y el archivo *respuestas.txt* se guarda en la carpeta "Cliente".
- Los archivos no se borran una vez terminada la conexión, por lo que ante una nueva ejecución se guarda abajo de lo ya existente.
- El cliente mandara mensajes de forma aleatoria hasta llegar a mandar la palabra *Terminar*, todo esto es de forma automatica.
### Actividad 2:
- El cliente funciona de la misma manera que en la Actividad 1.
- Para ejecutar multiples instancias de DataNode (o de Cliente) consideramos el flag `--scale`, quedando:\
`sudo docker-compose up --scale data=3`\
Para multiples clientes:\
`sudo docker-compose up --scale data=3 client=n`
- Tal como en la Actividad 1, los archivos generados por el Servidor se guardan en su respectiva carpeta (*hearbeat_server.txt* y *registro_server.txt*), similar con el Cliente (*registro_cliente.txt*) y para los DataNode se comparte el archivo *data.txt*, indicando con la IP quien escribio. Esto ultimo se debe a que el archivo se comparte entre los 3 containers.