# Gestion-de-cobranzas
# 🧾 Sistema de Gestión de Cobranzas para Pequeños Negocios – Backend

Este repositorio contiene el **backend de una API RESTful** diseñada para facilitar la gestión de cobranzas a crédito en pequeños negocios como tiendas, bodegas o servicios locales. El sistema permite registrar clientes, controlar deudas y establecer una base para automatizar recordatorios de pago.

---

## 📌 Problema

Muchos negocios locales gestionan las cobranzas de manera informal, lo que puede llevar a desorganización, pérdida de ingresos y un uso ineficiente del tiempo.

---

## ✅ Solución

Una API eficiente y fácil de implementar que permite:

- Registrar y gestionar deudas por cliente.
- Filtrar y consultar estados de deuda.
- Simular el envío de recordatorios (con posibilidad de integración futura con WhatsApp/SMS).

---

## 🚀 Características

### 📂 Gestión de Deudas

- Registrar nuevas deudas.
- Consultar todas las deudas (con opción de filtro por estado).
- Obtener detalles de una deuda específica.
- Editar o eliminar deudas existentes.

### 👤 Gestión de Clientes

- Registrar nuevos clientes.
- Ver todos los clientes registrados.
- Consultar información detallada de un cliente.
- Actualizar o eliminar registros.

### 🔔 Recordatorios (placeholder)

- Endpoint para simular el envío de recordatorios de pago.
- Preparado para futura integración con **Twilio** o la **API de WhatsApp**.

---

## 🛠️ Tecnologías Utilizadas

- **FastAPI**: Framework moderno y rápido para construir APIs con Python.
- **Pydantic**: Validación de datos mediante modelos.
- **Python**: Lenguaje principal del proyecto.
- **CORS Middleware**: Permite la conexión con un frontend externo.
- **Twilio / WhatsApp API**: Planificado para futuras integraciones de envío de recordatorios.

---

## ⚙️ Cómo Ejecutar el Proyecto

1. **Clona este repositorio** o guarda el código en `main.py`.

2. **Instala las dependencias**:

   ```bash
   pip install fastapi uvicorn "pydantic[email]"
