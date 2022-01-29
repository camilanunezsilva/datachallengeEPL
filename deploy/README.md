# Deploy con docker

## Consideraciones

Lo que detallaré a continuación, es lo que teoricamente conozco que se debe hacer via AWS y de forma muy generica, porque nunca he realizado el proceso.

- Instalar Docker, para generar una imagen del código. Yo utilicé Docker Desktop para Windows 10. Se puede descargar en https://docs.docker.com/desktop/windows/install/

- Crear imagen docker, a partir del Dockerfile

- Crear un repositorio en AWS ECR, para almacenar imagen creada en paso anterior

- Llamar a la imagen anterior, desde el servicio AWS ECS.

