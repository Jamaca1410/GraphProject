#wired graph algorithm
from JsonData import *
# TENER EN CUENTA EL KEY VALUE DEL GRAFO DEBE SER UN INT
# USAR SET
#PARA HACER LOOKUP USAR LIST
# EVITAR REPETICIONES
# EVITAR FORLOOP
#Clase usuario
class user:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class graph:
    #Inicializamos el grafo con un adjecency list 
    def __init__(self):
        self.graph = {}
        self.nodesadded = []

    def loadJson(self):
        self.addNodeJson()
        self.addEdgeJson()    

    def addNode(self, name, id):
        temp = user(id, name)   
        if temp.id not in self.nodesadded:
            self.graph[temp] = []
            self.nodesadded.append(temp.id)
    
    def addEdge(self, id1, id2):
        for key in self.graph:
                if key.id == id1:
                    class1 = key
                    exist1 = True
                if key.id == id2:
                    class2 = key
                    exist2 = True
        if exist1 == False or exist2 == False:
            print("One or both of the nodes does not exist in this graph.")  
        else:
            if id1 == id2:
                print("Connection to the same node are not allowed.")
                #Cuando los nodos no son iguales
            else:
                if class2 not in self.graph[class1] and class1 not in self.graph[class2]:
                    self.graph[class1].append(class2)
                    self.graph[class2].append(class1)
                else:
                    print("This connection already exist.")

    #Agregamos el nodo
    def addNodeJson(self):
        data = Json()
        nodeadd = []  
        for key in range(len(data["users"])): 
            temp = user(data["users"][key]["id"], data["users"][key]["name"])      
            nodeadd.append(temp)      
            if temp.id not in self.nodesadded:
                self.graph[nodeadd[key]] = []
                self.nodesadded.append(temp.id)  
            else:
                print("This node is already in the graph.")     
     

    def addEdgeJson(self):
        data = Json()
        for i in data["relations"]:
            #find the node
            exist1 = False
            exist2 = False
            for key in self.graph:
                if key.id == i[0]:
                    class1 = key
                    exist1 = True
                if key.id == i[1]:
                    class2 = key
                    exist2 = True                    

            if exist1 and exist2:
                #Cuando de quiere hacer una conexion a un mismo nodo
                if class1 == class2:
                    print("Connection to the same node are not allowed.")
                #Cuando los nodos no son iguales
                else:
                    if class2 not in self.graph[class1] and class1 not in self.graph[class2]:
                        self.graph[class1].append(class2)
                        self.graph[class2].append(class1)
                    else:
                        print("This connection already exist.")
            else:
                print("One or both of the nodes does not exist in this graph.")

    #Encontrar usuario       
    def findUser(self, id):
        exist = False
        for key in self.graph:
            if key.id == id:
                exist = True
        if exist == True:
            print(f"The user '{id}' exist.")
        else:
            print(f"The user '{id}' doesn't exist in this graph.")
        return exist

    #Verificar si existe una conexion   
    def findRelation(self, id1, id2):
        exist = False   
        for key in self.graph:
            if key.id == id1:
                for i in self.graph[key]:
                    if i.id == id2:
                        exist = True
        if exist == True:
            print(f"The relation between '{id1}' and '{id2}' exist.")
        else:
            print(f"The relation between '{id1}' and '{id2}' doesn't exist in this graph.")
        return exist

    #Remover nodo
    def remNode(self, id):
        exist = False
        for key in self.graph:
            if key.id == id:
                exist = True
                self.graph.pop(key)
                break
        for key in self.graph:
            for i in self.graph[key]:
                if i.id == id:
                    self.graph[key].remove(i)

        if exist:
            print(f"The user '{id}' was removed.")     
        else:
            print(f"The user '{id}' doesn't exist in this graph.")

    #Remover relacion
    def remEdge(self, id1, id2):
        if self.findRelation(id1, id2):
            for key in self.graph:
                if key.id == id1:
                    for i in self.graph[key]:
                        if i.id == id2:
                            self.graph[key].remove(i)
                if key.id == id2:
                    for i in self.graph[key]:
                        if i.id == id1:
                            self.graph[key].remove(i)
            print(f"The relation between '{id1}' and '{id2}' has been removed.")   
    
    #Relaciones sugeridas
    def suggestedfriends(self, id):
        exist = self.findUser(id)
        tempSuggested = []
        suggested = []
        if exist:
            print(f"The suggested friends of '{id}' are: ")
            for key in self.graph:
                if key.id == id:
                    for i in self.graph[key]:
                        for j in self.graph[i]:
                            tempSuggested.append(j.id)
            for i in tempSuggested:
                if tempSuggested.count(i) >= 2 and i not in suggested and i != id:
                    suggested.append(i)
            for i in suggested:
                for key in self.graph:
                    if key.id == id:
                        for k in self.graph[key]:
                            if i == k.id:
                                suggested.remove(i)

            if len(suggested) == 0:
                print("There are no suggested friends.")
            else:
                userlist = []
                print(suggested)
                for i in suggested:
                    for key in self.graph:
                        if key.id == i:
                            userlist.append(key)
                for i in userlist:
                    print(i.name, i)
            print()

    #Encontrar el camino entre dos nodos
    def bfspath(self, id1, id2):
        visited = []
        
        exist1 = False
        exist2 = False
        for key in self.graph:
            if key.id == id1:
                class1 = key
                exist1 = True
            if key.id == id2:
                class2 = key
                exist2 = True 

        queue = [[class1]]
        if exist1 and exist2:
            if class1 == class2:
                print("There is no path, because the inputs are the same.")
                return
            while queue: 
                path = queue.pop(0)
                node = path[-1]

                if node not in visited:
                    neighbours = self.graph[node]
                    for neighbour in neighbours:
                        new_path = list(path)
                        new_path.append(neighbour)
                        queue.append(new_path)

                        if neighbour == class2:
                            print(f"The path between the nodes '{id1}' and '{id2}' is: ", end=" ")
                            for i in new_path:
                                print(i.name, end=" ")
                            print()
                            return
                    visited.append(node)
            
            print("The connections between both nodes doesn't exist.")

        else:
            print("One or both of the nodes does not exist in this graph.")


    #Imprimir grafo
    def printGraph(self):
        for key in self.graph:
            print(key.name, ": ", end="")
            for i in self.graph[key]:
                print(i.name,"|", end=" ")
            print()


