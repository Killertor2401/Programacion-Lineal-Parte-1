# Evaluacion #4 Metodos Cuantitativos Programacion Entera: Parte 1

#Abajo se presentaran las librerias a utilizar y se explicara brevemente de ser necesario las funciones de ellas.

# Esta es la librería Pulp, la cual se va a utilizar para los cálculos.
import pulp
import sys

# Esta vendria a ser la librería PyQt6, que se va a utilizar para la interfaz.
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QLabel,
        QMainWindow, QGridLayout)

# Esta es la libreria Numpy.
import numpy as np

# Estas son las librerías de matplot que se van a utilizar en el proyecto a realizar.
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from shapely.geometry import LineString

"""
Un crucero que hace el recorrido de navegacion de La Guaira-Miami, ofrece habitaciones para solteros al precio de $100 y le ofrece a las parejas habitaciones al precio de $60 por oferta. A las parejas se le deja llevar equipaje de hasta 40 Kgs de peso por ser dos personas, y a los solteros un equipaje de 10 Kgs de peso al ser una sola persona. Si la embarcacion tiene 100 habitaciones disponibles, y se le admite un equipaje de hasta 2 toneladas de peso(2000 Kgs), entonces: ¿Cuál tiene que ser la oferta de habitaciones de la compañía encargada del crucero para cada tipo de situacion de pasajeros, con su finalidad de poder optimizar el beneficio de la misma? Tambien se necesita tener en consideracion las siguientes restricciones: Se debe considerar que por políticas de la empresa encargada de la embarcacion del crucero, se necesita ofrecerse por lo mas mínimo 5 habitaciones para parejas.
"""

prob = """Un crucero que hace el recorrido de navegacion de La Guaira-Miami, ofrece habitaciones para solteros al precio de $100 y le ofrece a las parejas habitaciones al precio de $60 por oferta. A las parejas se le deja llevar equipaje de hasta 40 Kgs de peso por ser dos personas, y a los solteros un equipaje de 10 Kgs de peso al ser una sola persona. Si la embarcacion tiene 100 habitaciones disponibles, y se le admite un equipaje de hasta 2 toneladas de peso(2000 Kgs), entonces: ¿Cuál tiene que ser la oferta de habitaciones de la compañía encargada del crucero para cada tipo de situacion de pasajeros, con su finalidad de poder optimizar el beneficio de la misma? Tambien se necesita tener en consideracion las siguientes restricciones: Se debe considerar que por políticas de la empresa encargada de la embarcacion del crucero, se necesita ofrecerse por lo mas mínimo 5 habitaciones para parejas."""

# Paso #1: Se procede a definir las variables de decisión del problema.
x = pulp.LpVariable("x", lowBound=1) # Solteros
y = pulp.LpVariable("y", lowBound=1) # Parejas

# Paso #2: Se procede a establecer la función "objetivo".
funcion_objetivo = 100 * x + 60 * y

# Paso #3: Se procede a agregar las restricciones con las que se iran a trabajar en este problema.
restricciones = [
    10 * x + 40 * y <= 2000,
    x + y <= 100,
    y >= 5,
    y >= 0
    
]

# Paso #4: Se procede a resolver el problema de programación entera lineal utilizando la libreria PuLP.
problema = pulp.LpProblem("Problema de Programación Lineal", pulp.LpMaximize)
problema += funcion_objetivo
for restriccion in restricciones:
    problema += restriccion

problema.solve()

# Paso #5: Se procede con el proceso de asignación de los resultados a las variables, para que sean usados en la interfaz del programa.
punto_1 = x.varValue
punto_2 = y.varValue
resultado = pulp.value(problema.objective)


