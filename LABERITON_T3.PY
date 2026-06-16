import time
import copy
LABERINTO = [
    ['F',  1,  1,  1,  0,  1,  1,  1,  1],
    [-2,  0,  0, -1,  0,  1,  0,  1,  0],
    [ 1,  1,  0,  1,  1,  1,  0,  1,  0],
    [ 0,  1,  0, -1,  0,  0,  0, -1,  0],
    [ 1,  1,  1,  1,  1,  1,  1,  1,  0],
    [-1,  0,  0,  0,  0,  0,  0,  1,  1],
    [ 1,  1,  1,  1, -1,  1,  1,  1,  0],
    [ 1,  0,  0,  1,  0,  1,  0,  1,  0],
    ['I',  1, -1,  1,  1,  1,  0,  1,  1]
]

FILAS = 9
COLUMNAS = 9
POS_INICIO = (8, 0)
POS_FIN = (0, 0)

MOVIMIENTOS = [
    (1, 0, "abajo"),
    (0, 1, "derecha"),
    (-1, 0, "arriba"),
    (0, -1, "izquierda")
]

def imprimir_matriz(matriz, camino_actual=None):
    """Imprime el laberinto de forma legible resaltando el camino del raton."""
    for r in range(FILAS):
        fila_str = []
        for c in range(COLUMNAS):
            if camino_actual and (r, c) in camino_actual:
                fila_str.append(f"[\033[92mR\033[0m]")
            else:
                val = matriz[r][c]
                if val == 'I': fila_str.append("[I]")
                elif val == 'F': fila_str.append("[F]")
                elif val == 0: fila_str.append("[00]")
                else: fila_str.append(f"[{val:2}]")
        print(" ".join(fila_str))
    print("-" * 40)

def obtener_costo_vida(celda):
    """Devuelve el impacto en las vidas segun el tipo de celda."""
    if celda == 'I' or celda == 'F':
        return 0
    if celda == -1:
        return -1
    if celda == -2:
        return -2
    return 0 

def resolver_laberinto():
    vidas_iniciales = 3
    camino = [POS_INICIO]
    visitados = set([POS_INICIO])
    
    print("=== LABERINTO ORIGINAL ===")
    imprimir_matriz(LABERINTO)
    print("\nIniciando búsqueda con Backtracking...\n")
    
    solucion = []
    
    def backtrack(r, c, vidas_actuales):
        if solucion:
            return True

        if (r, c) == POS_FIN:
            solucion.extend(list(camino))
            return True
            
        for dr, dc, direccion in MOVIMIENTOS:
            nr, nc = r + dr, c + dc

            if 0 <= nr < FILAS and 0 <= nc < COLUMNAS:
                if LABERINTO[nr][nc] != 0 and (nr, nc) not in visitados:
                    descuento = obtener_costo_vida(LABERINTO[nr][nc])
                    nuevas_vidas = vidas_actuales + descuento

                    if nuevas_vidas >= 1:
                        camino.append((nr, nc))
                        visitados.add((nr, nc))

                        print(f"Ratón se mueve hacia el \033[94m{direccion}\033[0m a ({nr},{nc}) | Vidas: {nuevas_vidas}")
                        imprimir_matriz(LABERINTO, camino)
                        time.sleep(0.3)

                        if backtrack(nr, nc, nuevas_vidas):
                            return True

                        camino.pop()
                        visitados.remove((nr, nc))
                        
                        print(f"!!!  Camino sin salida o letal  !!! Retrocediendo desde ({nr},{nc})...")
                        
        return False
    
    exito = backtrack(POS_INICIO[0], POS_INICIO[1], vidas_iniciales)
    
    print("\n !!! RESULTADO FINAL !!! ")
    if exito:
        print("!!!! MENSAJE: El raton logro salir con exito del laberinto (FELICIDADES) !!!!")
        print(f"\nCamino tomado (fila, columna): \n{solucion}\n")
        print("\nMatriz con el camino final marcado:")
        imprimir_matriz(LABERINTO, solucion)
    else:
        print("!!!!  El raton no logro salir, No existen caminos viables con vidas suficientes  !!!!")

if __name__ == "__main__":
    resolver_laberinto()    
