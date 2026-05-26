# Respuestas de Seguridad - Práctica 4 (Operaciones CRUD)
**Estudiante:** Anderson Plua
**Materia:** Ethical Hacking

### 1. Riesgo OWASP para la vista de lista sin autenticación
El riesgo principal que se aplica si esta vista expone todos los registros sin autenticación es la **Exposición de Datos Sensibles (Data Exposure)** y el **Control de Acceso Roto (Broken Access Control - OWASP A01:2021)**. Cualquier atacante en internet que descubra la ruta `/incidents/` podría leer todos los reportes, comprometiendo información confidencial sobre las vulnerabilidades y estados de los sistemas de la organización.

### 2. Token CSRF y su propósito
El token `{% csrf_token %}` previene ataques de **Falsificación de Solicitud entre Sitios (Cross-Site Request Forgery)**. Si se elimina este token, un atacante podría crear un sitio web malicioso y engañar a un usuario autenticado para que haga clic en un enlace. El navegador del usuario enviaría la solicitud POST a nuestra aplicación con sus credenciales, permitiendo al atacante crear, modificar o eliminar incidentes sin que el usuario legítimo se dé cuenta.

### 3. Ataque IDOR y su explotación
IDOR significa **Referencia Directa Insegura a Objetos (Insecure Direct Object Reference)**. Ocurre cuando una aplicación proporciona acceso directo a objetos basados en la entrada del usuario sin validar los permisos. 
Si esta aplicación tuviera múltiples usuarios y faltaran las verificaciones de propiedad, yo podría explotar esta vista simplemente cambiando la clave primaria (pk) en la URL. Por ejemplo, si estoy viendo mi incidente en `/incidents/2/`, cambiaría el número a `/incidents/3/`, `/incidents/4/`, etc., forzando al sistema a mostrarme o permitirme editar incidentes pertenecientes a otros usuarios.

### 4. Asignación Masiva y la protección de ModelForm
La Asignación Masiva (Mass Assignment) es una vulnerabilidad donde un atacante inyecta campos adicionales en los parámetros de una solicitud HTTP (por ejemplo, enviando `resolved=True` o manipulando `reported_at`) intentando modificar datos a los que no debería tener acceso.
Limitar los campos en `ModelForm` (usando `Meta.fields = ['title', 'description', 'severity']`) protege contra esto porque Django ignora estrictamente cualquier dato enviado en el `request.POST` que no esté explícitamente en esa lista, asegurando que campos críticos no puedan ser sobreescritos por el usuario.

### 5. El peligro de eliminar mediante peticiones GET
Permitir la eliminación de registros a través de una solicitud GET es extremadamente peligroso porque las peticiones GET están diseñadas para recuperar datos, no para alterarlos. Los navegadores web pre-cargan enlaces GET y las etiquetas HTML (como `<img src="...">`) pueden ejecutar peticiones GET silenciosamente.
El ataque que explota esto es el **CSRF**. Un atacante podría incrustar la URL `http://127.0.0.1:8000/incidents/1/delete/` dentro de una etiqueta de imagen en un foro o correo. Cuando la víctima (con su sesión iniciada) abra ese correo, el navegador hará la solicitud GET automáticamente y el registro será eliminado sin ninguna confirmación ni interacción consciente del usuario.

### 6. Inyección SQL en el filtro de severidad
Si el filtro de severidad se hubiera implementado con cadenas de texto SQL sin procesar (raw SQL) en lugar del ORM de Django, sería vulnerable a **Inyección SQL**. 
Una URL maliciosa para atacar ese filtro e intentar devolver todos los registros o alterar la consulta sería:
`http://127.0.0.1:8000/incidents/?severity=High' OR '1'='1`