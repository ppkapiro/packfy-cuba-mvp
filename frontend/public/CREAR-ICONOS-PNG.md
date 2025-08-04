# PWA Icon Generator - Crear iconos PNG desde SVG

# Para crear iconos PNG optimizados, usa uno de estos métodos:

## Método 1: Online (Recomendado)
1. Ve a: https://realfavicongenerator.net/
2. Sube una imagen 512x512 del logo de Packfy
3. Genera todos los iconos PWA automáticamente

## Método 2: Figma/Canva
1. Crea un design 512x512px
2. Fondo azul #3b82f6
3. Emoji 📦 grande en el centro
4. Texto "Packfy" abajo
5. Exporta como PNG en 192x192 y 512x512

## Método 3: PowerShell (Temporal)
```powershell
# Convertir SVG a PNG usando imagemagick (si está instalado)
magick convert icon-512.svg icon-512.png
magick convert icon-192.svg -resize 192x192 icon-192.png
```

## Método 4: Usar el logo actual temporalmente
Por ahora usaremos una versión optimizada del SVG existente.
