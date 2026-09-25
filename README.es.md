[English](README.md) | [Português (BR)](README.pt-BR.md) | [Español](README.es.md)

# phomemo-t02-linux

## Qué es

Un driver para la impresora térmica Phomemo T02 en Linux, vía Bluetooth LE (BLE). Incluye una CLI independiente (`t02`) y un backend CUPS para imprimir desde cualquier aplicación.

## Requisitos

- Python 3
- `uv` (recomendado, ejecuta el script con dependencias inline) **o** `bleak` + `pillow` instalados manualmente (`pip install -r requirements.txt`)
- BlueZ (stack Bluetooth de Linux)

## Instalación

Copia `t02` a `~/.local/bin` y hazlo ejecutable:

```sh
cp t02 ~/.local/bin/t02
chmod +x ~/.local/bin/t02
```

## Primer uso

Ejecuta el asistente de configuración, que escanea la impresora vía BLE y guarda su dirección:

```sh
t02 --setup
```

La configuración se guarda en `~/.config/t02.conf`.

## Uso

```sh
t02 "algún texto"         # imprime texto
t02 imagen.png            # imprime una imagen
t02 --font FUENTE.ttf ...  # fuente personalizada
t02 --size 32 ...         # tamaño de fuente
t02 --feed 8 ...          # avance extra en mm tras imprimir
t02 --info                # consulta el estado de la impresora
```

## Markdown

`t02 archivo.md` imprime Markdown con negrita, cursiva, subrayado (`++texto++` o `<u>`), títulos, listas, citas, código, tablas (columnas de ancho igual a 48mm), reglas horizontales e imágenes locales. Usa `weasyprint` (necesita Pango del sistema, ya presente en escritorios GNOME/KDE) y `pypdfium2`, además del paquete `markdown` (pip) o `python3-markdown` (apt). Instala con `pip install -r requirements.txt`, o automáticamente vía uv. Límite: cerca de 4.9m de altura por impresión.

## Integración CUPS/KDE

El script `cups/t02-backend` convierte el trabajo de impresión (PDF) a PNG a 203dpi y lo envía a la impresora.

1. Instala el backend como root:

   ```sh
   sudo install -o root -g root -m 0700 cups/t02-backend /usr/lib/cups/backend/t02
   ```

2. Registra la impresora:

   ```sh
   sudo lpadmin -p T02 -E -v t02:/ -m raw
   ```

3. Configura el papel a 48mm en las opciones de la impresora.

CUPS ejecuta el backend como root, así que el Python **del sistema** necesita tener instalados `python3-bleak` y `python3-pil` (no basta un venv/entorno uv de usuario). El backend lee la ruta del binario `t02` desde la variable de entorno `T02_BIN` (por defecto `/usr/local/bin/t02`) — instala una copia de `t02` ahí, o define `T02_BIN`.

## Solución de problemas

- **Error `ProfileUnavailable`**: elimina el vínculo BLE antiguo y vuelve a escanear:

  ```sh
  bluetoothctl remove <MAC>
  bluetoothctl scan transport le
  ```

- La T02 acepta **solo una conexión BLE a la vez** — desconecta cualquier otro cliente (app, otra instancia de `t02`) antes de imprimir.
- El Bluetooth clásico / RFCOMM **no funciona** con esta impresora; debe ser BLE.

## Notas de protocolo

- Servicio GATT BLE `ff00`, característica de escritura `ff02`, características de notificación `ff01`/`ff03`.
- Las imágenes se envían como comandos raster ESC/POS `GS v 0`.
- Las respuestas de estado con formato `1f 11 xx` se confirman enviando `1a xx`.

## Modo `--raw`

`--raw` envía comandos directamente a la impresora mediante una escritura BLE de bajo nivel, sin pasar por el bucle del cliente asyncio/bleak. Esto es **experimental** y menos probado que la ruta por defecto — espera aristas sin pulir.

## Créditos

Basado en ingeniería inversa del protocolo de [vivier/phomemo-tools](https://github.com/vivier/phomemo-tools) y [transcriptionstream/phomymo](https://github.com/transcriptionstream/phomymo).
