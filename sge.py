"""
Sistema de Gestión de Estudiantes (SGE) básico
Autor: Nelson Andrés Luque González
Curso: Algoritmos y Programación - Ciencia de datos

Aplicación de consola que permite agregar, mostrar y buscar estudiantes por ID.
Demuestra: decisiones simples/anidadas, decisión múltiple (match-case),
ciclos while/for, variables de conteo, sumatoria y bandera, y uso de listas.
"""

# Límite de registros: aunque la lista de Python crece dinámicamente,
# se fija un máximo para practicar el control de capacidad (como en un arreglo).
MAX_ESTUDIANTES = 50


# ---------------------------------------------------------------------------
# Funciones de entrada validada (reutilizables)
# ---------------------------------------------------------------------------
def leer_entero(mensaje, minimo=None, maximo=None):
    """Pide un número entero hasta que el usuario ingrese uno válido.

    Se usa un ciclo while porque no sabemos cuántos intentos necesitará
    el usuario; try/except evita que el programa se caiga con texto.
    """
    while True:
        dato = input(mensaje).strip()
        try:
            numero = int(dato)
        except ValueError:
            print("  [!] Debe ingresar un número entero. Intente de nuevo.")
            continue
        # Decisión anidada: solo se revisa el rango si el número es válido
        if minimo is not None and numero < minimo:
            print(f"  [!] El valor debe ser mayor o igual a {minimo}.")
        elif maximo is not None and numero > maximo:
            print(f"  [!] El valor debe ser menor o igual a {maximo}.")
        else:
            return numero


def leer_texto(mensaje):
    """Pide un texto no vacío (repetición condicionada al final)."""
    # Python no tiene do-while; se simula con while True + break:
    # el cuerpo se ejecuta al menos una vez y la condición se evalúa al final.
    while True:
        texto = input(mensaje).strip()
        if texto != "":
            break
        print("  [!] Este campo no puede estar vacío.")
    return texto.title()


def leer_nota(mensaje):
    """Pide una nota decimal entre 0.0 y 5.0."""
    while True:
        dato = input(mensaje).strip().replace(",", ".")
        try:
            nota = float(dato)
            if 0.0 <= nota <= 5.0:
                return nota
            print("  [!] La nota debe estar entre 0.0 y 5.0.")
        except ValueError:
            print("  [!] Ingrese un número válido (ej. 4.2).")


# ---------------------------------------------------------------------------
# Operaciones del sistema
# ---------------------------------------------------------------------------
def buscar_indice(estudiantes, id_buscado):
    """Recorre la lista y devuelve la posición del estudiante o -1.

    Se usa una bandera 'encontrado' para detener el recorrido apenas
    aparece el ID y no hacer comparaciones innecesarias.
    """
    encontrado = False
    indice = 0
    while indice < len(estudiantes) and not encontrado:
        if estudiantes[indice]["id"] == id_buscado:
            encontrado = True
        else:
            indice += 1
    return indice if encontrado else -1


def agregar_estudiante(estudiantes, total):
    """Agrega un estudiante si hay cupo y el ID no está repetido.

    Devuelve el contador actualizado (total de estudiantes).
    """
    # Decisión simple: controlar que no se exceda la capacidad máxima
    if total >= MAX_ESTUDIANTES:
        print("  [!] Se alcanzó el máximo de estudiantes permitido.")
        return total

    id_nuevo = leer_entero("  ID del estudiante: ", minimo=1)
    # Decisión simple: evitar IDs duplicados
    if buscar_indice(estudiantes, id_nuevo) != -1:
        print(f"  [!] Ya existe un estudiante con ID {id_nuevo}.")
        return total

    estudiante = {
        "id": id_nuevo,
        "nombre": leer_texto("  Nombre completo: "),
        "edad": leer_entero("  Edad: ", minimo=15, maximo=99),
        "programa": leer_texto("  Programa académico: "),
        "nota": leer_nota("  Nota promedio (0.0 - 5.0): "),
    }
    estudiantes.append(estudiante)
    total += 1  # variable de conteo
    print(f"  [OK] Estudiante agregado. Total registrados: {total}")
    return total


