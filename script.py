# Fundamentos da Programação - Primeiro Projeto - 2022-23 #





# 1 - Justificação de textos


def limpa_texto(texto):
  """
  Remove os caracteres de escape, espaços repetidos e espaços no início e fim
  de uma string.

  Args / Returns: str --> str 
  """

  return " ".join(texto.split())


def corta_texto(texto, largura):
  """
  Corta o texto em duas strings:
  --> texto_cortado: contém todas as palavras completas desde o início do texto
      até a um comprimento máximo igual à largura fornecida 
  --> resto: contém o resto do texto de entrada

  Args / Returns: str, int --> str, str
  """

  texto_cortado, resto = '', ''
  
  if largura < len(texto):
    # Recuar desde o caracter a seguir à largura até encontrar um espaço.
    for i in range(largura, -1, -1):
      if texto[i] == ' ':
        texto_cortado = texto[:i]
        resto = texto[i+1:]
        break
  else:
    texto_cortado = texto
  
  return texto_cortado, resto

  
def insere_espacos(texto, largura):
  """
  Insere, entre as palavras, os espaços necessários e de forma uniforme de
  maneira a que a string fique com tamanho igual à largura dada.
  Se for só uma palavra, acrescentar os espaços necessários no fim.

  Args / Returns: str, int --> str
  """

  lista_palavras = texto.split()
  texto_com_espacos = ''

  if len(lista_palavras) >= 2:
    num_espacos_texto_entrada = len(lista_palavras) - 1
    num_espacos_necessarios = largura - (len(texto) - num_espacos_texto_entrada)

    for i in range(num_espacos_texto_entrada):
      espacos_por_palavra = num_espacos_necessarios // num_espacos_texto_entrada
      espacos_sobra = num_espacos_necessarios % num_espacos_texto_entrada
      
      if i < espacos_sobra:
        texto_com_espacos += lista_palavras[i] + ' ' * (espacos_por_palavra + 1)
      else:
        texto_com_espacos += lista_palavras[i] + ' ' * espacos_por_palavra

    return texto_com_espacos + lista_palavras[-1]
  
  else:
    return texto + ' ' * (largura - len(texto))


def justifica_texto(texto, largura):
  """
  Cria um tuplo correspondente ao texto justificado, ou seja, com strings sem
  caracteres brancos, com comprimento igual à largura e com número correto de
  espaços entre palavras.

  Args / Returns: str, int --> tuple
  """

  # Verificar validade dos argumentos
  if not (type(texto) == str and type(largura) == int and texto != ''):
    raise ValueError("justifica_texto: argumentos invalidos")
  
  # Verificar se alguma palavra é maior que a largura da coluna
  for palavra in texto.split():
    if len(palavra) > largura:
      raise ValueError("justifica_texto: argumentos invalidos")

  texto_justificado = ()
  resto = limpa_texto(texto)

  while len(resto) >= largura:
    texto_cortado, resto = corta_texto(resto, largura)
    texto_justificado += (insere_espacos(texto_cortado, largura),)

  if resto != '':
    texto_justificado += (resto + ' ' * (largura - len(resto)),)
  
  return texto_justificado





# 2 - Método de Hondt


def calcula_quocientes(dict_votos, num_dep):
  """
  Devolve o dicionário do tipo {'partido': [x1, x2, ... , xn], ...}:
  --> mesmos partidos do dicionário argumento
  --> listas de comprimento igual ao número de deputados e com os quocientes
      calculados com o método de Hondt por ordem decrescente. 

  Args / Returns: dict, int --> dict

  dict_votos = {'partido': num_votos, ...}
  """

  lista_partidos = list(dict_votos.keys())
  dict_quocientes = {}

  for partido in lista_partidos:
    dict_quocientes[partido] = [dict_votos[partido] / n 
                                for n in range(1, num_dep + 1)]
  
  return dict_quocientes