if __name__ == "__main__":
    graph = graph()
    graph.addNode("JAvier", 90)
    graph.addNode("PErdr", 90)
    graph.addNode("fOrg", 60)
    graph.addNode("LADdvc", 40)
    for key in graph.graph:
        print(key)  
    #graph.printGraph()
    print("\n \n")
    graph.loadJson()
    graph.printGraph()
    print("\n \n")

    for key,value in graph.graph.items():
        print(key, value)
    # graph.addEdge(9,9)
    # graph.addEdge(40,90)
    # graph.addEdge(90,40)
    # graph.addEdge(60,40)
    # graph.addEdge(40,40)
    # graph.addEdge(10,9)
    # graph.printGraph()
    # print("\n \n")
    # graph.bfspath(0, 13)
    # graph.bfspath(25, 1)
    # graph.bfspath(1, 25)
    # graph.bfspath(13 ,13)
    # graph.bfspath(90, 40)
    # graph.bfspath(90, 1)
    # ##
    # graph.findUser(9)
    # graph.findUser(29)
    # graph.findUser(30)
    # graph.findRelation(9,0)
    # graph.findRelation(4,8)
    # graph.findRelation(8,4)
    # graph.findRelation(3,2)
    # for i in range(5,11):
    #     graph.remNode(i)
    # graph.remNode(31)
    # graph.remNode(29)
    # graph.remNode(29)
    # print("\n \n")
    # graph.printGraph()
    # graph.remEdge(15,0)
    # graph.remEdge(0,15)
    # graph.remEdge(1,23)
    # graph.remEdge(25,21)
    # graph.remEdge(35,51)
    # graph.remEdge(2,51)
    # print("\n \n")
    # graph.printGraph()
    # graph.suggestedfriends(16)
    # graph.suggestedfriends(12)
    # graph.suggestedfriends(29)
    graph.suggestedfriends(40)