# Paso #6: Se procede a crea la ventana principal del programa.
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        
        # Paso 6.1: El proceso de la creación de las etiquetas a utilizar.
        titulo = QLabel("Problema de Programación Lineal")
        myFont=QtGui.QFont('Arial', 12)
        myFont.setBold(True)

        titulo.setFont(myFont)
        enun = QLabel(prob, alignment=Qt.AlignmentFlag.AlignJustify)
        enun.setWordWrap(True)

        funcion = QLabel("Función Objetivo: 100 * x + 60 * y", alignment=Qt.AlignmentFlag.AlignJustify)
        res1 = QLabel("Restricción 1: 10 * x + 40 * y <= 2000", alignment=Qt.AlignmentFlag.AlignJustify)

        res2 = QLabel("Restricción 2: x + y <= 100", alignment=Qt.AlignmentFlag.AlignJustify)
        res3 = QLabel("Restricción 3: y >= 5", alignment=Qt.AlignmentFlag.AlignJustify)
        res4 = QLabel("Restricción 4: y >= 0", alignment=Qt.AlignmentFlag.AlignJustify)
        titulo2 = QLabel("Asignación óptima de recursos", alignment=Qt.AlignmentFlag.AlignHCenter)


        x1 = QLabel(f"Solteros = {punto_1}", alignment=Qt.AlignmentFlag.AlignJustify)
        y1 = QLabel(f"Parejas = {punto_2}", alignment=Qt.AlignmentFlag.AlignJustify)
        final = QLabel(f"Beneficio máximo obtenido: {resultado}", alignment=Qt.AlignmentFlag.AlignJustify)

        Font=QtGui.QFont('Arial', 10)
        Font.setBold(True)
        final.setFont(Font)
        titulo2.setFont(Font)


        # Paso #6.2: Se procede a trabajar con la asignación de los espacios a los componentes del mismo programa.
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.setContentsMargins(20,20,20,30)
        grid.addWidget(titulo, 0, 0)
        grid.addWidget(enun, 1, 0)
        grid.addWidget(funcion, 2, 0)
        grid.addWidget(res1, 3, 0)
        grid.addWidget(res2, 4, 0)
        grid.addWidget(res3, 5, 0)
        grid.addWidget(res4, 6, 0)
        grid.addWidget(titulo2, 7, 0)
        grid.addWidget(x1, 8, 0)
        grid.addWidget(y1, 9, 0)
        grid.addWidget(final, 10, 0)

        # Paso #6.3: Se procede a trabajar con los datos finales del widget.
        widget = QWidget()
        widget.setLayout(grid)
        self.setCentralWidget(widget)
        self.setGeometry(500, 100, 400, 600)
        self.setWindowTitle('Problema de Programación Lineal')
        self.show()




# Paso #7: Se procede a ejecutar la ventana del programa.
app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()

# Paso #8: Gráfica de las ecuaciones y el área de resultados.

# Paso #8.1: Se procede a trabajar con las ecuaciones e intervalos del programa(Las cuales en este caso vendrian a representar restricciones despejadas).
x = np.arange(-100, 150, 50)
y = np.arange(-100, 150, 50)
y1 = (2000 - (10 * x))/ 40
y2 = 100 - x
y3 = 5 + (0 * x)
x1 = 0 * y
y4 = 0 * x
z = (-100 * x) / 600

# Paso #8.2: Se procede a asignar los identificadores para las líneas.
primera_linea = LineString(np.column_stack((x, y1)))
segunda_linea = LineString(np.column_stack((x, y2)))
tercera_linea = LineString(np.column_stack((x, y3)))
cuarta_linea = LineString(np.column_stack((x1, y)))
quinta_linea = LineString(np.column_stack((x, y4)))
sexta_linea = LineString(np.column_stack((x, z)))

# Paso #8.3: Se procede a graficar las líneas.
plt.plot(x, y1, '-', linewidth=2, color='b')
plt.plot(x, y2, '-', linewidth=2, color='g')
plt.plot(x, y3, '-', linewidth=2, color='r')
plt.plot(x1, y, '-', linewidth=2, color='y')
plt.plot(x, y4, '-', linewidth=2, color='k')
plt.plot(x, z, ':', linewidth=1, color='k')

# Paso #8.4: Se generan las intersecciones (vértices).
primera_interseccion = cuarta_linea.intersection(primera_linea)
segunda_interseccion = primera_linea.intersection(segunda_linea)
tercera_interseccion = segunda_linea.intersection(tercera_linea)
cuarta_interseccion = tercera_linea.intersection(cuarta_linea)

# Paso #8.5: Se procede a graficar los vértices.
plt.plot(*primera_interseccion.xy, 'o')
plt.plot(*segunda_interseccion.xy, 'o')
plt.plot(*tercera_interseccion.xy, 'o')
plt.plot(*cuarta_interseccion.xy, 'o')

