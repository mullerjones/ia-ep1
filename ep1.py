"""
  AO PREENCHER ESSE CABECALHO COM O MEU NOME E O MEU NUMERO USP,
  DECLARO QUE SOU A UNICA PESSOA AUTORA E RESPONSAVEL POR ESSE PROGRAMA.
  TODAS AS PARTES ORIGINAIS DESSE EXERCICIO PROGRAMA (EP) FORAM
  DESENVOLVIDAS E IMPLEMENTADAS POR MIM SEGUINDO AS INSTRUCOES
  DESSE EP E, PORTANTO, NAO CONSTITUEM ATO DE DESONESTIDADE ACADEMICA,
  FALTA DE ETICA OU PLAGIO.
  DECLARO TAMBEM QUE SOU A PESSOA RESPONSAVEL POR TODAS AS COPIAS
  DESSE PROGRAMA E QUE NAO DISTRIBUI OU FACILITEI A
  SUA DISTRIBUICAO. ESTOU CIENTE QUE OS CASOS DE PLAGIO E
  DESONESTIDADE ACADEMICA SERAO TRATADOS SEGUNDO OS CRITERIOS
  DIVULGADOS NA PAGINA DA DISCIPLINA.
  ENTENDO QUE EPS SEM ASSINATURA NAO SERAO CORRIGIDOS E,
  AINDA ASSIM, PODERAO SER PUNIDOS POR DESONESTIDADE ACADEMICA.

  Nome : Alexandre Muller Jones
  NUSP : 8038149

  Referencias: Com excecao das rotinas fornecidas no enunciado
  e em sala de aula, caso voce tenha utilizado alguma referencia,
  liste-as abaixo para que o seu programa nao seja considerado
  plagio ou irregular.

  Exemplo:
  - O algoritmo Quicksort foi baseado em:
  https://pt.wikipedia.org/wiki/Quicksort
  http://www.ime.usp.br/~pf/algoritmos/aulas/quick.html
"""

import util
import time

addEspaco = "addEspaco"
movEspaco = "movEspaco"

############################################################
# Part 1: Segmentation problem under a unigram model

#Defini o estado como uma tupla de inteiros positivos maiores do que 1
#Cada número representa um ponto de inserção de um espaço na string original

class SegmentationProblem(util.Problem):
    def __init__(self, query, unigramCost):
        self.query = query
        self.unigramCost = unigramCost

    def isState(self, state):
        """ Metodo que implementa verificacao de estado """
        #apenas verifica se todos os valores do estado estão corretos
        #nunca é chamada pois o estado é bem construído
        for each in state:
            if each > len(query) or each < 0:
                return False
        
        return True

    def initialState(self):
        """ Metodo que implementa retorno da posicao inicial """
        #Estado inicial é apenas um espaço no primeiro lugar possivel
        state = (1,)
        return state

    def actions(self, state):
        """ Metodo que implementa retorno da lista de acoes validas
        para um determinado estado
        """
        #As ações possiveis são:
        #1) adicionar um espaço na tupla (ou seja, aumentar o numero palavras que formarão a string final)
        #2) mover o ultimo espaço (ou seja, mudar apenas onde as palavras se separam)
        acoes = []
        if state[-1] != len(self.query):
            acoes.append(movEspaco)

        if len(state) < len(self.query):
            acoes.append(addEspaco)

        return acoes

    def nextState(self, state, action):
        """ Metodo que implementa funcao de transicao """
        #se a ação é adicionar um espaço, adiciona um no proximo espaço possível depois do ultimo existente
        if action == addEspaco:
            aux = state[-1]
            state = state + (aux+1,)
        #se a ação é mover o espaço, move o ultimo espaço da tupla uma posição para a frente
        if action == movEspaco:
            aux = state[-1]
            state = state[:-1] + (aux+1,)
        return state

    def isGoalState(self, state):
        """ Metodo que implementa teste de meta """
        #é estado meta se dividiu a string em palavras que todas estao abaixo de 10
        #em outras palavras, se todas as palavras estão no corpus
        copiaQuery = self.query #copia query para versão destrutivel
        listaPalavras = []      #inicializa lista das palavras apos divisao
        aux = ""                #string auxiliar para guardar cada palavra
        for i in range(len(state)):
            j = i+1
            aux = copiaQuery[state[-j]:]        #aux recebe a ultima palavra
            listaPalavras.append(aux)           #essa palavra eh colocada na lista
            copiaQuery = copiaQuery[:state[-j]] #essa palavra eh removida do fim da copia
        listaPalavras.append(copiaQuery)        #adiciona o restante da string (que representa uma palavra)

        #aqui, listaPalavras contém todas as palavras da string, em ordem inversa
        #como o modelo é um modelo de unigramas, a ordem das palavras não importa
        #este próximo trecho remove palavras vazias da lista,
        # o que ocorre em alguns casos nessa modelagem, especialmente para palavras unicas
        i = 0
        length = len(listaPalavras)
        while(i<length):
            if listaPalavras[i] == '':
                listaPalavras.remove(listaPalavras[i])
                length = length - 1
            else:
                i = i+1
        
        #para cada palavra na lista, checa se seu custo é maior que o limiar estabelecido
        for palavra in listaPalavras:
            if self.unigramCost(palavra) > 10: #Se qualquer palavra nao estiver no corpus
                return False                   #tera custo > 10 e retorna False
        #Se chegou aqui, nao retornou False
        #Ou seja, todas as palavras estao no corpus e eh estado meta
        return True

    def stepCost(self, state, action):
        """ Metodo que implementa funcao custo """
        #obtem próximo estado a partir da ação passada
        nxtState = self.nextState(state, action)
        #Separa a query da mesma forma que o isGoalState usando o pŕoximo estado (nxtState)
        copiaQuery = self.query
        listaPalavras = []
        aux = ""
        for i in range(len(nxtState)):
            j = i+1
            aux = copiaQuery[nxtState[-j]:]
            listaPalavras.append(aux)
            copiaQuery = copiaQuery[:nxtState[-j]]
        listaPalavras.append(copiaQuery)
        #calcula custo de cada palavra e soma num total
        custoTotal = 0.0
        for palavra in listaPalavras:
            custoTotal += self.unigramCost(palavra)
        
        #retorna custo total do próximo estado
        return custoTotal