def atribui_mandatos(dict_votos, num_dep):
  """
  Devolve a lista ordenada de tamanho igual ao número de deputados e com os
  partidos que obtiveram cada mandato

  Args / Returns: dict, int --> list
  """

  dict_quocientes = calcula_quocientes(dict_votos, num_dep)
  lista_mandatos = []
  
  # template da lista que contém o partido com maior quociente de cada iteração
  maior_quociente = ['partido', 0] 

  for _ in range(num_dep):
    for partido, quociente in dict_quocientes.items():
      # comparar quocientes mais altos de cada partido com o maior_quociente
      # se forem iguais escolher o que tiver menor número de votos
      if (quociente[0] > maior_quociente[1] or
              (quociente[0] == maior_quociente[1] and 
              dict_votos[partido] < dict_votos[maior_quociente[0]])):
        maior_quociente[0] = partido
        maior_quociente[1] = quociente[0]

    lista_mandatos += [maior_quociente[0]]
    del dict_quocientes[maior_quociente[0]][0]
    maior_quociente = ['partido', 0]
  
  return lista_mandatos


def obtem_partidos(info):
  """
  Devolve a lista por ordem alfabética com o nome de todos os partidos que
  participaram nas eleições (de vários territórios)

  Args / Returns: dict --> list

  info = {'território': {'deputados': int, 'votos': {'partido': int, ...}}, ...}
  """

  lista_partidos = []

  for circulo in info.values():
    lista_partidos += [partido for partido in circulo['votos'].keys()
                               if partido not in lista_partidos]

  return sorted(lista_partidos)


def obtem_resultado_eleicoes(info):
  """
  Devolve a lista com os resultados das eleições e de comprimento igual ao
  número total de partidos.
  A lista está ordenada por ordem descendente do número de deputados obtidos e,
  em caso de empate, do número de votos.
  
  Args / Returns: dict --> list

  info = {'território': {'deputados': int, 'votos': {'partido': int, ...}}, ...}
  resultados = [('partido', num_dep, num_votos), ...]
  """

  # Funções auxiliares
  def dict_eh_valido(d):
    if type(d) == dict and d:
      for territorio, circulo in d.items():
        if not (type(territorio) == str and circulo_eh_valido(circulo)):
          return False
      return True
    return False

  def circulo_eh_valido(c):
    return (type(c) == dict and len(c) == 2 and 
            'deputados' in c and 'votos' in c and
            votos_eh_valido(c['votos']) and
            sum(c['votos'].values()) != 0 and
            deputados_eh_valido(c['deputados']))

  def deputados_eh_valido(n):
    return type(n) == int and n > 0

  def votos_eh_valido(d):
    if type(d) == dict and d:
      for partido, votos in d.items():
        if not (type(partido) == str and
                type(votos) == int and votos >= 0):
          return False
      return True
    return False

  # Verificar validade dos argumentos:
  if not dict_eh_valido(info):
    raise ValueError("obtem_resultado_eleicoes: argumento invalido")
  
  lista_partidos = obtem_partidos(info)
  resultados = []

  # criar template da lista resultados
  for partido in lista_partidos:
    resultados += [[partido, 0, 0]]
  
  for circulo in info.values():
    lista_mandatos = atribui_mandatos(circulo['votos'], circulo['deputados'])

    for partido in circulo['votos'].keys():
      resultados[lista_partidos.index(partido)][1] += lista_mandatos.count(partido)
      resultados[lista_partidos.index(partido)][2] += circulo['votos'][partido]

  resultados = sorted(resultados, reverse = True, key=lambda l: (l[1], l[2]))
  # "key=lambda l: (l[1], l[2])" diz ao sorted que queremos que, para cada lista
  #  em resultados, tome l[1] (número de deputados obtidos) como sorting key e,
  #  em caso de empate, l[2] (número de votos) 

  for i in range(len(resultados)):
    resultados[i] = tuple(resultados[i])

  return resultados





# 3 - Solução de Sistemas de Equações


