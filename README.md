# Adversarial Camouflage Aerial

Este repositorio contiene el código y la documentación del proyecto de investigación:

"Adversarial Camouflage para Evasión de Detectores de Objetos en Imágenes Aéreas: Diseño, Optimización y Evaluación bajo Condiciones Físicas Reales"


Enlaces (video y documento)
- Notebook principal de ataque (local): `experiments/Ataque_Adversarial.ipynb`
- Video explicativo (YouTube): https://youtu.be/rvVKcorkqAA
- Documento: 

Para actualizar los enlaces:
- Edita este archivo `README.md` y sustituye las URLs de los placeholders por las reales.
- Si prefieres, pégame las URLs y las añado yo (indica también el texto visible para cada enlace).


IMPORTANTE: código central en Notebooks
- Nota: el flujo de experimentos y las pruebas reproducibles están orquestadas desde los notebooks dentro de la carpeta `experiments/`. Los dos notebooks principales son:
  - `experiments/Ataque_Adversarial.ipynb` — prueba de concepto de optimización de textura (digital + export para impresión).
  - `experiments/Proyecto_VPC_Colab.ipynb` — notebook guía para ejecutar el proyecto en Google Colab (setup, baseline y runners).

Resumen breve
- Problema: los sistemas de detección aérea automatizada (p. ej. drones o vigilancia satelital) emplean modelos como YOLO entrenados en datasets como DOTA o xView para detectar vehículos, embarcaciones y otros objetos. Su robustez frente a texturas adversariales aplicadas como cobertura completa sobre objetos en vista cenital está menos estudiada que la de parches frontales.
- Propuesta / solución: diseñar e implementar un pipeline de optimización de texturas adversariales que, aplicadas como cobertura completa sobre vehículos en imágenes aéreas, reduzcan la detección de YOLOv8 OBB. El pipeline incluye Expectation Over Transformation (EoT) adaptado a vista cenital (altitud/zoom, rotación, inclinación), Non-Printability Score (NPS) calibrado para la impresora disponible, y un término opcional de naturalidad. Se evalúa digitalmente y físicamente (impresión y fotografía de maqueta a escala).

Cómo ejecutar los notebooks
- En Google Colab (recomendado para GPU):
  1. Abre `experiments/Proyecto_VPC_Colab.ipynb` en Colab (File > Upload notebook o abrir desde GitHub/Drive).
  2. Monta Google Drive como indica el notebook para acceder a `data/` y guardar `results/`.
  3. Ejecuta las celdas de setup (instalación de dependencias y verificación de runtime). Luego corre las secciones de baseline y ataque según las instrucciones del notebook.

- Local (sin Colab):
  1. Crea y activa un entorno virtual e instala dependencias:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

  2. Abre los notebooks con JupyterLab / Jupyter Notebook y ejecuta las celdas (si necesitas GPU local, asegúrate de tener CUDA y torch compatibles).
  3. Alternativamente, muchos pasos de los notebooks están disponibles como scripts CLI (`scripts/*.py`) si prefieres automatizar desde shell.

