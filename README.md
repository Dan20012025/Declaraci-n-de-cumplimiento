# ⚡ Generador de Declaraciones RETIE

Aplicación web gratuita que genera automáticamente declaraciones de **cumplimiento RETIE** por apartamento, basada en una plantilla `.docx`.

🔧 Ideal para:
- Ingenieros eléctricos
- Revisores de cumplimiento RETIE
- Proyectos de vivienda, torres, edificios
- Constructores o diseñadores eléctricos

---

## 🚀 ¿Qué hace esta app?

Te permite subir una plantilla Word con los campos `{{consecutivo}}` y `{{apto}}`, para que el sistema genere copias personalizadas automáticamente para todos los apartamentos de una torre, siguiendo una numeración secuencial.

✅ Conserva el diseño original de la plantilla  
✅ No pierde formato, ni imágenes  
✅ Exporta todo en un solo documento Word listo para imprimir o firmar

---

## 🌐 Accede aquí

👉 [Haz clic para abrir la app](https://TU-USUARIO.streamlit.app)  
*Reemplaza por el enlace de Streamlit Cloud real*

---

## 🛠️ Cómo usar

1. Sube tu plantilla `.docx` que tenga los campos:  
   - `{{consecutivo}}` → para el número que irá aumentando
   - `{{apto}}` → para el número del apartamento

2. Ingresa el consecutivo inicial (ej. 1300)

3. Elige si todos los pisos tienen igual cantidad de apartamentos  
   o configura manualmente por piso

4. Descarga el documento final con todas las autodeclaraciones generadas

---

## 📄 Ejemplo de plantilla Word

```text
Declaración de Cumplimiento RETIE

Consecutivo: {{consecutivo}}  
Apartamento: {{apto}}

El presente documento certifica que...
