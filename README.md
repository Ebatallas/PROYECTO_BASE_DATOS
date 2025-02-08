# README - 📌 Descripción del Proyecto

Este proyecto desarrolla un pipeline automatizado para la ingesta, limpieza, procesamiento y visualización de datos de producción petrolera, utilizando herramientas como Apache Airflow, Knime, Elasticsearch y Kibana. La implementación mejora la eficiencia en el manejo de cuatro bases de datos que se actualizan diariamente, optimizando la toma de decisiones en tiempo real.

🟢 FASE 1: Preparación del Entorno y Configuración de Herramientas

🔹 Instalar y Configurar Herramientas:

✅ Knime → Para limpieza y transformación de datos históricos.

✅ Apache Airflow → Para la automatización de flujos batch y en tiempo real.

✅ Elasticsearch + Kibana → Para el almacenamiento y visualización de datos.

✅ Docker → Para contenerización y despliegue escalable.

⚠️ Verificación: Confirmar que cada herramienta funciona correctamente antes de continuar.

🟢 FASE 2: Procesamiento de Datos Históricos en Knime (Batch)

🔹 Carga y Limpieza de Datos en Knime:

📌 Datos de Entrada:

1️⃣ Coordenadas de Pozos

2️⃣ Histórico de Actividades

3️⃣ Histórico de Presiones

✅ Pasos en Knime:

Leer los archivos Excel y CSV en Knime.

Realizar limpieza de datos (valores nulos, formatos erróneos, normalización de datos).

Transformar datos si es necesario (unificación de columnas, cambios de tipo de datos).

Exportar los datos limpios a Elasticsearch.📌 Verificación:

Confirma que los datos están bien estructurados antes de enviarlos a Elasticsearch.

🟢 FASE 3: Creación del Flujo en Tiempo Real con Apache Airflow (Streaming)

🔹 Automatización con DAGs en Airflow:

✅ DAG-1: Generar Datos Sintéticos de Producción

Se ejecuta cada  minuto.

Genera datos sintéticos de producción basados en registros históricos.

Guarda los datos en un archivo CSV.

✅ DAG-2: Enviar Datos a Elasticsearch

Se ejecuta después de DAG-1.

Lee el CSV y envía los datos a Elasticsearch.

Kibana actualiza automáticamente la información.

📌 Verificación:

Ejecutar manualmente los DAGs en Airflow y verificar que los datos aparecen en Kibana.

🟢 FASE 4: Visualización en Kibana

🔹 Creación de Dashboards en Kibana:

✅ Gráfica de tendencias de presión y producción.

✅ Monitor de producción en tiempo real (auto-refresh cada  min).

📌 Verificación:

Asegurar que los gráficos en Kibana reflejan correctamente los datos enviados.

🟢 FASE 5: Pruebas Finales y Ajustes

🔹 Validación del Pipeline Completo:
✅ Ejecutar Knime → Verificar que los datos históricos aparecen en Kibana.

✅ Ejecutar DAGs en Airflow → Confirmar que los datos sintéticos llegan a Elasticsearch.

✅ Ajustar errores o mejoras si es necesario.

📌 Verificación:

Confirma que cada componente del pipeline funciona sin errores antes de la implementación final.

🟢 FASE 6: Presentación del Proyecto

🔹 Preparar Documentación y Exposición:

✅ Crear un diagrama de arquitectura con la descripción del sistema.

✅ Explicar cómo funciona cada componente del pipeline.

✅ Mostrar en Kibana los dashboards en vivo con datos en tiempo real.

✅ Subir código a GitHub con todos los scripts y configuraciones.

📌 RESUMEN DEL FLUJO

1️⃣ Instalar y configurar herramientas (Knime, Airflow, Kibana, Elasticsearch).

2️⃣ Cargar y limpiar datos históricos en Knime → Enviar a Kibana.

3️⃣ Crear DAGs en Airflow para generar y enviar datos sintéticos en tiempo real.

4️⃣ Diseñar dashboards en Kibana para visualizar datos históricos y en tiempo real.

5️⃣ Probar y ajustar el pipeline completo.

