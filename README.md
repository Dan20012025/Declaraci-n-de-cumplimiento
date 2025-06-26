# ⚡ Generador de Declaraciones RETIE

Aplicación web para generar automáticamente declaraciones de **cumplimiento RETIE** por apartamento, basada en una plantilla Word personalizada (`.docx`).

🔧 Ideal para:
- Ingenieros eléctricos
- Revisores de cumplimiento RETIE
- Constructores de proyectos de vivienda (torres, edificios, conjuntos)
- Cualquier profesional que deba emitir autodeclaraciones RETIE rápidamente

---

## 🚀 ¿Qué hace esta app?

Sube una plantilla `.docx` con los campos `{{consecutivo}}` y `{{apto}}`, y el sistema genera múltiples documentos listos para imprimir o firmar.

✅ Mantiene el diseño, formato e imágenes originales  
✅ Genera múltiples declaraciones en un solo archivo  
✅ Configura fácilmente apartamentos por piso o piso a piso

---

## 🌐 Accede aquí

👉 [https://dan20012025-declaraci-n-de-cumplimiento.streamlit.app](https://dan20012025-declaraci-n-de-cumplimiento.streamlit.app)

---

## 🛠️ Cómo usar

1. Sube tu plantilla Word con `{{consecutivo}}` y `{{apto}}`.
2. Elige el número inicial del consecutivo.
3. Define cuántos pisos y apartamentos tiene la torre.
4. Descarga el documento final en un solo archivo Word.

---

## 📄 Ejemplo de plantilla Word

```text
Declaración de Cumplimiento RETIE

Consecutivo: {{consecutivo}}  
Apartamento: {{apto}}

El presente documento certifica que...
