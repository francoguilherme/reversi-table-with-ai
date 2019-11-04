from anytree import RenderTree
from models.playNode import PlayNode
from models.move import Move

class BestPlayer:
  MAX_DEPTH = 4

  def __init__(self, color):
    self.color = color

  def play(self, board):
    import time

    start_time = time.time()

    root = PlayNode(name="root", color="")    
    self.generateTree(board, root)
    
    if self.color == board.BLACK:
      root.value = self.negamaxAlfaBeta(root, -float("inf"), float("inf"), 1)
    elif self.color == board.WHITE:
      root.value = -self.negamaxAlfaBeta(root, -float("inf"), float("inf"), -1)

    candidates=[child.move for child in root.children if child.value == root.value]
    bestMove = self.getNearestCorner(candidates)

    elapsed_time = time.time() - start_time

    #for pre, fill, node in RenderTree(root):
    #  if node==root:
    #    print "%s%s = %f" % (pre, node.name, node.value)
    #  else:
    #    if node.value != None:
    #      print "%s%s_X:%d_Y:%d = %f" % (pre, node.color, node.move.x, node.move.y, node.value)
    #    else:
    #      print "%s%s_X:%d_Y:%d" % (pre, node.color, node.move.x, node.move.y)
    print "Total time:", elapsed_time

    return bestMove

  def generateTree(self, board, root):
    if root.depth >= self.MAX_DEPTH:
      root.value = self.heuristic(board)
      return

    #Save current player color and switch to generate opponent moves
    current = self.color
    self.color = board._opponent(self.color)

    previousMove = [0,0]
    for move in board.valid_moves(current):
      if move.x == previousMove[0] and move.y == previousMove[1]:
        continue
      node = PlayNode(color=self.color, move=move, parent=root)
      previousMove[0] = move.x
      previousMove[1] = move.y
      clone = board.get_clone()
      clone.play(move, current)
      self.generateTree(clone, node)
    
    if root.is_leaf:
      #Significa que oponente nao tem jogadas, entao se calcula a heuristica desse no tambem
      root.value = self.heuristic(board)

    #After generating opponent moves, return original color
    self.color = board._opponent(self.color)

  def negamaxAlfaBeta(self, node, alfa, beta, player):

    if node.is_leaf:
      return player * node.value
    value = -float("inf")

    if node.children != None:
      for child in node.children:
        value = max(value, -self.negamaxAlfaBeta(child, -beta, -alfa, -player))
        alfa = max(alfa, value)
        
        if alfa >= beta:
          break
    
    if node.depth == 1:
      node.value = player * value
    return value

  def heuristic(self, board):
    my_color = self.color
    opp_color = board._opponent(self.color)
    empty = '.'
    qtd_pecas = quinas_ocupadas = quinas_proximas = mobilidade = valor_peca_estatico = 0.0

    cores = board.score()
    if my_color == board.BLACK:
      my_tiles = cores[1]
      opp_tiles = cores[0]
    elif my_color == board.WHITE:
      my_tiles = cores[0]
      opp_tiles = cores[1]

    #qtd de pecas no tabuleiro
    qtd_pecas = 100 * (my_tiles - opp_tiles) / (my_tiles + opp_tiles)

    #valores de cada peca no tabuleiro
    peso_estatico_das_pecas = [
        [4, -3, 2, 2, 2, 2, -3, 4],
        [-3, -4, -1 -1, -1, -1, -1, -4, -3],
        [2, -1, 1, 0, 0, 1, -1, 2],
        [2, -1, 0, 1, 1, 0, -1, 2],
        [2, -1, 0, 1, 1, 0, -1, 2],
        [2, -1, 1, 0, 0, 1, -1, 2],
        [-3, -4, -1, -1, -1, -1, -4, -3],
        [4, -3, 2, 2, 2, 2, -3, 4]
    ]

    my_tiles = opp_tiles = 0
    for i in range(0,8):
        for j in range(0,8):
            if board.get_square_color(i+1,j+1) == my_color:
                my_tiles += 1
            elif board.get_square_color(i+1,j+1) == opp_color:
                opp_tiles += 1
    valor_peca_estatico = my_tiles - opp_tiles

    #quinas ocupadas
    my_tiles = opp_tiles = 0
    if board.get_square_color(1,1) == my_color:
      my_tiles += 1
    elif board.get_square_color(1,1) == opp_color:
      opp_tiles += 1
    if board.get_square_color(1,8) == my_color:
      my_tiles += 1
    elif board.get_square_color(1,8) == opp_color:
      opp_tiles += 1
    if board.get_square_color(8,1) == my_color:
      my_tiles += 1
    elif board.get_square_color(8,1) == opp_color:
      opp_tiles += 1
    if board.get_square_color(8,8) == my_color:
      my_tiles += 1
    elif board.get_square_color(8,8) == opp_color:
      opp_tiles += 1
    quinas_ocupadas = 25 * (my_tiles - opp_tiles)

    #prximidade das quinas
    my_tiles = opp_tiles
    if board.get_square_color(1,1) == empty:
      if board.get_square_color(1,2) == my_color:
        my_tiles += 1
      elif board.get_square_color(1,2) == opp_color:
        opp_tiles += 1
      if board.get_square_color(2,2) == my_color:
        my_tiles += 1
      elif board.get_square_color(2,2) == opp_color:
        opp_tiles += 1
      if board.get_square_color(2,1) == my_color:
        my_tiles += 1
      elif board.get_square_color(2,1) == opp_color:
        opp_tiles += 1

    if board.get_square_color(1,8) == empty:
      if board.get_square_color(1,7) == my_color:
        my_tiles += 1
      elif board.get_square_color(1,7) == opp_color:
        opp_tiles += 1
      if board.get_square_color(2,7) == my_color:
        my_tiles += 1
      elif board.get_square_color(2,7) == opp_color:
        opp_tiles += 1
      if board.get_square_color(2,8) == my_color:
        my_tiles += 1
      elif board.get_square_color(2,8) == opp_color:
        opp_tiles += 1
    
    if board.get_square_color(8,1) == empty:
      if board.get_square_color(8,2) == my_color:
        my_tiles += 1
      elif board.get_square_color(8,2) == opp_color:
        opp_tiles += 1
      if board.get_square_color(7,2) == my_color:
        my_tiles += 1
      elif board.get_square_color(7,2) == opp_color:
        opp_tiles += 1
      if board.get_square_color(7,1) == my_color:
        my_tiles += 1
      elif board.get_square_color(7,1) == opp_color:
        opp_tiles += 1      
    
    if board.get_square_color(8,8) == empty:
      if board.get_square_color(7,8) == my_color:
        my_tiles += 1
      elif board.get_square_color(7,8) == opp_color:
        opp_tiles += 1
      if board.get_square_color(7,7) == my_color:
        my_tiles += 1
      elif board.get_square_color(7,7) == opp_color:
        opp_tiles += 1
      if board.get_square_color(8,7) == my_color:
        my_tiles += 1
      elif board.get_square_color(8,7) == opp_color:
        opp_tiles += 1
    quinas_proximas = -12.5 * (my_tiles - opp_tiles)

    score = (25 * qtd_pecas) + (30 *(quinas_ocupadas + quinas_proximas)) + valor_peca_estatico

    if my_color == 'o':
      return -score
    else:
      return score

  def getNearestCorner(self, moves):
    import math
    corners = [[1,1],[1,8], [8,1], [8,8]]
    minDist = 10
    retMove = None
    for move in moves:
      for corner in corners:
        distX = abs(corner[0] - move.x)
        distY = abs(corner[1] - move.y)
        dist  = math.sqrt(distX*distX + distY*distY)
        if dist < minDist:
          minDist = dist
          retMove = move

    return retMove