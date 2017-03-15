#!/usr/bin/python

import networkx as nx
import numpy

# Este es un script para recopilar algunas de las funciones del modulo networkx en python que 
# considero podrian ser útiles para realizar operaciones sobre agregados.

# Declara un objeto de tipo Graph
G = nx.Graph()

# Declara los nodos de la red. Para mi caso, a partir de la lista de IDs.
H = nx.path_graph(10)
G.add_nodes_from(H)

# Declara las interacciones entre los nodos. Para mi caso, a partir de una lista de interacciones pareadas entre vecinos.
G.add_edges_from([(1,2),(1,3), (4,5)])

# Obten el numero de componentes conectados. En el contexto del modelo, cada componente es un agregado diferente.
nx.number_connected_components(G)

# Crea una lista con los nodos y otras dos listas de atributos llamadas cell_type y conc. 
# Las tres listas deben ser del mismo tamaño.
# Los valores en ids deben corresponder a los nombres de mis nodos en la red G
ids  = [0,1,2,3,4,5,6,7,8,9]
cell_type = [1,1,1,1,1,2,2,1,2,1]
conc = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]

# Crea dos diccionarios. Uno entre ids y cell_type
# y otro entre ids y conc.
# En ambos casos ids es tomado entrada del diccionario.
x = dict(zip(ids,cell_type))
y = dict(zip(ids,conc))

# Asocia los diccionarios anteriores como atributos a los nodos de la red.
nx.set_node_attributes(G, "cell_type", x)
nx.set_node_attributes(G, "conc", y)

# Itera sobre los componentes de la red. Accede y manipula los atributos de los nodos de cada componente.
for c in nx.connected_component_subgraphs(G):
	print "Este es un agregado independiente:"
	size = len(nx.nodes(c))
	spores = nx.get_node_attributes(c, 'cell_type')
	num = spores.values()
	print "la fraccion de esporas en este componente es:"
	num.count(2)/float(size)
	a = numpy.array(nx.get_node_attributes(c, 'conc').values())
	print "la concentracion promedio de señal a en este componente es:"
	a.mean()
	print "y su desviacion estandar es:"
	a.std()
	print "\n"
	
