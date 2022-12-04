# audio-convertion-tool

## Procedimiento para ejecutar la aplicación

1. Descargue la imagen del máquina virtual de este [link](https://uniandes-my.sharepoint.com/:u:/g/personal/c_riverao_uniandes_edu_co/EZsttXcFpO9FigeOadsZMcIBtjmeZmSHvUlV0x1Q5LZL6g?e=3L1cvS).
2. Monte la máquina virtual en aplicación como VirtualBox.
3. Arranque la máquina virtual y espere que inicialice.
4. Ingrese los siguientes datos de acceso:
```
Usuario: chgarciaa1
Contraseña: chgarciaa1
```
5. Ubíquese en el siguiente directorio para activar el entorno virtual de la aplicación, ejecutando el siguiente comando
```
cd /var/www/Transform   
```
6. Active el entorno virtual de la aplicación ejecutando el siguiente comando
```
. venv/bin/activate
```
7. Ingrese en el directorio Transform/convertidor ejecutando el siguiente comando
```
cd convertidor
```
8. Ejecutar el worker mediante Celery. Una vez ejecutado el comando, la aplicación se quedará escuchando eventos en segundo plano
```
celery -A beat beat -l info &
```
9. Ejecute el siguiente comando para activar el worker de las colas que procesan los archivos
```
celery -A task.celery worker -l info &
```
10. Utilice la documentación en [Postman](https://documenter.getpostman.com/view/20323572/2s84LF4GMM), de la API de la aplicación para que realice las peticiones que requiera. 
Si desea puede autenticarse utilizando un usuario de ejemplo utilizado en la documentación

## Proyecto - Entrega 1

[Proyecto entrega Arquitectura conclusiones consideraciones.pdf](https://github.com/criverao/audio-convertion-tool/blob/master/Proyecto%201%20entrega%201%20-%20Arquitectura%2C%20conclusiones%20y%20consideraciones.pdf)

[Plan de pruebas.docx](https://github.com/criverao/audio-convertion-tool/blob/master/Plan%20de%20pruebas.pdf)

[Escenario y Pruebas de Estrés API REST y Batch.docx](https://github.com/criverao/audio-convertion-tool/blob/master/Escenario%20y%20Pruebas%20de%20Estre%CC%81s%20API%20REST%20y%20Batch.pdf)

## Proyecto - Entrega 2

[Escenario y Pruebas de Estrés API REST y Batch.docx](https://github.com/criverao/audio-convertion-tool/files/9907092/Escenario.y.Pruebas.de.Estres.API.REST.y.Batch.docx)

[Plan de pruebas.docx](https://github.com/criverao/audio-convertion-tool/files/9907091/Plan.de.pruebas.docx)

[Video Sustentación Semana 3](https://user-images.githubusercontent.com/36201331/199156759-f245be5d-4347-4216-b0ed-81b8872f5011.mp4)

## Proyecto - Entrega 3

[Escenario y Pruebas de Estrés API REST y Batch.pdf](https://github.com/criverao/audio-convertion-tool/files/10009579/Escenario.y.Pruebas.de.Estres.API.REST.y.Batch.pdf)

[Plan de pruebas.pdf](https://github.com/criverao/audio-convertion-tool/files/10009580/Plan.de.pruebas.pdf)

[Arquitectura conclusiones y consideraciones.pdf](https://github.com/criverao/audio-convertion-tool/files/10009578/Arquitectura.conclusiones.y.consideraciones.pdf)

[Video Sustentación Semana 5](https://user-images.githubusercontent.com/98676704/201826559-62bf4d35-4db5-4ce3-8cef-07189c49b380.mp4)


## Proyecto - Entrega 4

[Escenario y Pruebas de Estrés API REST y Batch.docx](https://github.com/criverao/audio-convertion-tool/files/10063663/Escenario.y.Pruebas.de.Estres.API.REST.y.Batch.docx)

[Plan de pruebas.docx](https://github.com/criverao/audio-convertion-tool/files/10063664/Plan.de.pruebas.docx)

[Arquitectura conclusiones y consideraciones.docx](https://github.com/criverao/audio-convertion-tool/files/10063666/Arquitectura.conclusiones.y.consideraciones.docx)

## Proyecto - Entrega 5

[Escenario y Pruebas de Estrés API REST y Batch.docx]()

[Plan de pruebas.docx]()

[Arquitectura conclusiones y consideraciones.docx]()

[Video Sustentación Semana 8](https://uniandes-my.sharepoint.com/:v:/g/personal/c_riverao_uniandes_edu_co/ET1kpMOUNHdIoO7yOaKYvGcBNP-ReSJYeciKN-xyJTdGSQ?e=IVR4mX)
