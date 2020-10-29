#coding: utf-8
import argparse
import json
import sys
import os

def arg_parser():
    parser = argparse.ArgumentParser(description='Testa se uma palavra pertence pertence a uma linguagem')
    parser.add_argument('arquivo', help='Inserir o caminho do arquivo .json a ser testado')
    return parser


def open_json(arquivo):
    try:
        with open(arquivo, "r") as json_file:
            dados = json.load(json_file)
    except Exception:
        print("File {} does not exist".format(arquivo))
    return dados


class Pilha:
    def __init__(self):
        self.p = []

    def empilha(self,elemento):
        self.p.append(elemento)
    
    def desempilha(self):
        if self.verifica_pilha_vazia() is False:
            return self.p.pop()
    
    def verifica_pilha_vazia(self):
        if len(self.p) == 0 :
            return True
        else :
            return False
    
    def topo_pilha(self,i): # retorna as i posicoes do topo da pilha
        if self.verifica_pilha_vazia() is False:
                return self.p[-i:]
        else:
            return ['']


def main(dados):    
    #separa o arquivo json nos elemntos que compoem automato
    estados = dados['ap'][0]
    alfabeto = dados['ap'][1]
    alfabeto_pilha = dados['ap'][2]
    transicoes = dados['ap'][3]
    estado_inicial = dados['ap'][4]
    estados_finais = dados['ap'][5]
    
    while(True):
        palavra = str(sys.stdin.readline())

        if not palavra:
            break
        
        palavra = palavra.strip()
        simboloConsumido = True
        estado_atual = estado_inicial
        pilha = Pilha()

        
        #Para cada palavra fornecida, sera verificado o estado atual, o simbolo lido,
        #o que sera desempilhado e/ou empilhado e o próximo estado.

        #simboloConsumido: boolean que passa para True quando o simbolo e lido adequadamente
        
        i = 0

        if palavra != '#':
            while (True):
                # realiza a leitura do array de transicoes do arquivo json
                for transicao in transicoes:
                    simboloConsumido = False
                    transicao_estado_atual = transicao[0]
                    transicao_simbolo = transicao[1]
                    transicao_desempilha = transicao[2]
                    proximo_estado = transicao[3]
                    empilha_elementos = transicao[4]

                    if(transicao_estado_atual == estado_atual and (i < len(palavra))):
                        if (transicao_simbolo == palavra[i] or transicao_simbolo == '#'):
                            if transicao_simbolo == palavra[i]:
                                # pode-se desempilhar nada ou desempilhar um caractere
                                # a transição vai depender do topo da pilha
                                if(transicao_desempilha == '#'): # se não desempilha nada
                                    if (empilha_elementos != '#'):
                                        for elemento in empilha_elementos[::-1]:
                                            pilha.empilha(elemento)
                                    # realiza a transição e muda de estado - se for #, vai de graça pro prox estado
                                    estado_atual = proximo_estado
                                    simboloConsumido = True
                                    i = i + 1

                                elif transicao_desempilha == "".join(pilha.topo_pilha(len(transicao_desempilha))):
                                    for j in range(len(transicao_desempilha)):
                                        pilha.desempilha()
                                    # empilha
                                    if (empilha_elementos != '#'):
                                        for elemento in empilha_elementos[::-1]:
                                            pilha.empilha(elemento)
                                    estado_atual = proximo_estado
                                    simboloConsumido = True
                                    i = i + 1

                            elif transicao_simbolo == '#':
                                # nunca vai desempilhar #, pois eh APD
                                # verifica o topo da pilha
                                if transicao_desempilha == "".join(pilha.topo_pilha(len(transicao_desempilha))):
                                    for j in range(len(transicao_desempilha)):
                                        pilha.desempilha()
                                    # empilha
                                    if (empilha_elementos != '#'):
                                        for elemento in empilha_elementos[::-1]:
                                            pilha.empilha(elemento)
                                    estado_atual = proximo_estado
                                    simboloConsumido = True # é consumido, mas não é consumido
                    else:
                        if(transicao_estado_atual == estado_atual):
                            if transicao_simbolo == '#':
                                if transicao_desempilha == "".join(pilha.topo_pilha(len(transicao_desempilha))):
                                    for j in range(len(transicao_desempilha)):
                                        pilha.desempilha()
                                    # empilha
                                    if (empilha_elementos != '#'):
                                        for elemento in empilha_elementos[::-1]:
                                            pilha.empilha(elemento)
                                    estado_atual = proximo_estado
                                    simboloConsumido = True
                    if simboloConsumido is True:
                        break

                if (simboloConsumido is False) or (i >= len(palavra) and (pilha.verifica_pilha_vazia() is True)) :
                    break

        if(simboloConsumido is True and (pilha.verifica_pilha_vazia()) and estado_atual in estados_finais):
            print("Sim")
        else:
            print("Não")


if __name__ == "__main__":
    parser = arg_parser()
    argumento = parser.parse_args(sys.argv[1:])
    arquivo = argumento._get_kwargs()[0][1]
    
    dados = open_json(arquivo)
    main(dados)