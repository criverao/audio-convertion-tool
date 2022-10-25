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
Si desea puede autenticarse utilizando un usuario de ejemplo utilizado en la documentaciónç

## Documento de plan de pruebas

[Link](https://github.com/criverao/audio-convertion-tool/blob/master/Plan%20de%20pruebas.pdf)

## Documento de Escenarios y pruebas de Estrés API RESTy Batch

[Link](https://github.com/criverao/audio-convertion-tool/blob/master/Escenario%20y%20Pruebas%20de%20Estre%CC%81s%20API%20REST%20y%20Batch.pdf)
