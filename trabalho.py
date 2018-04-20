#trabalho individual da cadeira de Algoritmos Avançados de Bioinformática

from MyGraph import MyGraph
import operator
import matplotlib.pyplot as plt
import plotly.plotly as py

#função para ler o ficheiro da matriz
def read_file_mat(filename, sep = "\t"):
	mf = open(filename)
	res = [ ]
	line = mf.readline()
	while line:
		tokens = line.strip().split(sep)
		res.append((tokens[0],tokens[1],tokens[2]))
		line = mf.readline()
	return res

#função para ler o ficheiro dos metabolitos e reaçoes
def read_file_rm(filename, sep = ","):    
	rf = open(filename)    
	list_ids = []    
	ats_ids = {}
	rline = rf.readline()
	while rline:
		tokens = rline.strip().split(sep)
		list_ids.append(tokens[0])        
		ats_ids[tokens[0]] = tokens[1:]        
		rline = rf.readline()    
	return (list_ids, ats_ids)

#função para criar o grafo
def perg1(metab,reac,bounds,mat):
	print("\nPergunta 1\n")
	gmr = MyGraph({})
	for m in metab: gmr.add_node(m)
	for r in reac: gmr.add_node(r) 
	for e in mat:
		met_index = int(e[0])
		met_id = metab[met_index]
		reac_index = int(e[1])
		reac_id = reac[reac_index]
		reac_rev = float(bounds[reac_id][0])
		sign = float(e[2])
		if sign > 0 or reac_rev < 0: gmr.add_edge(reac_id,met_id)
		if sign < 0 or reac_rev < 0: gmr.add_edge(met_id, reac_id)
	print("\nGrafo concluído\n--------------------------")
	return gmr

#função para determinar o número de reações e metabolitos
def perg2(grafo):
	num_meta = str(len(metab))
	num_reac = str(len(reac))
	print("Pergunta 2\n")
	print("Numero metabolitos: "+str(len(metab)))
	print("Numero reacoes: "+str(len(reac)))
	print("--------------------------")
	return num_reac, num_meta

#Identifica os 10 metabolitos que participam num maior número de reações.
def perg3(grafo): 
	print("Pergunta 3\nTop10 metabolitos com maior número de reações\n")
	graus = {}
	#para cada metabolito obter o seu grau e criar dicionario em que a chave é o metaboltio e o valor é o grau 
	for m in metab: 
		grau = grafo.degree(m)
		graus[m] = grau
	#ordenar o dicionario de forma descendente a partir do seu grau e retirar os 10 primeiros
	ordenado = sorted(graus.items(), key=operator.itemgetter(1),reverse=True)[:10]
	for key,value in ordenado:
		print("metabolito: "+key+" -> reações: "+str(value))
	print("--------------------------")
	return ordenado

#Cria um gráfico com a distribuição do número de reações por cada um dos possíveis graus do tipo “inout”.
def perg4(grafo):
	print("Pergunta 4\n")
	rgraus = []
	#criar um array com os graus de cada reação 
	for r in reac:
		rgraus.append(grafo.degree(r))
	#criar um histograma com o array criado
	plt.hist(rgraus,bins=50)
	plt.xlabel("Graus do tipo inout")
	plt.ylabel("Quantidade de reações")
	plt.show()
	print("Gráfico feito\n--------------------------")


#5.	Identifica os metabolitos que são dead ends
def perg5(grafo):
	print("Pergunta 5\nMetabolitos dead ends\n")
	dead_ends = []
	for key,value in grafo.g.items():
		#se a chave do dicionário começar por "M_" e ter lista vazia como valor, é um dead_end pois significa que esse metabolito é produzido e nao há reações que o consumam
		if ("M_" in key and value==[]):
			dead_ends.append(key)
	print(len(dead_ends))
	print(dead_ends)
	print("--------------------------")
	return dead_ends


