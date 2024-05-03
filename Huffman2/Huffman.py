import heapq  # Importa el módulo heapq para trabajar con colas de prioridad
import os  # Importa el módulo os para operaciones del sistema operativo

# Definición de la clase NodoHuffman
class NodoHuffman:
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter  # El carácter almacenado en este nodo del árbol
        self.frecuencia = frecuencia  # La frecuencia del carácter en el texto
        self.izquierda = None  # Referencia al nodo hijo izquierdo
        self.derecha = None  # Referencia al nodo hijo derecho

    # Método de comparación para la clase NodoHuffman, necesario para la cola de prioridad
    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

# Función para contar la frecuencia de cada carácter en un texto
def contar_frecuencias(texto):
    frecuencias = {}  # Crea un diccionario para almacenar las frecuencias de los caracteres
    for caracter in texto:
        if caracter in frecuencias:
            frecuencias[caracter] += 1  # Incrementa la frecuencia si el caracter ya está en el diccionario
        else:
            frecuencias[caracter] = 1  # Agrega el caracter al diccionario con frecuencia 1 si es la primera vez que aparece
    return frecuencias

# Función para construir el árbol de Huffman a partir de las frecuencias
def construir_arbol(frecuencias):
    cola = [NodoHuffman(caracter, frecuencia) for caracter, frecuencia in frecuencias.items()]  # Crea una lista de nodos Huffman a partir del diccionario de frecuencias
    heapq.heapify(cola)  # Convierte la lista en una cola de prioridad
    while len(cola) > 1:  # Mientras haya más de un elemento en la cola
        izquierda = heapq.heappop(cola)  # Obtiene el nodo con menor frecuencia
        derecha = heapq.heappop(cola)  # Obtiene el nodo con la segunda menor frecuencia
        suma_frecuencias = izquierda.frecuencia + derecha.frecuencia  # Calcula la suma de las frecuencias
        nodo_padre = NodoHuffman(None, suma_frecuencias)  # Crea un nuevo nodo que será el padre de los dos nodos obtenidos
        nodo_padre.izquierda = izquierda  # Asigna el nodo de menor frecuencia como hijo izquierdo del nuevo nodo
        nodo_padre.derecha = derecha  # Asigna el nodo de segunda menor frecuencia como hijo derecho del nuevo nodo
        heapq.heappush(cola, nodo_padre)  # Agrega el nuevo nodo a la cola de prioridad
    return cola[0]  # Devuelve el único nodo que queda en la cola, que es la raíz del árbol de Huffman

# Función para construir la tabla de códigos Huffman
def construir_tabla_codigos(arbol_huffman, prefijo="", tabla_codigos={}):
    if arbol_huffman is not None:
        if arbol_huffman.caracter is not None:
            tabla_codigos[arbol_huffman.caracter] = prefijo  # Asigna el prefijo al carácter si es una hoja del árbol
        construir_tabla_codigos(arbol_huffman.izquierda, prefijo + "0", tabla_codigos)  # Recorre hacia la izquierda agregando '0' al prefijo
        construir_tabla_codigos(arbol_huffman.derecha, prefijo + "1", tabla_codigos)  # Recorre hacia la derecha agregando '1' al prefijo
    return tabla_codigos

# Función para comprimir un texto utilizando el algoritmo de Huffman
def comprimir(texto):
    frecuencias = contar_frecuencias(texto)  # Obtiene las frecuencias de los caracteres en el texto
    arbol_huffman = construir_arbol(frecuencias)  # Construye el árbol de Huffman
    tabla_codigos = construir_tabla_codigos(arbol_huffman)  # Construye la tabla de códigos Huffman
    texto_codificado = ''.join(tabla_codigos[caracter] for caracter in texto)  # Codifica el texto usando la tabla de códigos
    padding = 8 - len(texto_codificado) % 8  # Calcula el padding necesario para que la longitud del texto codificado sea un múltiplo de 8
    texto_codificado += padding * '0'  # Agrega el padding al texto codificado
    bytes_codificados = bytearray()  # Crea un bytearray para almacenar los bytes codificados
    for i in range(0, len(texto_codificado), 8):
        byte = texto_codificado[i:i+8]  # Divide el texto codificado en bloques de 8 bits
        bytes_codificados.append(int(byte, 2))  # Convierte cada bloque de 8 bits a un entero y lo agrega al bytearray
    return bytes_codificados, arbol_huffman, texto_codificado  # Devuelve los bytes codificados, el árbol de Huffman y el texto codificado

# Función para comprimir un archivo de texto
def comprimir_archivo(archivo_entrada, archivo_salida):
    with open(archivo_entrada, 'r') as f:
        texto = f.read()  # Lee el contenido del archivo de entrada
    bytes_codificados, arbol_huffman, texto_codificado = comprimir(texto)  # Comprime el texto
    print("Texto comprimido:")  # Imprime el mensaje indicando que se va a mostrar el texto comprimido
    print(texto_codificado)  # Muestra el texto comprimido
    with open(archivo_salida, 'wb') as f:
        f.write(bytes_codificados)  # Escribe los bytes codificados en el archivo de salida
    return arbol_huffman  # Devuelve el árbol de Huffman para su posterior uso en la descompresión

def descomprimir_archivo(archivo_entrada, archivo_salida, arbol_huffman):
    texto_decodificado = ''  # Inicializa una cadena para almacenar el texto decodificado
    nodo_actual = arbol_huffman  # Inicializa el nodo actual en la raíz del árbol de Huffman
    
    with open(archivo_entrada, 'rb') as f:
        while True:
            byte = f.read(1)  # Lee un byte del archivo
            if not byte:  # Si no hay más bytes para leer, termina el bucle
                break
            byte = ord(byte)  # Convierte el byte en un entero
            bits = '{:08b}'.format(byte)  # Convierte el byte en una cadena binaria de 8 bits
            
            for bit in bits:
                if bit == '0':
                    nodo_actual = nodo_actual.izquierda  # Recorre hacia la izquierda si el bit es '0'
                else:
                    nodo_actual = nodo_actual.derecha  # Recorre hacia la derecha si el bit es '1'
                if nodo_actual.caracter is not None:
                    texto_decodificado += nodo_actual.caracter  # Si se llega a una hoja, agrega el carácter al texto decodificado
                    nodo_actual = arbol_huffman  # Reinicia la búsqueda desde la raíz del árbol
    
    # Elimina los caracteres nulos al final del texto decodificado
    texto_decodificado = texto_decodificado.rstrip('\x00')
    
    print("Texto descomprimido:")  # Imprime el mensaje indicando que se va a mostrar el texto descomprimido
    print(texto_decodificado)  # Muestra el texto descomprimido
    
    with open(archivo_salida, 'w') as f:
        f.write(texto_decodificado)  # Escribe el texto decodificado en el archivo de salida


# Ejemplo de uso
archivo_entrada = 'ArchivoHuffman.txt'  # Nombre del archivo de entrada
archivo_comprimido = 'texto.bin'  # Nombre del archivo comprimido
archivo_descomprimido = 'texto_descomprimido.txt'  # Nombre del archivo descomprimido

# Comprimir el archivo de entrada y guardar el árbol de Huffman para su posterior uso en la descompresión
arbol_huffman = comprimir_archivo(archivo_entrada, archivo_comprimido)

# Descomprimir el archivo comprimido utilizando el árbol de Huffman previamente obtenido
descomprimir_archivo(archivo_comprimido, archivo_descomprimido, arbol_huffman)