# Paso #8.5: Se imprime las coordenadas de los vértices en la consola de Python.
print('\n COORDENADAS DE LAS INTERSECCIONES')
print('Coordenadas de la primera intersección: {} '.format(primera_interseccion))
print('Coordenadas de la segunda intersección: {} '.format(segunda_interseccion))
print('Coordenadas de la tercera intersección: {} '.format(tercera_interseccion))
print('Coordenadas de la cuarta intersección: {} '.format(cuarta_interseccion))

# Paso #8.6: Se procede a identificar los valores de las coordenadas X y Y de cada vértice.
xi1m, yi1m = primera_interseccion.xy
xi2m, yi2m = segunda_interseccion.xy
xi3m, yi3m = tercera_interseccion.xy
xi4m, yi4m = cuarta_interseccion.xy

# Paso #8.8: Se cambia el formato de matriz a float.
xi1 = np.float64(np.array(xi1m))
xi2 = np.float64(np.array(xi2m))
xi3 = np.float64(np.array(xi3m))
xi4 = np.float64(np.array(xi4m))
yi1 = np.float64(np.array(yi1m))
yi2 = np.float64(np.array(yi2m))
yi3 = np.float64(np.array(yi3m))
yi4 = np.float64(np.array(yi4m))

# Paso #8.9: Se evalua la función objetivo en cada vértice.
FOi1 = (xi1 * 100) + (yi1 * 60)
FOi2 = (xi2 * 100) + (yi2 * 60)
FOi3 = (xi3 * 100) + (yi3 * 60)
FOi4 = (xi4 * 100) + (yi4 * 60)

# Paso #8.10: Se imprime las evaluaciones de la FO en cada vértice (Consola).
print('\n EVALUACIÓN DE LA FO EN LOS VÉRTICES')
print('Función objetivo en la intersección 1: {} pesos'.format(FOi1))
print('Función objetivo en la intersección 2: {} pesos'.format(FOi2))
print('Función objetivo en la intersección 3: {} pesos'.format(FOi3))
print('Función objetivo en la intersección 4: {} pesos'.format(FOi4))

# Paso #9: Se calcula el mejor resultado (Maximizar).
ZMAX = max(FOi1, FOi2, FOi3, FOi4)

# Paso #10: Se imprime la solución óptima en la consola.
print('\n SOLUCIÓN ÓPTIMA')
print('Solución óptima: {} pesos'.format(ZMAX))

# Paso #11: Se ordenan las coordenadas de los vértices (Las coordenadas X en m y las coordenadas Y en n).
m = [xi1, xi2, xi3, xi4]
n = [yi1, yi2, yi3, yi4]

# Paso #12: Se grafica el polígono solución a partir de las coordenadas de los mismos vértices.
plt.fill(m, n, color='silver')

# Paso #13: Se procede a identificar el índice del vértice de la mejor solución.
dict1 = {0:FOi1, 1:FOi2, 2:FOi3, 3:FOi4}
posicion = max(dict1, key=dict1.get)

# Paso #14: Se obtenien las coordenadas del vértice de la mejor solución de acuerdo al índice.
XMAX = m[posicion]
YMAX = n[posicion]

# Paso #15: Se procede a imprimir las coordenadas del vértice de la mejor solución (variables de decisión).
print('\n VARIABLES DE DECISIÓN')
print('Cantidad de habitaciones a reservar para solteros: {} '.format(XMAX))
print('Cantidad de habitaciones a reservar para parejas: {} '.format(YMAX))

# Paso #16: Se procede a generar las anotaciones de las coordenadas Y, solución óptima en el gráfico.
plt.annotate('  X: {0} / Y: {1} (Coordenadas)'.format(XMAX, YMAX), (XMAX, YMAX))
plt.annotate('  Solución óptima: {}'.format(ZMAX), (XMAX, YMAX+3))


# Paso #17: Se procede a poner configuraciones adicionales del gráfico que se va a trabajar en este problema.
plt.grid()
plt.xlabel('Habitaciones para solteros')
plt.ylabel('Habitaciones para parejas')
plt.title('Método Gráfico')

# Paso #18: Por ultimo, se procede con la iniciación de la gráfica.
plt.show()