# Static Files Directory

This directory contains static files for the myApp Django application.

## Structure

```
static/
└── myApp/
    ├── images/
    │   ├── logo.png
    │   ├── hero-bg.jpg
    │   └── icons/
    ├── css/
    │   └── styles.css
    └── js/
        └── main.js
```

## Usage in Templates

To use static files in your Django templates, add this at the top of your template:

```html
{% load static %}
```

Then reference images like this:

```html
<img src="{% static 'myApp/images/logo.png' %}" alt="Logo">
```

## Adding Images

Simply place your image files in the appropriate subdirectories:
- `images/` for general images
- `images/icons/` for icons and small graphics
