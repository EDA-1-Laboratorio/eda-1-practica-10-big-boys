import time
import random


# ---------------------------------------------------------------------------
# Problema A – Insertion sort con métricas
# ---------------------------------------------------------------------------

def insertion_sort_metricas(arr: list) -> tuple:
    """
    Ordena 'arr' usando insertion sort e instrumenta la ejecución.

    Retorna:
        (arreglo_ordenado, comparaciones, movimientos, tiempo_seg)
    """
    arr           = arr.copy()
    n             = len(arr)
    comparaciones = 0
    movimientos   = 0
    inicio        = time.perf_counter()

    for i in range(1, n):
        llave = arr[i]
        j = i - 1

        # TODO: mientras j >= 0 y arr[j] > llave:
        #            - incrementa comparaciones
        #            - desplaza arr[j] a arr[j+1], incrementa movimientos
        #            - decrement j
        while j >= 0:
            comparaciones += 1
            if arr[j] > llave:
                arr[j + 1] = arr[j]
                movimientos += 1
                j -= 1
            else:
                break

        # TODO: cuenta la comparación que termina el while (si j >= 0)
        # (Ya se contó en el break anterior o al fallar la condición del while)

        # TODO: coloca llave en arr[j + 1] e incrementa movimientos
        arr[j + 1] = llave
        movimientos += 1

    tiempo = time.perf_counter() - inicio
    return (arr, comparaciones, movimientos, tiempo)


# ---------------------------------------------------------------------------
# Problema B – Generación de escenarios
# ---------------------------------------------------------------------------

def generar_arreglo(n: int, escenario: str) -> list:
    """
    Genera un arreglo de tamaño n según el escenario indicado.
    """
    # TODO: implementa los tres escenarios; lanza ValueError si escenario es inválido.
    if escenario == 'mejor':
        return list(range(n))
    elif escenario == 'peor':
        return list(range(n, 0, -1))
    elif escenario == 'promedio':
        arr = list(range(n))
        random.shuffle(arr)
        return arr
    else:
        raise ValueError("Escenario inválido")


def medir_escenarios(tamanos: list) -> list:
    """
    Para cada tamaño en 'tamanos' evalúa los tres escenarios e imprime resultados.

    Retorna:
        Lista de dicts: {tamano, escenario, comparaciones, movimientos, tiempo}
    """
    resultados = []
    for n in tamanos:
        for escenario in ("mejor", "promedio", "peor"):
            arr = generar_arreglo(n, escenario)
            # TODO: llama a insertion_sort_metricas y guarda el resultado.
            _, comps, movs, t = insertion_sort_metricas(arr)
            resultados.append({
                "tamano": n,
                "escenario": escenario,
                "comparaciones": comps,
                "movimientos": movs,
                "tiempo": t
            })
    return resultados


# ---------------------------------------------------------------------------
# Problema D – Versión híbrida (insertion sort + merge sort)
# ---------------------------------------------------------------------------

def _merge(izq: list, der: list) -> list:
    """Combina dos listas ordenadas en una sola."""
    # TODO: implementa la fusión estándar de merge sort.
    res = []
    i = j = 0
    while i < len(izq) and j < len(der):
        if izq[i] <= der[j]:
            res.append(izq[i]); i += 1
        else:
            res.append(der[j]); j += 1
    res.extend(izq[i:])
    res.extend(der[j:])
    return res


def _merge_sort_hibrido(arr: list, umbral: int) -> list:
    """
    Divide 'arr' recursivamente.
    Si el subarreglo tiene tamaño <= umbral, usa insertion_sort_metricas.
    Si no, divide a la mitad y fusiona con _merge.
    """
    if len(arr) <= umbral:
        # TODO: retorna insertion_sort_metricas(arr)[0]
        return insertion_sort_metricas(arr)[0]
    
    mid = len(arr) // 2
    # TODO: llama recursivamente y fusiona con _merge
    izq = _merge_sort_hibrido(arr[:mid], umbral)
    der = _merge_sort_hibrido(arr[mid:], umbral)
    return _merge(izq, der)


def insertion_sort_hibrido(arr: list, umbral: int = 32) -> list:
    """
    Punto de entrada del ordenamiento híbrido.
    Retorna el arreglo ordenado.
    """
    # TODO: llama a _merge_sort_hibrido
    return _merge_sort_hibrido(arr, umbral)


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    tamanos = [1000, 2000, 4000]
    print("Midiendo escenarios... (puede tardar unos segundos)\n")
    resultados = medir_escenarios(tamanos)

    if resultados:
        print(f"{'Tamaño':>8} {'Escenario':>10} {'Comps':>12} "
              f"{'Movs':>12} {'Tiempo (s)':>12}")
        print("-" * 60)
        for r in resultados:
            print(f"{r['tamano']:>8} {r['escenario']:>10} "
                  f"{r['comparaciones']:>12} {r['movimientos']:>12} "
                  f"{r['tiempo']:>12.4f}")
    else:
        print("medir_escenarios aún no implementada.")




''En insertion_sort_metricas, se completó el bucle while para desplazar los elementos mayores a la "llave"
hacia la derecha. Se incluyó un contador de comparaciones que registra cada evaluación del ciclo y un contador 
de movimientos que suma cada vez que un dato cambia de posición o se inserta la llave final.
En generar_arreglo y medir_escenarios, se programaron las tres condiciones de prueba: 'mejor' (lista ordenada), 
'peor' (lista invertida) y 'promedio' (lista aleatoria). La función de medición recolecta estos datos y los 
organiza en un diccionario con el tamaño, las métricas de esfuerzo y el tiempo exacto de ejecución.
En la versión híbrida, se implementó la lógica de "divide y vencerás". El algoritmo divide el arreglo a la 
mitad recursivamente como en un Merge Sort, pero cuando llega a un tamaño pequeño (umbral), cambia automáticamente 
a Insertion Sort para aprovechar su mayor velocidad en subarreglos cortos.''