def segmentWords(query, unigramCost):

    if len(query) == 0:
        return ''
     
    # BEGIN_YOUR_CODE 
    # Voce pode usar a funo getSolution para recuperar a sua soluo a partir do no meta
    # valid,solution  = util.getSolution(goalNode,problem)
    prob = SegmentationProblem(query, unigramCost)
    goal = util.uniformCostSearch(prob)
    #separa as palavras como o isGoalState usando o estado meta
    listaPalavras = []
    aux = ""
    copQuery = query
    for i in range(len(goal.state)):
        j = i+1
        aux = copQuery[goal.state[-j]:]
        listaPalavras.append(aux)
        copQuery = copQuery[:goal.state[-j]]
    listaPalavras.append(copQuery)
    #Como a lista contem as palavras em ordem reversa, a inverte para montar a string de saida
    listaPalavras.reverse()
    #novamente, remove os espacos vazios
    i = 0
    length = len(listaPalavras)
    while(i<length):
        if listaPalavras[i] == '':
            listaPalavras.remove(listaPalavras[i])
            length = length - 1
        else:
            i = i+1
    aux = ""
    #adiciona na saida cada palavra e um espaço
    for palavra in listaPalavras:
        aux += palavra
        aux += " "
    return aux[:-1] #retorna string de saida sem o espaço final desnecessário

    # END_YOUR_CODE

############################################################
# Part 2: Vowel insertion problem under a bigram cost

#Modelei este problema a partir do possibleFills
#Cada conjunto de consoantes da entrada tem uma lista correspondente de possiveis palavras que pode formar
#Desta forma, modelei o estado como uma combinação de alguma palavra dos possibleFills de cada bloco da entrada
#Entretando, o possibleFills retorna um set, que não é ordenado
#Portanto, foi necessário criar uma classe de apoio que contenha os possibleFills em uma lista,
#de modo que cada palavra tenha um indice que possa ser referenciado

