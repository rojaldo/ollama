#!/bin/bash

# Script para iniciar el sistema de reconocimiento de prendas de ropa
# Uso: bash run_vision_app.sh

echo "=================================================="
echo "👕 Analizador de Prendas de Ropa"
echo "=================================================="
echo ""

# Colores para salida
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para verificar si un comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Función para verificar port
check_port() {
    nc -z localhost 11434 2>/dev/null
    return $?
}

# 1. Verificar Ollama instalado
echo -e "${BLUE}[1/4] Verificando Ollama...${NC}"
if ! command_exists ollama; then
    echo -e "${RED}❌ Ollama no está instalado${NC}"
    echo "Descárgalo desde: https://ollama.ai"
    exit 1
fi
echo -e "${GREEN}✅ Ollama encontrado${NC}"

# 2. Verificar si Ollama está corriendo
echo ""
echo -e "${BLUE}[2/4] Verificando si Ollama está ejecutándose...${NC}"
if ! check_port; then
    echo -e "${YELLOW}⚠️  Ollama no está ejecutándose en localhost:11434${NC}"
    echo ""
    echo -e "${YELLOW}Iniciando Ollama...${NC}"
    
    # Intenta iniciar Ollama en background
    if command_exists ollama; then
        ollama serve > /dev/null 2>&1 &
        OLLAMA_PID=$!
        echo -e "${YELLOW}Ollama iniciado (PID: $OLLAMA_PID)${NC}"
        echo "Esperando 3 segundos para que Ollama se estabilice..."
        sleep 3
    fi
fi

# Verificar nuevamente
if check_port; then
    echo -e "${GREEN}✅ Ollama está ejecutándose${NC}"
else
    echo -e "${RED}❌ No se pudo conectar a Ollama en localhost:11434${NC}"
    echo "Por favor, ejecuta manualmente en otra terminal:"
    echo -e "${YELLOW}ollama serve${NC}"
    exit 1
fi

# 3. Verificar modelo llava
echo ""
echo -e "${BLUE}[3/4] Verificando modelo 'llava'...${NC}"

# Obtener lista de modelos disponibles
MODELS=$(ollama list | grep -i llava)

if [ -z "$MODELS" ]; then
    echo -e "${YELLOW}⚠️  Modelo 'llava' no encontrado${NC}"
    echo "Descargando 'llava' (esto puede tomar algunos minutos)..."
    echo ""
    
    ollama pull llava
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Modelo 'llava' descargado correctamente${NC}"
    else
        echo -e "${RED}❌ Error al descargar 'llava'${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ Modelo 'llava' disponible${NC}"
    echo "Modelos de visión disponibles:"
    echo "$MODELS"
fi

# 4. Verificar Python y dependencias
echo ""
echo -e "${BLUE}[4/4] Verificando Python y dependencias...${NC}"

if ! command_exists python3; then
    echo -e "${RED}❌ Python3 no encontrado${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python versión: $PYTHON_VERSION"

# Verificar paquetes requeridos
echo "Verificando paquetes requeridos..."
python3 -c "import gradio; import ollama; import PIL" 2>/dev/null

if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️  Algunos paquetes no están instalados${NC}"
    echo "Instalando: gradio, ollama, pillow"
    pip install gradio ollama pillow -q
fi

echo -e "${GREEN}✅ Todas las dependencias están disponibles${NC}"

# 5. Iniciar la aplicación
echo ""
echo "=================================================="
echo -e "${GREEN}✅ Todo listo para iniciar${NC}"
echo "=================================================="
echo ""
echo -e "${YELLOW}Iniciando la aplicación...${NC}"
echo "La interfaz se abrirá en: ${BLUE}http://localhost:7860${NC}"
echo ""
echo "Presiona Ctrl+C para detener la aplicación"
echo ""

cd "$(dirname "$0")" || exit

# Ejecutar la aplicación
python3 vision_sample.py
