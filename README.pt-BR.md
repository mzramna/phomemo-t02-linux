[English](README.md) | [Português (BR)](README.pt-BR.md) | [Español](README.es.md)

# phomemo-t02-linux

## O que é

Um driver para a impressora térmica Phomemo T02 no Linux, via Bluetooth LE (BLE). Inclui uma CLI standalone (`t02`) e um backend CUPS para imprimir a partir de qualquer aplicativo.

## Requisitos

- Python 3
- `uv` (recomendado, roda o script com dependências inline) **ou** `bleak` + `pillow` instalados manualmente (`pip install -r requirements.txt`)
- BlueZ (stack Bluetooth do Linux)

## Instalação

Copie `t02` para `~/.local/bin` e torne-o executável:

```sh
cp t02 ~/.local/bin/t02
chmod +x ~/.local/bin/t02
```

## Primeiro uso

Rode o assistente de configuração, que escaneia a impressora via BLE e salva o endereço:

```sh
t02 --setup
```

O config é salvo em `~/.config/t02.conf`.

## Uso

```sh
t02 "algum texto"        # imprime texto
t02 imagem.png           # imprime uma imagem
t02 --font FONTE.ttf ...  # fonte customizada
t02 --size 32 ...        # tamanho da fonte
t02 --feed 8 ...         # avanço extra em mm após imprimir
t02 --info               # consulta status da impressora
```

## Integração CUPS/KDE

O script `cups/t02-backend` converte o job de impressão (PDF) em PNG a 203dpi e envia para a impressora.

1. Instale o backend como root:

   ```sh
   sudo install -o root -g root -m 0700 cups/t02-backend /usr/lib/cups/backend/t02
   ```

2. Registre a impressora:

   ```sh
   sudo lpadmin -p T02 -E -v t02:/ -m raw
   ```

3. Configure o papel para 48mm nas opções da impressora.

O CUPS roda o backend como root, então o Python **do sistema** precisa ter `python3-bleak` e `python3-pil` instalados (não basta um venv/ambiente uv de usuário). O backend lê o caminho do binário `t02` da variável de ambiente `T02_BIN` (padrão `/usr/local/bin/t02`) — instale uma cópia de `t02` nesse caminho, ou defina `T02_BIN`.

## Troubleshooting

- **Erro `ProfileUnavailable`**: remova o bond BLE antigo e escaneie de novo:

  ```sh
  bluetoothctl remove <MAC>
  bluetoothctl scan transport le
  ```

- A T02 aceita **apenas uma conexão BLE por vez** — desconecte qualquer outro cliente (app, outra instância do `t02`) antes de imprimir.
- Bluetooth clássico / RFCOMM **não funciona** com essa impressora; precisa ser BLE.

## Notas de protocolo

- Serviço GATT BLE `ff00`, característica de escrita `ff02`, características de notificação `ff01`/`ff03`.
- Imagens são enviadas como comandos raster ESC/POS `GS v 0`.
- Respostas de status no formato `1f 11 xx` são confirmadas enviando `1a xx`.

## Modo `--raw`

`--raw` envia comandos direto para a impressora via escrita BLE de baixo nível, contornando o loop do cliente asyncio/bleak. Isso é **experimental** e menos testado que o caminho padrão — espere arestas.

## Créditos

Baseado em engenharia reversa de protocolo de [vivier/phomemo-tools](https://github.com/vivier/phomemo-tools) e [transcriptionstream/phomymo](https://github.com/transcriptionstream/phomymo).
