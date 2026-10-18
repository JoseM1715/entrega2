# Historias de usuario

Roles: **Ahorrador** (persona que quiere cumplir una meta), **Administrador** y **Equipo de desarrollo**.

| ID | Historia | Criterios de aceptación | Responsable |
|----|----------|-------------------------|-------------|
| HU-01 | Como ahorrador quiero indicar mi meta y plazo para saber cuánto ahorrar cada mes. | Una meta de $1.200.000 a 12 meses sin abono da una cuota de $95.941,77 (tasa 0,75 % mensual). | Jose Angel Sanchez |
| HU-02 | Como ahorrador quiero incluir un abono extra en un mes para reducir mi cuota. | Meta $2.000.000 a 10 meses con abono de $1.000.000 en el mes 5: cuota $92.991,27. | Jose Angel Sanchez |
| HU-03 | Como ahorrador quiero mensajes claros cuando los datos son inválidos para corregirlos. | Se rechazan meta o plazo ≤ 0, abono negativo, abono mayor que la meta o sin mes válido; la web muestra el mensaje y no guarda nada. | Valentina Mesa |
| HU-04 | Como ahorrador quiero guardar mi meta con su cuota para consultarla después. | Al pulsar "Calcular y guardar" se muestra el ID de la meta y la cuota; queda guardada en PostgreSQL. | Valentina Mesa |
| HU-05 | Como ahorrador quiero buscar una meta por su ID. | Con un ID válido se muestran meta, plazo y cuota; con uno inexistente se muestra "No hay ninguna meta guardada con ese ID.". | Valentina Mesa |
| HU-06 | Como desarrollador quiero documentación Swagger de la API para conocer sus endpoints. | http://localhost:5000/docs muestra /api/usuarios, /api/metas y /api/metas/{id}. | Jose Angel Sanchez |
| HU-07 | Como equipo queremos levantar todo con un solo comando. | `docker compose up --build` inicia base de datos, seeding, backend y frontend. | Francisco |
| HU-08 | Como equipo queremos datos iniciales en la base de datos. | El seeding crea el usuario admin, la tabla maestra de parámetros y dos usuarios con una meta de ejemplo; se puede repetir sin duplicar. | Francisco |
| HU-09 | Como equipo queremos pruebas automáticas para detectar errores pronto. | Pasan las pruebas unitarias del backend y las de Playwright. | Francisco |
| HU-10 | Como administrador quiero iniciar sesión. | **Pendiente**: el usuario `admin` ya se crea con el seeding, falta el login. | Jose Angel Sanchez |