def estado_academico(nota):
    """Clasifica la nota con decisiones anidadas (if-elif-else)."""
    if nota >= 3.0:
        if nota >= 4.5:
            return "Excelente"
        elif nota >= 4.0:
            return "Sobresaliente"
        else:
            return "Aprobado"
    else:
        return "Reprobado"


def mostrar_estudiante(estudiante):
    """Imprime una fila con los datos de un estudiante."""
    print(f"  {estudiante['id']:<6}{estudiante['nombre']:<25}"
          f"{estudiante['edad']:<6}{estudiante['programa']:<25}"
          f"{estudiante['nota']:<6.1f}{estado_academico(estudiante['nota'])}")


def mostrar_encabezado():
    print(f"  {'ID':<6}{'NOMBRE':<25}{'EDAD':<6}{'PROGRAMA':<25}{'NOTA':<6}ESTADO")
    print("  " + "-" * 80)


def mostrar_todos(estudiantes, total):
    """Muestra la lista completa y calcula el promedio general."""
    if total == 0:
        print("  No hay estudiantes registrados.")
        return

    mostrar_encabezado()
    suma_notas = 0.0  # variable de sumatoria (acumulador)
    # Ciclo for ascendente: recorre la lista del primero al último
    for estudiante in estudiantes:
        mostrar_estudiante(estudiante)
        suma_notas += estudiante["nota"]
    print("  " + "-" * 80)
    print(f"  Total de estudiantes: {total}   "
          f"Promedio general: {suma_notas / total:.2f}")


def mostrar_inverso(estudiantes, total):
    """Muestra los estudiantes del último al primero (iteración descendente)."""
    if total == 0:
        print("  No hay estudiantes registrados.")
        return
    mostrar_encabezado()
    for i in range(total - 1, -1, -1):
        mostrar_estudiante(estudiantes[i])


def buscar_estudiante(estudiantes):
    """Busca por ID e informa si se encontró o no."""
    id_buscado = leer_entero("  ID a buscar: ", minimo=1)
    posicion = buscar_indice(estudiantes, id_buscado)
    # Decisión simple: validar si el estudiante fue encontrado
    if posicion != -1:
        print("  [OK] Estudiante encontrado:")
        mostrar_encabezado()
        mostrar_estudiante(estudiantes[posicion])
    else:
        print(f"  [X] No existe un estudiante con ID {id_buscado}.")


def mostrar_menu(total):
    print("\n" + "=" * 45)
    print("   SISTEMA DE GESTIÓN DE ESTUDIANTES (SGE)")
    print("=" * 45)
    print(f"   Estudiantes registrados: {total}/{MAX_ESTUDIANTES}")
    print("   1. Agregar estudiante")
    print("   2. Mostrar lista de estudiantes")
    print("   3. Buscar estudiante por ID")
    print("   4. Mostrar lista en orden inverso")
    print("   5. Salir")
    print("=" * 45)


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------
def main():
    estudiantes = []        # lista que almacena los registros
    total_estudiantes = 0   # variable de conteo
    bandera_salir = False   # bandera que controla el ciclo principal

    # Repetición condicionada al comienzo: el menú se repite mientras
    # el usuario no haya elegido salir.
    while not bandera_salir:
        mostrar_menu(total_estudiantes)
        opcion = leer_entero("   Seleccione una opción: ")

        # Decisión múltiple: dirige el flujo según la opción elegida
        match opcion:
            case 1:
                total_estudiantes = agregar_estudiante(estudiantes, total_estudiantes)
            case 2:
                mostrar_todos(estudiantes, total_estudiantes)
            case 3:
                buscar_estudiante(estudiantes)
            case 4:
                mostrar_inverso(estudiantes, total_estudiantes)
            case 5:
                confirmar = input("   ¿Seguro que desea salir? (s/n): ").strip().lower()
                if confirmar == "s":
                    bandera_salir = True
            case _:
                print("  [!] Opción no válida. Elija un número del 1 al 5.")

    print("\n  Gracias por usar el SGE. ¡Hasta pronto!")


if __name__ == "__main__":
    main()
