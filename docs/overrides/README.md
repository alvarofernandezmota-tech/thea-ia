# 🎨 MkDocs Theme Overrides

**Propósito:** Customizaciones del tema Material for MkDocs para THEA IA.

**Última actualización:** 06 Enero 2026  
**MkDocs versión:** Material Theme

---

## 📁 Estructura

overrides/
├── .icons/ # Iconos customizados
├── assets/
│ ├── stylesheets/ # CSS personalizados
│ └── javascripts/ # JS personalizados
├── partials/ # Plantillas HTML modificadas
│ ├── header.html
│ ├── footer.html
│ └── nav.html
└── README.md # Este archivo

text

---

## 🎨 Customizaciones Aplicadas

### 1. CSS Customizados
- **Colores corporativos** - Esquema de colores THEA IA
- **Tipografía** - Fuentes optimizadas
- **Responsive design** - Ajustes móvil/desktop

### 2. JavaScript Extensions
- **Search enhancements** - Búsqueda mejorada
- **Analytics** - Tracking de uso
- **Interactive examples** - Código ejecutable

### 3. Plantillas HTML
- **Header** - Logo y navegación personalizada
- **Footer** - Links y copyright THEA IA
- **Navigation** - Sidebar customizado

---

## 🔧 Cómo Modificar

### Agregar CSS Nuevo
1. Crear archivo en `assets/stylesheets/custom.css`
2. Referenciar en `mkdocs.yml`:
   ```yaml
   extra_css:
     - overrides/assets/stylesheets/custom.css
Agregar JavaScript
Crear archivo en assets/javascripts/custom.js

Referenciar en mkdocs.yml:

text
extra_javascript:
  - overrides/assets/javascripts/custom.js
Modificar Plantillas
Copiar plantilla original de Material theme

Modificar en partials/

MkDocs automáticamente usa la versión override

📚 Referencias
Material for MkDocs - Customization

MkDocs - Custom Themes

Contacto: alvarofernandezmota@gmail.com