


Este programa se ejecuta mediante la conexión cliente/servidor entre dos MMClient y un MMServer.

El resto de archivos son necesarios para la ejecución.

En esta práctica, las partidas las gestiona un solo hilo (linkinThread), el cual se ejecuta individualmente para cada cliente.

En el caso de que el cliente cree la partida, simplemente será registrado en la base de datos y se iniciará ña instancia mastermind.

En el caso de que el cliente se quiera unir a una partida existente, el hilo iniciará la clase Game. Esta conecta con el cliente host elegido y gestiona la partida.

Para esto, se sirve de la clase mastermind importada desde MMClass.py


Integrantes del equipo:

    Yuriy Moreno Salomón
    David Santa Cruz Del Moral
    Hao (Francesco) Zhou
    Diego Sota Rebollo
