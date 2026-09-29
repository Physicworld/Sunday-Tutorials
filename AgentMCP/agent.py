# --------- INSTALL OLLAMA -------------------
# curl -fsSL https://ollama.ai/install.sh | sh
# ollama serve
# ollama pull gemma3:4b

import asyncio
import json
import os
import re
import sys
from pathlib import Path

import requests
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from dataclasses import dataclass
from typing import Dict, Any, Optional

# Configuración (ver .env.example); los valores por defecto son los del tutorial
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "gemma3:4b")
OLLAMA_TIMEOUT = float(os.environ.get("OLLAMA_TIMEOUT", "120"))  # segundos

# Ruta del servidor MCP relativa a este archivo: funciona desde cualquier cwd
MCP_SERVER_PATH = str(Path(__file__).resolve().parent / "mcp_server.py")


@dataclass
class ToolCall:
    name: str
    arguments: Dict[str, Any]


class OllamaClient:
    def __init__(self, base_url: str = OLLAMA_BASE_URL, model: str = OLLAMA_MODEL,
                 timeout: float = OLLAMA_TIMEOUT):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    def generate(self, prompt: str, system: str = None) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        if system:
            payload["system"] = system

        try:
            response = requests.post(f"{self.base_url}/api/generate", json=payload, timeout=self.timeout)
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            return f"Ollama Error: {str(e)}"


class Agent:
    def __init__(self):
        self.ollama = OllamaClient()
        self.available_tools = []
        self.conversation_history = []

    async def connect_to_mcp(self):
        self.mcp_client = Client(StdioTransport(command=sys.executable, args=[MCP_SERVER_PATH]))
        await self.mcp_client.__aenter__()
        tools = await self.mcp_client.list_tools()
        self.available_tools = [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.input_schema.get("properties", {}) if tool.input_schema else {}
            } for tool in tools
        ]

    def create_system_prompt(self) -> str:
        """Crea el prompt del sistema con información sobre herramientas MCP"""
        tools_info = "\n".join([
            f"- {tool['name']}: {tool['description']}: {tool['parameters']}"
            for tool in self.available_tools
        ])

        return f"""Eres un asistente IA que puede usar herramientas externas a través del protocolo MCP.

HERRAMIENTAS DISPONIBLES:
{tools_info}

INSTRUCCIONES:
1. Cuando necesites usar una herramienta, responde EXACTAMENTE en este formato:
   USAR_HERRAMIENTA: nombre_herramienta
   ARGUMENTOS: {{"argumento1": "valor1", "argumento2": "valor2"}}

2. Si no necesitas herramientas, responde normalmente.

3. Después de usar una herramienta, espera el resultado antes de continuar.

4. Mantén las respuestas concisas y útiles.
"""

    def parse_tool_call(self, response: str) -> Optional[ToolCall]:
        """Extrae llamadas a herramientas de la respuesta de Ollama"""
        # Buscar patrón de herramienta
        tool_pattern = r"USAR_HERRAMIENTA:\s*(\w+)"
        args_pattern = r"ARGUMENTOS:\s*(\{.*?\})"

        tool_match = re.search(tool_pattern, response, re.IGNORECASE)
        args_match = re.search(args_pattern, response, re.DOTALL | re.IGNORECASE)

        if tool_match:
            tool_name = tool_match.group(1)
            arguments = {}

            if args_match:
                try:
                    arguments = json.loads(args_match.group(1))
                except json.JSONDecodeError:
                    print(f"⚠️ Error parseando argumentos: {args_match.group(1)}")

            return ToolCall(name=tool_name, arguments=arguments)

        return None

    async def execute_tool(self, tool_call: ToolCall) -> str:
        """Ejecuta una herramienta MCP"""
        try:
            print(f"🔧 Ejecutando herramienta: {tool_call.name}")
            print(f"📋 Argumentos: {tool_call.arguments}")

            result = await self.mcp_client.call_tool(tool_call.name, tool_call.arguments)
            structured = result.structured_content
            if structured and 'result' in structured:
                output = structured['result']
            else:
                # Herramientas sin salida estructurada: usar el contenido de texto
                output = "\n".join(
                    getattr(block, "text", str(block)) for block in result.content
                )
            return output if isinstance(output, str) else str(output)

        except Exception as e:
            error_msg = f"Error ejecutando {tool_call.name}: {str(e)}"
            print(f"❌ {error_msg}")
            return error_msg

    async def chat(self, user_input: str) -> str:
        """Procesa entrada del usuario y responde"""
        # Agregar a historial
        self.conversation_history.append(f"Usuario: {user_input}")

        # Crear contexto completo
        context = "\n".join(self.conversation_history[-10:])  # Últimas 10 interacciones
        prompt = f"{context}\nUsuario: {user_input}\nAsistente:"

        # Generar respuesta con Ollama
        system_prompt = self.create_system_prompt()
        response = self.ollama.generate(prompt, system_prompt)

        # Verificar si necesita usar herramientas
        tool_call = self.parse_tool_call(response)

        if tool_call:
            # Verificar que la herramienta existe
            tool_names = [t['name'] for t in self.available_tools]
            if tool_call.name not in tool_names:
                final_response = f"❌ Herramienta '{tool_call.name}' no disponible. Herramientas disponibles: {', '.join(tool_names)}"
            else:
                # Ejecutar herramienta
                tool_result = await self.execute_tool(tool_call)

                # Generar respuesta final con el resultado
                follow_up_prompt = f"{prompt}\n{response}\n\nResultado de la herramienta: {tool_result}\n\nPor favor, proporciona una respuesta final basada en este resultado:"
                final_response = self.ollama.generate(follow_up_prompt, system_prompt)
        else:
            final_response = response

        # Agregar respuesta al historial
        self.conversation_history.append(f"Asistente: {final_response}")

        return final_response

    async def run_interactive(self):
        """Ejecuta el agente en modo interactivo"""
        print("🤖 Mini Agente Ollama + MCP iniciado")
        print("Escribe 'salir' para terminar\n")

        # Conectar a MCP
        await self.connect_to_mcp()

        try:
            while True:
                user_input = input("\n💬 Tú: ").strip()

                if user_input.lower() in ['salir', 'exit', 'quit']:
                    print("👋 ¡Hasta luego!")
                    break

                if not user_input:
                    continue

                print("🤔 Pensando...")
                response = await self.chat(user_input)
                print(f"🤖 Agente: {response}")

        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
        finally:
            if hasattr(self, 'mcp_client'):
                await self.mcp_client.__aexit__(None, None, None)


async def main():
    # Conectar a servidor MCP via STDIO
    agente = Agent()

    await agente.run_interactive()


if __name__ == "__main__":
    asyncio.run(main())
