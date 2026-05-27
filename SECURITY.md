# Respuestas de Seguridad - Práctica 4 (CRUD & Authentication Hardening)
**Estudiante:** Anderson Plua
**Materia:** Ethical Hacking (Octavo Semestre)
**Universidad:** Uleam, Extensión El Carmen

---

## PARTE 1: Seguridad en Operaciones CRUD 

### 1. Riesgo OWASP para la vista de lista sin autenticación
El riesgo principal es la **Exposición de Datos Sensibles (Data Exposure)** y el **Control de Acceso Roto (Broken Access Control)**. Al no requerir autenticación, cualquier atacante que descubra la ruta `/incidents/` podría leer todos los reportes, comprometiendo información confidencial de la organización.

### 2. Token CSRF y su propósito
El token `{% csrf_token %}` previene ataques de **Falsificación de Solicitud entre Sitios (CSRF)**. Si se elimina, un atacante podría engañar a un usuario autenticado para que haga clic en un enlace malicioso, forzando a su navegador a enviar solicitudes (como borrar un incidente) sin su consentimiento.

### 3. Ataque IDOR y su explotación
IDOR significa **Referencia Directa Insegura a Objetos**. Ocurre cuando se accede a objetos directamente por su ID sin validar permisos. Un atacante podría explotarlo cambiando el número en la URL (ej. de `/incidents/1/` a `/incidents/5/`) para leer, editar o eliminar incidentes de otros usuarios.

### 4. Asignación Masiva y protección de ModelForm
La Asignación Masiva ocurre cuando un atacante inyecta campos adicionales en una petición POST (ej. enviando `resolved=True`) intentando alterar datos protegidos. Definir `Meta.fields = ['title', 'description', 'severity']` en el `ModelForm` previene esto, ya que Django ignorará cualquier campo que no esté explícitamente en esa lista.

### 5. El peligro de eliminar mediante peticiones GET
Es peligroso porque las solicitudes GET se pueden ejecutar simplemente visitando un enlace o cargando una imagen (ej. `<img src=".../delete/">`). Un atacante podría incrustar esto en un correo, y cuando la víctima lo abra, su navegador ejecutará el borrado automáticamente (ataque CSRF).

### 6. (Bono) Inyección SQL en el filtro
Si el filtro no usara el ORM, una URL maliciosa para inyectar código SQL sería:
`http://127.0.0.1:8000/incidents/?severity=High' OR '1'='1`

---

## PARTE 2: Autenticación y Hardening 

### Q0: El problema de un rastreador sin autenticación
Es un riesgo crítico porque expone vulnerabilidades internas; cualquier atacante podría ver qué sistemas fallan en la empresa y aprovechar esa información para lanzar ataques precisos.

### Q1: User vs UserProfile (OneToOneField)
El modelo `User` maneja la autenticación central (contraseñas), mientras que `UserProfile` almacena datos adicionales de negocio (como el rol). Usamos `OneToOneField` para extender el usuario sin alterar el código fuente de Django.

### Q2: Propósito de ?next= y redirección abierta
El parámetro `?next=` redirige al usuario a la página que buscaba antes de que se le pidiera iniciar sesión. Si no se valida, se corre el riesgo de un ataque de "Open Redirect", donde se usa un enlace engañoso (`/login/?next=http://sitio-malicioso.com`) para robar credenciales.

### Q3: Autenticación vs Autorización
**Autenticación** es verificar *quién eres* (ej. el formulario de login verifica tus credenciales). **Autorización** es verificar *qué puedes hacer* (ej. nuestra vista verifica si tienes el rol `is_admin()` antes de dejarte editar). Si omites la autorización, un analista autenticado podría borrar incidentes críticos.

### Q4: commit=False y Asignación Masiva
Usamos `commit=False` para pausar el guardado en la BD y asignar en el código backend `incident.reported_by = request.user`. Si esto se enviara por un campo oculto en el HTML, un atacante alteraría el campo (Mass Assignment) para hacerse pasar por otro usuario.

### Q5: Ocultar botones en la plantilla NO es suficiente
Ocultar botones HTML es solo "seguridad por oscuridad". Un atacante podría simplemente escribir la ruta en el navegador (`/incidents/1/delete/`). Este ataque se llama "Forced Browsing" o IDOR, y se previene validando los roles directamente en las vistas (`views.py`).

### Q6 (Bono): Ataque de Fuerza Bruta y django-axes
Un ataque de fuerza bruta intenta adivinar contraseñas probando combinaciones masivamente. `django-axes` lo mitiga bloqueando temporalmente la IP tras varios fallos (AXES_FAILURE_LIMIT). Poner el límite muy bajo corre el riesgo de bloquear a usuarios legítimos que se equivoquen al tipear.