#funçao auxiliar para o ex6
def aux6(grafo,m,vis,produtos):
	for key,value in grafo.g.items():
		#verificar se é dead_end
		if (m == key and value==[]): 
			produtos.append(m)
		else: #se não for dead_end
			for v in value: 
				if(v in vis): #se já foi visitado pára, para evitar ciclos
					break
				else:
					vis.append(v) #adiciona ao array de visitados
					aux6(grafo,v,vis,produtos) #continua recursivamente
	return produtos

def perg6(grafo,uptake):
	print("Pergunta 6\nProdutos excretados pelos metabolitos: ")
	print(uptake)
	print("Uptake inserido no ficheiro trabalho.py")
	prod = [] 
	for m in uptake: #para cada metabolito presente no uptake
		produtos = [] 
		x = []
		print("\nPara o metabolito "+m+":\n")
		vis = []
		produtos = aux6(grafo,m,vis,x) 
		print(len(produtos))
		print(produtos)
		prod.append(produtos)
	print("--------------------------")
	return prod

#dado um metabolito devolve a lista de reações que produzem esse metabolito
def perg7(grafo,meta):
	pred = grafo.get_predecessors(meta) #obter os antecessores do nodo no grafo
	print(len(pred))
	print(pred)
	print("--------------------------")
	return pred

#verificação se existe reações com o mesmo metabolito como reagente e produto
def perg8(grafo):
	print("Pergunta 8\nReações que contêm metabolitos que servem como reagentes e produtos\n")
	res = []
	s = []
	for r in reac: #para cada reaçao
		pred = grafo.get_predecessors(r) #obter os antecessores
		suc = grafo.get_successors(r) #obter os sucessores
		for p in pred: #para cada um dos antecessores, verifica se tambem é sucessor
			if p in suc:
				res.append(r)
				break
	s = set(res)
	if len(s)>0:
		print(len(s))
		print(s)
		print("--------------------------")
		return s
	else:
		print("--------------------------")
		return None

#dado o metabolito origem e destino retorna todos os caminhos possíveis entre estes dois nós
def perg9(grafo, orig, dest):
    
	if orig == dest: return [] 
	l = [(orig, [])] 
	caminhos = [] #array de caminhos
	visited = [] #array visitados
	while l:
		node, path = l.pop(0) #pop da lista
		for elem in grafo.get_successors(node): #para cada um dos sucessore
			if elem == dest: #se for igual ao nodo destino
				caminhos.append([orig] + path + [elem])
			elif elem not in visited: #se o nodo ainda não foi visitado
				l.append((elem, path + [elem]))
				visited.append(elem)
	print(len(caminhos))
	print(caminhos)
	print("--------------------------")
	return caminhos

#lista de ciclos existentes na rede
def perg10(grafo):
	print("Pergunta 10\nCiclos presentes no grafo\n")
	ciclos = []
	nodes = grafo.get_nodes()
	for n in nodes: #para cada nodo no grafo verifica se contém um ciclo
		if grafo.node_has_cycle(n):
			ciclos.append(n)
	print(len(ciclos))	
	#print(ciclos)
	print("--------------------------")
	return ciclos


mat = read_file_mat("ijr904-matrix.txt")
metab,_ = read_file_rm("ijr904-metab.txt")
reac,bounds = read_file_rm("ijr904-reac.txt")


grafo = perg1(metab,reac,bounds,mat)


num_reac, num_meta = perg2(grafo)


top10 = perg3(grafo)


perg4(grafo)


dead_ends = perg5(grafo)


uptake = ["M_hco3_c","M_actp_c"]#['M_acac_e']
produtos = perg6(grafo,uptake)



print("Pergunta 7\n")
meta = input("Insira metabolito\n")
print("Reações que produzem o metabolito "+meta +"\n")
#meta = "M_atp_c"
reacprod = perg7(grafo,meta)


reagprod = perg8(grafo)


print("Pergunta 9\n")
orig = input("Insita metabolito origem\n")
dest = input("Insira metabolito destino\n")
#orig = "M_h_c"
#dest = "M_atp_c"
print("Sequência de nós entre a origem "+orig+" e o destino "+dest+"\n")
path = perg9(grafo,orig,dest)


ciclos = perg10(grafo)
