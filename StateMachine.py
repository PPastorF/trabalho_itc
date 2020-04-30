class Transicao(object):
    """Transicao so guarda de onde veio, qual o simbolo transacionado e o destino
        no fim nao precisei disso"""

    def __init__(self,anterior,trans,proximo):
        self.anterior = anterior
        self.trans = trans
        self.proximo = proximo

    def show(self):
        print('[',self.anterior,self.trans,self.proximo,']',sep=' ',end=' ')

class StateMachine(object):
    """StateMachine. Deve calcular AFD e AFN """
    def __init__(self):
        print("Numero de estados:"); self.nq = int(input())
        print("n terminais e conjunto terminais"); temp = input().split()
        self.nAlfabeto = int(temp[0])
        self.alfabeto = temp[1:]
        self.qInciais = [str(i) for i in range(int(input()))]
        temp = input().split()
        
        # Estados serao pesquisados por dict entao pode ser string
        self.nAceitacao = temp[0]
        self.aceitacao = temp[1:]
        self.nTransicoes = int(input())
        self.transicoes = {}

        for i in range(self.nTransicoes):
            anterior, trans, proximo = input().split()
        
            if anterior+trans in self.transicoes.keys():
                self.transicoes[anterior+trans].append(Transicao(anterior,trans,proximo))
            else:
                self.transicoes[anterior+trans] = [Transicao(anterior,trans,proximo)]

        self.nCadeias = int(input())
        self.cadeias = []
        for i in range(self.nCadeias):
            self.cadeias.append(input())

    def status(self):
        print("\n****************** Status ***********************\n")
        print('nq: ',self.nq,' nAlfabeto: ',self.nAlfabeto)
        print('alfabeto: ',end = '')
        print(self.alfabeto)
        print('nInciais')
        print(self.qInciais)
        print(self.nTransicoes,' transicoes:')
        for v in self.transicoes.values():
            v.show()
        print('\n',self.nCadeias,'cadeias: ')
        print(self.cadeias)

    def run(self):
        # rodar para todas cadeias
        resposta = [-1 for i in range(self.nCadeias)] # -1 nao foi avaliado
        for index,cadeia in enumerate(self.cadeias):
            ''' Eu iria validar se as palavras batem com a gramatica, nao sei se isso eh necessario'''
            # validade = 0
            # for simbolo in cadeia: # considere o vazio tbm!
            #     if simbolo not in self.alfabeto:
            #         validade = -1
            #         break
            # else: # inner did not break
            #     continue
            # break # inner did break

            if cadeia == '-' :
                resposta[index] = self.validarCadeiaVazia()
            else:
                resposta[index] = self.validarCadeia(cadeia)

        return resposta

    def validarCadeia(self,cadeia):
        for inicial in self.qInciais:
            q = [inicial]
            passo = [0]
            option = [0] # dentre opcoes
            while(passo[0] < len(cadeia)): #iteracao termina antes do ultimo elemento da cadeia

                if q[0]+cadeia[passo[0]] not in self.transicoes.keys():
                    # q nao tem nenhuma transicao compativel
                    del q[0] # "pop" na pilha(`q`,`passo`) de tarefas
                    del passo[0]
                    del option[0]
                else:
                    for op,new in enumerate(self.transicoes[q[0]+cadeia[passo[0]]][1:]):
                        # verificar multiplicidade em transicoes
                        # push na pilha (`q`,`passo`)
                        q.append(new.proximo)
                        passo.append(passo[0]+1)
                        option.append(option[op+1])

                    # prossegue
                    q[0] = self.transicoes[q[0]+cadeia[passo[0]]][option[0]].proximo
                    passo[0]+=1

            if q[0] in self.aceitacao:
                return 1

        return 0
    # verificar cadeia vazia e retornar validade
    def validarCadeiaVazia(self):
        resposta = 0
        for inicial in self.qInciais:
            if inicial in [str(i) for i in self.aceitacao]:
                resposta = 1
                break

        return resposta

state = StateMachine()
# state.status()
resposta = state.run()
for index,r in enumerate(resposta):
    if r == 1:
        print('{}. aceita'.format(index+1))
    elif r == 0:
        print('{}. rejeita'.format(index+1))
