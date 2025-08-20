# 🔌 Packfy MCP Server
# Servidor MCP para desarrollo en tiempo real

import asyncio
import json
import os
import subprocess
import time
from typing import Any, Dict, List

from mcp import ImageContent, TextContent, Tool
from mcp.server import Server
from mcp.server.stdio import stdio_server

# Servidor MCP para Packfy
app = Server("packfy-mcp")


@app.call_tool()
async def restart_backend(arguments: Dict[str, Any]) -> List[TextContent]:
    """Reinicia el backend Django sin reconstruir Docker"""
    try:
        # Ejecutar comando de reinicio
        result = subprocess.run(
            ["docker-compose", "restart", "backend"],
            capture_output=True,
            text=True,
            cwd=os.getcwd(),
        )

        if result.returncode == 0:
            return [
                TextContent(
                    type="text", text="✅ Backend reiniciado exitosamente"
                )
            ]
        else:
            return [
                TextContent(type="text", text=f"❌ Error: {result.stderr}")
            ]
    except Exception as e:
        return [
            TextContent(type="text", text=f"❌ Error inesperado: {str(e)}")
        ]


@app.call_tool()
async def hot_reload_frontend(arguments: Dict[str, Any]) -> List[TextContent]:
    """Recarga automática del frontend sin reiniciar"""
    try:
        # Tocar archivo para forzar hot reload
        frontend_path = "./frontend/src/App.tsx"
        if os.path.exists(frontend_path):
            # Modificar timestamp para trigger reload
            os.utime(frontend_path, None)
            return [
                TextContent(
                    type="text", text="🔄 Frontend recargado automáticamente"
                )
            ]
        else:
            return [TextContent(type="text", text="❌ No se encontró App.tsx")]
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]


@app.call_tool()
async def run_migrations(arguments: Dict[str, Any]) -> List[TextContent]:
    """Ejecuta migraciones de Django sin parar servicios"""
    try:
        result = subprocess.run(
            [
                "docker-compose",
                "exec",
                "backend",
                "python",
                "manage.py",
                "migrate",
            ],
            capture_output=True,
            text=True,
        )

        return [
            TextContent(
                type="text",
                text=f"🔄 Migraciones: {result.stdout if result.returncode == 0 else result.stderr}",
            )
        ]
    except Exception as e:
        return [
            TextContent(type="text", text=f"❌ Error en migraciones: {str(e)}")
        ]


@app.call_tool()
async def check_services_health(
    arguments: Dict[str, Any],
) -> List[TextContent]:
    """Verifica estado de todos los servicios"""
    try:
        result = subprocess.run(
            ["docker-compose", "ps", "--services"],
            capture_output=True,
            text=True,
        )

        services_info = "📊 Estado de servicios:\n"
        services_info += result.stdout

        return [TextContent(type="text", text=services_info)]
    except Exception as e:
        return [
            TextContent(
                type="text", text=f"❌ Error verificando servicios: {str(e)}"
            )
        ]


@app.call_tool()
async def live_logs(arguments: Dict[str, Any]) -> List[TextContent]:
    """Muestra logs en tiempo real del servicio especificado"""
    service = arguments.get("service", "backend")

    try:
        # Obtener últimas 50 líneas de logs
        result = subprocess.run(
            ["docker-compose", "logs", "--tail=50", service],
            capture_output=True,
            text=True,
        )

        return [
            TextContent(
                type="text", text=f"📝 Logs de {service}:\n{result.stdout}"
            )
        ]
    except Exception as e:
        return [
            TextContent(
                type="text", text=f"❌ Error obteniendo logs: {str(e)}"
            )
        ]


# Definir herramientas disponibles
@app.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="restart_backend",
            description="Reinicia el backend Django sin reconstruir",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="hot_reload_frontend",
            description="Recarga automática del frontend",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="run_migrations",
            description="Ejecuta migraciones de Django",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="check_services_health",
            description="Verifica estado de servicios",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="live_logs",
            description="Muestra logs en tiempo real",
            inputSchema={
                "type": "object",
                "properties": {
                    "service": {
                        "type": "string",
                        "description": "Nombre del servicio (backend, frontend, database)",
                    }
                },
                "required": [],
            },
        ),
    ]


async def main():
    async with stdio_server() as streams:
        await app.run(streams[0], streams[1])


if __name__ == "__main__":
    asyncio.run(main())