def produto_interno(vetor1, vetor2):
  """
  Faz o produto interno de dois vetores

  Args / Returns: tuple, tuple --> float
  """

  res = 0

  for i in range(len(vetor1)):
    res += vetor1[i] * vetor2[i]

  return float(res)


def verifica_convergencia(A, c, x, e):
  """
  Verifica se o valor absoluto do erro de todas as equações é inferior à precisão
  --> | fi(x) - ci | < e , sendo i o número de equações do sistema
  
  Args / Returns: tuple, tuple, tuple, float --> bool

  A --> matriz A
  c --> vetor das constantes
  x --> vetor com soluções atuais
  e --> valor da precisão

  fi(x) = Ai x = A[i][1]*x1 + A[i][2]*x2 + ... + A[i][n]*xn
  Ou seja:
  fi(x) = produto interno dos vetores Ai e x
  """

  for i in range(len(A)): # i --> linhas de A
    if abs(produto_interno(A[i], x) - c[i]) >= e:
      return False
  return True


def retira_zeros_diagonal(A, c):
  """
  Troca as linhas da matriz A e as respetivas linhas do vetor c de maneira a
  que não haja zeros na diagonal principal de A

  Args / Returns: tuple, tuple --> tuple, tuple

  Elemento da diagonal --> A[i][i]
  """

  matriz_A, vetor_c = list(A), list(c)

  for i in range(len(A)): # i --> linhas de A
    if matriz_A[i][i] == 0:
      for j in range(len(A)): # j --> novas linhas de A
        if matriz_A[j][i] != 0 and matriz_A[i][j] != 0:
          # trocar linhas da matriz e do vetor
          matriz_A[i], matriz_A[j] = matriz_A[j], matriz_A[i]
          vetor_c[i], vetor_c[j] = vetor_c[j], vetor_c[i]
          break

  return tuple(matriz_A), tuple(vetor_c)


def eh_diagonal_dominante(A):
  """
  Verifica se a matriz A é diagonal dominante, ou seja:
  --> |A[i][i]| >= soma |A[i][j]|
  Para j != i (elementos que não fazem parte da diagonal principal) e para
  todas as linhas i

  Args / Returns: tuple --> bool
  """

  for i in range(len(A)):
    soma_restantes_el = sum([abs(el) for j, el in enumerate(A[i]) if j != i])
    if abs(A[i][i]) < soma_restantes_el:
      return False
  return True


def resolve_sistema(A, c, e):
  """
  Calcula as soluções do sistema aplicando o método de Jacobi

  Args / Returns: tuple, tuple, float --> tuple

  A --> matriz A
  c --> vetor das constantes
  e --> valor da precisão
  """

  # Funções auxiliares
  def matriz_eh_valida(A):
    if type(A) == tuple and A != ():
      for i in range(len(A)):
        if not (type(A[i]) == tuple and tuplo_eh_valido(A[i], len(A))):
          return False
      return True
    return False

  def tuplo_eh_valido(t, comp):
    if type(t) == tuple and t != () and len(t) == comp:
      for i in range(comp):
        if not (type(t[i]) == float or type(t[i]) == int):
          return False
      return True
    return False

  def precisao_eh_valida(e):
    return (type(e) == float and e > 0)

  # Verificar validade dos argumentos
  if not (matriz_eh_valida(A) and
          tuplo_eh_valido(c, len(A)) and
          precisao_eh_valida(e)):
    raise ValueError("resolve_sistema: argumentos invalidos")

  A, c = retira_zeros_diagonal(A, c)

  # Verificar se A é diagonal dominante
  if not eh_diagonal_dominante(A):
    raise ValueError("resolve_sistema: matriz nao diagonal dominante")

  # solução nula
  solucao_sistema = [0] * len(A)
  solucao_anterior = solucao_sistema.copy()

  while not verifica_convergencia(A, c, solucao_sistema, e):
    for i in range(len(solucao_sistema)):
      solucao_sistema[i] += (c[i] - produto_interno(A[i], solucao_anterior))/A[i][i]
    solucao_anterior = solucao_sistema.copy()

  return tuple(solucao_sistema)

