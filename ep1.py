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

addEspaco = 20
movEspaco = 30

############################################################
# Part 1: Segmentation problem under a unigram model

class SegmentationProblem(util.Problem):
    def __init__(self, query, unigramCost):
        self.query = query
        self.unigramCost = unigramCost

    def isState(self, state):
        """ Metodo que implementa verificacao de estado """
        for each in state:
            if each > len(query) or each < 0:
                return False
        
        return True

    def initialState(self):
        """ Metodo que implementa retorno da posicao inicial """
        state = (1)
        self.state = state

    def actions(self, state):
        """ Metodo que implementa retorno da lista de acoes validas
        para um determinado estado
        """
        #acoes
        ##adiciona um espaco novo
        ##muda a posicao de um espaco
        raise NotImplementedError

    def nextState(self, state, action):
        """ Metodo que implementa funcao de transicao """
        if action == addEspaco:
            aux = state[-1]
            state = state + (aux+1,)
        if action == movEspaco:
            aux = state[-1]
            state = state[:-1] + (aux+1,)

    def isGoalState(self, state):
        """ Metodo que implementa teste de meta """
        #eh meta se dividiu em palavras que todas estao abaixo de 15
        copiaQuery = query #copia query para versao destrutivel
        listaPalavras = [] #lista das palavras apos divisao
        aux = ""           #string auxiliar para guardar cada palavra
        for i in range(len(state)):
            j = i+1
            aux = copiaQuery[state[-j]:]        #aux recebe a ultima palavra
            listaPalavras.append(aux)           #essa palavra eh colocada na lista
            copiaQuery = copiaQuery[state[-j]:] #essa palavra eh removida do fim da copia
        
        #listaPalavras tem todas as palavras, porem de tras para frente
        #nao invertemos a lista aqui pois a ordem das palavras nao importa nesta etapa
        for palavra in listaPalavras:
            if self.unigramCost(palavra) > 15: #Se qualquer palavra nao estiver no corpus
                return False                   #retorna False
        #Se chegou aqui, nao retornou False
        #Ou seja, todas as palavras estao no corpus e eh estado meta
        return True

    def stepCost(self, state, action):
        """ Metodo que implementa funcao custo """
        #Separa a query com os espacos do estado
        copiaQuery = query
        listaPalavras = []
        aux = ""
        for i in range(len(state)):
            j = i+1
            aux = copiaQuery[state[-j]:]
            listaPalavras.append(aux)
            copiaQuery = copiaQuery[state[-j]:]
        listaPalavras.reverse()
        #calcula custo de cada palavra e custo total
        custoTotal = 0.0
        for palavra in listaPalavras:
            custoTotal += self.unigramCost(palavra)
        
        return custoTotal


def segmentWords(query, unigramCost):

    if len(query) == 0:
        return ''
     
    # BEGIN_YOUR_CODE 
    # Voce pode usar a função getSolution para recuperar a sua solução a partir do no meta
    # valid,solution  = util.getSolution(goalNode,problem)

    raise NotImplementedError

    # END_YOUR_CODE

############################################################
# Part 2: Vowel insertion problem under a bigram cost

class VowelInsertionProblem(util.Problem):
    def __init__(self, queryWords, bigramCost, possibleFills):
        self.queryWords = queryWords
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def isState(self, state):
        """ Metodo  que implementa verificacao de estado """
        raise NotImplementedError

    def initialState(self):
        """ Metodo  que implementa retorno da posicao inicial """
        raise NotImplementedError

    def actions(self, state):
        """ Metodo  que implementa retorno da lista de acoes validas
        para um determinado estado
        """
        raise NotImplementedError

    def nextState(self, state, action):
        """ Metodo que implementa funcao de transicao """
        raise NotImplementedError

    def isGoalState(self, state):
        """ Metodo que implementa teste de meta """
        raise NotImplementedError

    def stepCost(self, state, action):
        """ Metodo que implementa funcao custo """
        raise NotImplementedError



def insertVowels(queryWords, bigramCost, possibleFills):
    # BEGIN_YOUR_CODE 
    # Voce pode usar a função getSolution para recuperar a sua solução a partir do no meta
    # valid,solution  = util.getSolution(goalNode,problem)
    raise NotImplementedError
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
    
    resulSegment = segmentWords('believeinyourselfhavefaithinyourabilities', unigramCost)
    print(resulSegment)
    

    resultInsert = insertVowels('smtms ltr bcms nvr'.split(), bigramCost, possibleFills)
    print(resultInsert)

if __name__ == '__main__':
    main()
