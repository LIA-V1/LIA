# Guía de Despliegue de LIA V3 (ADK Web)

Has completado el desarrollo de tu agente LIA V3. Para permitir que otros usuarios lo utilicen a través de una interfaz web, el camino más sencillo y recomendado por `google-adk` es **Google Cloud Run**.

## Requisitos Previos

1.  **Google Cloud SDK (gcloud)**: Es necesario para la configuración inicial.
    *   Descárgalo e instálalo desde: [cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install?hl=es-419)
    *   **IMPORTANTE**: Durante la instalación, marca la casilla "Add to PATH".
    *   Después de instalar, abre una **nueva terminal** y ejecuta: `gcloud init`
2.  **Proyecto en GCP**: Tener un ID de proyecto válido y facturación activa.

## Opción A: Despliegue Manual (Rápido)

Desde tu terminal, en la carpeta que contiene el directorio `lia/`, ejecuta:

```bash
adk deploy cloud_run --with_ui
```

## Opción B: Conectar con Git (Recomendado para Producción)

Si quieres que Cloud Run se actualice automáticamente cada vez que hagas un `push` a tu repositorio de Git:

1.  Ve a la consola de [Google Cloud Run](https://console.cloud.google.com/run).
2.  Haz clic en **"CREAR SERVICIO"**.
3.  Selecciona **"Implementar continuamente desde un repositorio"**.
4.  Haz clic en **"CONFIGURAR CLOUD BUILD"**.
5.  Selecciona tu proveedor (GitHub/Bitbucket) y elige tu repositorio.
6.  En la configuración de ejecución, selecciona **Dockerfile**. 

   > [!TIP]
   > He movido el `Dockerfile` y el `requirements.txt` a la raíz de tu repositorio `LIA/`. Ahora Google Cloud los encontrará automáticamente sin que tengas que configurar rutas manuales.

### ¿Qué hace este comando?
- Empaqueta tu agente LIA.
- Crea una imagen de contenedor.
- La sube a Artifact Registry de Google.
- Despliega el contenedor en Cloud Run.
- **`--with_ui`**: Activa la interfaz web del ADK para que puedas compartir la URL con otros usuarios.

## Configuración de Producción

Una vez desplegado, asegúrate de configurar las variables de entorno en la consola de Google Cloud Run:

- `GOOGLE_API_KEY`: Tu clave de Gemini (Flash).
- `GOOGLE_API_KEY_PRO`: Tu clave de Gemini (Pro).

## Verificación

Al terminar el despliegue, la terminal te entregará una URL (ej. `https://lia-v3-xxxx.a.run.app`). Cualquiera con esa URL podrá interactuar con tu agente.
