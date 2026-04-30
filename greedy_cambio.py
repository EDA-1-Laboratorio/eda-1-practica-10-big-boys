import math

# ---------------------------------------------------------------------------
# Problema A – Solución greedy
# ---------------------------------------------------------------------------

def cambio_greedy(monto: int, monedas: list) -> tuple | None:
    """
    Resuelve el problema de cambio con la estrategia ávida:
    en cada paso usa la moneda de mayor valor que quepa.
    """
    # TODO: 1. Ordena las monedas de mayor a menor.
    monedas_ord = sorted(monedas, reverse=True)
    
    usadas = []
    restante = monto
    
    # TODO: 2. Para cada denominación, toma tantas monedas como quepan.
    for moneda in monedas_ord:
        cantidad = restante // moneda
        if cantidad > 0:
            usadas.extend([moneda] * cantidad)
            restante %= moneda
            
    # TODO: 3. Si el residuo final es 0, retorna (lista_de_monedas_usadas, total).
    if restante == 0:
        return (usadas, len(usadas))
        
    # TODO: 4. Si queda residuo, retorna None.
    return None


# ---------------------------------------------------------------------------
# Problema B – Solución óptima por programación dinámica
# ---------------------------------------------------------------------------

def cambio_optimo_dp(monto: int, monedas: list) -> tuple | None:
    """
    Resuelve el problema de cambio de manera óptima usando
    programación dinámica (número mínimo de monedas).
    """
    # TODO: crea la tabla dp y la tabla padre con longitud monto + 1.
    dp = [float('inf')] * (monto + 1)
    padre = [-1] * (monto + 1)
    
    dp[0] = 0 # Caso base: 0 monedas para monto 0
    
    # TODO: llena la tabla recorriendo cada monto parcial de 1 a monto.
    for i in range(1, monto + 1):
        for m in monedas:
            if m <= i:
                if dp[i - m] + 1 < dp[i]:
                    dp[i] = dp[i - m] + 1
                    padre[i] = m
                    
    # TODO: si dp[monto] es inf, retorna None.
    if dp[monto] == float('inf'):
        return None
        
    # TODO: reconstruye la lista de monedas usando padre[].
    usadas = []
    actual = monto
    while actual > 0:
        moneda = padre[actual]
        usadas.append(moneda)
        actual -= moneda
        
    return (usadas, len(usadas))


# ---------------------------------------------------------------------------
# Problema C – Comparación: contraejemplos
# ---------------------------------------------------------------------------

def comparar_estrategias(monto_max: int, monedas: list) -> dict:
    """
    Para cada monto de 1 a monto_max, compara greedy vs DP.
    """
    res = {
        'montos_greedy_falla': [],
        'montos_greedy_suboptimo': []
    }
    
    # TODO: itera los montos, llama a cambio_greedy y cambio_optimo_dp.
    for m in range(1, monto_max + 1):
        g = cambio_greedy(m, monedas)
        d = cambio_optimo_dp(m, monedas)
        
        # TODO: clasifica cada caso y acumula en las listas correspondientes.
        if d is not None:
            if g is None:
                res['montos_greedy_falla'].append(m)
            elif g[1] > d[1]:
                res['montos_greedy_suboptimo'].append((m, g[1], d[1]))
                
    return res


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Sistema canónico
    canonicas = [1, 2, 5, 10, 20, 50]
    print("=== Sistema canónico [1,2,5,10,20,50] ===")
    for monto in [11, 30, 63]:
        g = cambio_greedy(monto, canonicas)
        d = cambio_optimo_dp(monto, canonicas)
        print(f"  Monto {monto:>3}: greedy={g}  dp={d}")

    # Sistema no canónico – aquí greedy falla
    no_canonicas = [1, 3, 4]
    print("\n=== Sistema no canónico [1,3,4] ===")
    for monto in [6, 12, 15]:
        g = cambio_greedy(monto, no_canonicas)
        d = cambio_optimo_dp(monto, no_canonicas)
        print(f"  Monto {monto:>3}: greedy={g}  dp={d}")

    print("\n=== Análisis completo montos 1-60, sistema [1,3,4] ===")
    resultado = comparar_estrategias(60, no_canonicas)
    if resultado is not None:
        sub = resultado.get("montos_greedy_suboptimo", [])
        fal = resultado.get("montos_greedy_falla", [])
        print(f"  Casos subóptimos : {len(sub)}")
        print(f"  Casos con fallo  : {len(fal)}")
        if sub:
            print(f"  Primeros 5 subóptimos: {sub[:5]}")
    else:
        print("  comparar_estrategias aún no implementada")



''En cambio_greedy, se utilizó la lógica del "mejor paso inmediato". Primero ordenamos las monedas para 
usar siempre la más grande posible; luego, usamos la división entera // para saber cuántas de esas monedas 
caben en el monto y el operador residuo % para actualizar lo que falta por devolver. Si al final no sobra nada, la solución es válida.
En cambio_optimo_dp, se aplicó una tabla de resultados. El algoritmo llena una lista (dp) con el número 
mínimo de monedas para cada valor desde 1 hasta el monto final. La tabla padre es fundamental, ya que "anota" qué moneda
usamos para llegar a ese mínimo, lo que nos permite reconstruir la lista de monedas al final caminando hacia atrás desde el monto total.
En comparar_estrategias, se realizó un ciclo de prueba masiva. El código ejecuta ambos algoritmos para cada número y los compara. 
Si el algoritmo de Programación Dinámica (DP) encuentra una solución pero el Greedy no, se registra como fallo. Si ambos encuentran 
solución, pero el Greedy usa más monedas (es decir, el total de monedas de Greedy es mayor al de DP), se registra como subóptimo.''
