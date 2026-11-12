# Pitch (4 a 5 minutos)

Texto base. Cambien las palabras para que suenen suyas. Cada bloque indica que criterio cubre.

## 1. El problema y para quien (0:00 - 1:00) [P1]
"Mucha gente quiere ahorrar para algo concreto: un viaje, un computador, un fondo de emergencia. Pero casi nadie sabe **cuanto** debe apartar cada mes. El dinero ahorrado gana intereses, y si ademas se hace un pago extra a mitad de camino, la cuenta se complica: hacerla a mano es lento y es facil equivocarse.

Por ejemplo: si quiero juntar dos millones y medio en doce meses, y en el mes seis puedo adelantar cien mil pesos, ¿cuanto debo ahorrar mensualmente? Quienes lo necesitan son personas sin conocimientos financieros que quieren una respuesta rapida y confiable."

## 2. Que hace nuestra solucion (1:00 - 2:00) [P2]
"Nuestra aplicacion es un **Simulador de Ahorro Programado**. El usuario ingresa la meta, el plazo y, si quiere, un abono extra y el mes en que lo hara. La aplicacion calcula la cuota mensual con interes compuesto del 0,75 % mensual, la guarda y permite consultarla despues con su numero.

Para el ejemplo de antes, la respuesta es **191.516,95 pesos al mes**. Si los datos no tienen sentido, por ejemplo un abono sin mes, la aplicacion explica el error y no guarda nada.

Lo que **no** hace todavia: no tiene inicio de sesion (el usuario administrador ya existe, falta la pantalla) y la tasa de interes es fija."

## 3. Por que esta arquitectura y estas practicas DevOps (2:00 - 3:45) [P3]
"Separamos la aplicacion en tres partes: una pagina web, una API y una base de datos. Asi cada una se prueba y se actualiza sin tocar las otras.

- **Contenedores (Docker):** la aplicacion corre igual en cualquier computador. Las imagenes estan publicadas en DockerHub.
- **Pruebas automaticas:** 41 pruebas unitarias del backend y 5 pruebas Playwright que recorren la pagina real, de la pantalla hasta la base de datos.
- **Integracion continua (GitHub Actions):** cada cambio dispara las pruebas y la construccion de la imagen; si algo falla, no avanza.
- **Kubernetes (Minikube):** si un servicio se cae, Kubernetes lo reinicia solo; la base de datos usa un volumen, asi que los datos no se pierden; y las contrasenas viven en un Secret, no en el codigo.

Hay un precio: es mas complejo que una sola aplicacion, y no implementamos GitOps. Lo elegimos porque queriamos poder demostrar que el sistema se entrega de forma verificable, del commit al pod."

## 4. Cierre (3:45 - 4:30) [P4]
"En resumen: resolvemos un problema cotidiano con una herramienta simple, y lo entregamos con practicas que hacen el sistema reproducible y verificable. Ahora les mostramos todo funcionando en vivo."

## Consejos
- Repartan el pitch entre los tres (por ejemplo: Francisco problema, Valentina solucion, Jose arquitectura y cierre) o que hable uno solo con los otros dos atentos; la rubrica evalua la narrativa, el tiempo y que dominen las preguntas.
- Practiquen con cronometro: no pasarse de 5 minutos.
- No inventen estadisticas. Usen el escenario del ejemplo.
- Preparen respuestas para: "por que no usaron GitOps?", "que pasa si se cae la base de datos?", "donde estan las contrasenas?".