class VowelInsertionProblem(util.Problem):

    #Classe auxiliar criada para este fim
    class listaFills:
        def __init__(self, queryWords, possibleFills):
            #classe precisa da lista de palavras, da funcao possiblefills e a lista que sera montada
            self.queryWords = queryWords
            self.possibleFills = possibleFills
            self.lFills = []
        
        #unica funcao dessa classe é criar o lFills a partir da entrada
        def create(self):
            for word in self.queryWords:
                aux = self.possibleFills(word) #obtem o set
                auxL = []                      #cria uma lista auxiliar
                for each in aux:               #para cada item do set, o adiciona na lista
                    auxL.append(each)          
                self.lFills.append(auxL)       #adiciona a lista criada no lFills
            return self.lFills                 #retorna a lista de listas

    def __init__(self, queryWords, bigramCost, possibleFills):
        self.queryWords = queryWords
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills
        #lFills mantera no proprio objeto do problema a lista de listas do possibleFills
        self.lFills = self.listaFills(queryWords, possibleFills)
        self.lFills = self.lFills.create()

    def isState(self, state):
        """ Metodo  que implementa verificacao de estado """
        #confere apenas se nenhum dos indices do estado é maior
        #que o numero de palavras possiveis do possibleFills
        #também não é chamada e não é necessária dado que os estados são bem construídos
        for ii in range(len(state)):
            if state[i] >= len(self.possibleFills(queryWords[i])):
                return False
        
        return True

    def initialState(self):
        """ Metodo  que implementa retorno da posicao inicial """
        #estado inicial tem todos os indices como 0
        #Aqui, usamos uma string ao inves de uma tupla para facilitar a interação com
        #indices em qualquer posição, o que não é possivel com uma tupla
        aux = ""
        for i in range(len(self.queryWords)):
            aux += "0 "
        return aux[:-1]

    def actions(self, state):
        """ Metodo  que implementa retorno da lista de acoes validas
        para um determinado estado
        """
        #so ha uma acao possivel - mudar qual palavra se esta escolhendo de algum
        #possibleFills. Portanto, as acoes possiveis sao quais indices podem ser mudados
        lista = state.split()
        acoes = []
        for ii in range(len(lista)):
            if int(lista[ii]) < len(self.lFills[ii]) - 1: #se determinado indice ja esta no maximo, ele nao pode mudar
                acoes.append(ii) #adiciona o indice de qual palavra pode mudar na lista de acoes
        
        return acoes

    def nextState(self, state, action):
        """ Metodo que implementa funcao de transicao """
        #proximo estado é adicionar 1 no número de indice passado no action
        aux = state.split() #desmonta string
        aux[action] = str(int(aux[action]) + 1) #adiciona 1 no lugar indicado
        #remonta a string
        nxtState = ""
        for each in aux:
            nxtState += each
            nxtState += " "
        
        return nxtState[:-1]

    def isGoalState(self, state):
        """ Metodo que implementa teste de meta """
        #confere se todos os bigramas tem custo menos que 13, limiar escolhido para boas formacoes
        lista = state.split()
        lPalavras = []
        #monta lista de palavras a partir do estado e de lFills
        for ii in range(len(lista)):
            listaDessa = self.lFills[ii]
            index = int(lista[ii])
            if len(listaDessa) == 0:
                lPalavras.append(self.queryWords[ii])
            else:
                lPalavras.append(listaDessa[index])
        
        #checa custo de cada bigrama
        custo = 0.0
        for ii in range(len(lPalavras)):
            if ii == 0:
                custo = self.bigramCost('-BEGIN-',lPalavras[0])
            else:
                custo = self.bigramCost(lPalavras[ii-1], lPalavras[ii])
            
            if custo > 13:
                return False
        
        return True
        
    def stepCost(self, state, action):
        """ Metodo que implementa funcao custo """
        nxtState = self.nextState(state, action)
        lista = nxtState.split()
        lPalavras = []
        for ii in range(len(lista)):
            lPalavras.append(self.lFills[ii][int(lista[ii])])
        #aqui, lPalavras tem a lista de palavras correspondentes ao proximo estado
        #calculando custo total do proximo estado
        custoTotal = 0.0
        for ii in range(len(lPalavras)):
            if ii == 0:
                custoTotal += self.bigramCost('-BEGIN-',lPalavras[0])
            else:
                custoTotal += self.bigramCost(lPalavras[ii-1], lPalavras[ii])
        
        return custoTotal
    
    #funcao extra que rotorna string de saida a partir de um determinado estado
    def devolveString(self, state):
        out = ""
        lista = state.split()
        lPalavras = []
        for ii in range(len(lista)):
            index = int(lista[ii])
            lPalavras.append(self.lFills[ii][index])
        out = ' '.join(lPalavras)
        return out



def insertVowels(queryWords, bigramCost, possibleFills):
    # BEGIN_YOUR_CODE 
    # Voce pode usar a função getSolution para recuperar a sua solução a partir do no meta
    # valid,solution  = util.getSolution(goalNode,problem)
    prob = VowelInsertionProblem(queryWords, bigramCost, possibleFills)
    goal = util.uniformCostSearch(prob)
    if goal == None:
        saida = ' '.join(queryWords)
    else:
        saida = prob.devolveString(goal.state)
    return saida
    # END_YOUR_CODE

############################################################


def getRealCosts(corpus='corpus.txt'):

    """ Retorna as funcoes de custo unigrama, bigrama e possiveis fills obtidas a partir do corpus."""
    
    _realUnigramCost, _realBigramCost, _possibleFills = None, None, None
    if _realUnigramCost is None:
        print('Training language cost functions [corpus: '+ corpus+']... ')
        
        _realUnigramCost, _realBigramCost = util.makeLanguageModels(corpus)
        _possibleFills = util.makeInverseRemovalDictionary(corpus, 'aeiou')

        print('Done!')

    return _realUnigramCost, _realBigramCost, _possibleFills

def main():
    """ Voce pode/deve editar o main() para testar melhor sua implementacao.

    A titulo de exemplo, incluimos apenas algumas chamadas simples para
    lhe dar uma ideia de como instanciar e chamar suas funcoes.
    Descomente as linhas que julgar conveniente ou crie seus proprios testes.
    """
    unigramCost, bigramCost, possibleFills  =  getRealCosts()

    resulSegment = segmentWords('believeinyourselfhavefaith', unigramCost)
    print(resulSegment)

    resultInsert = insertVowels('wld lk t hv mr lttrs'.split(), bigramCost, possibleFills)
    print(resultInsert)

if __name__ == '__main__':
    main()
