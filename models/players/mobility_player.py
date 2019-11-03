from anytree import RenderTree
from models.playNode import PlayNode
from models.move import Move

class MobilityPlayer:
  from time import time

  MAX_DEPTH = 3
  TIME_LIMIT = 1.0

  def __init__(self, color):
    self.color = color
    self.start_time = 0
    self.elapsed_time = 0

  def play(self, board):
    start_time = self.time()

    root = PlayNode(name="root", color="")    
    self.generateTree(board, root, start_time)
    
    if self.color == board.BLACK:
      root.value = self.negamaxAlfaBeta(root, -float("inf"), float("inf"), 1)
    elif self.color == board.WHITE:
      root.value = -self.negamaxAlfaBeta(root, -float("inf"), float("inf"), -1)

    candidates=[child.move for child in root.children if child.value == root.value]
    bestMove = self.getNearestCorner(candidates)

    self.elapsed_time = self.time() - start_time

    for pre, fill, node in RenderTree(root):
      if node==root:
        print "%s%s = %f" % (pre, node.name, node.value)
      else:
        if node.value != None:
         print "%s%s_X:%d_Y:%d = %f" % (pre, node.color, node.move.x, node.move.y, node.value)
        else:
          print "%s%s_X:%d_Y:%d" % (pre, node.color, node.move.x, node.move.y)
    print "Total time:", self.elapsed_time
    print "Max depth:", root.height
    print "Leaves:", len(root.leaves)

    return bestMove

  def generateTree(self, board, root, start_time):   
    fila = []
    previousMove = [0,0]

    #Cria filhos do no inicial e adiciona na fila
    for move in board.valid_moves(self.color):
      if move.x == previousMove[0] and move.y == previousMove[1]:
        continue
      node = PlayNode(color=self.color, move=move, board=board.get_clone(), parent=root)
      previousMove[0] = move.x
      previousMove[1] = move.y
      fila.append(node)

    while len(fila):

      if self.time() - start_time >= self.TIME_LIMIT*0.3:
        break

      play = fila.pop(0)
      clone = play.board.get_clone()
      clone.play(play.move, play.color)

      for move in clone.valid_moves(board._opponent(play.color)):
        if move.x == previousMove[0] and move.y == previousMove[1]:
          continue
        node = PlayNode(color=board._opponent(play.color), move=move, board=clone, parent=play)
        previousMove[0] = move.x
        previousMove[1] = move.y
        fila.append(node)
    
    for leaf in root.leaves:
      leaf.value = self.heuristic(leaf.board)

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

    #mobilidade
    count = self.count_valid_moves(board, my_color)
    my_tiles = count[0]
    opp_tiles = count[1]
    if my_tiles + opp_tiles != 0:
        mobilidade = 100 * (my_tiles - opp_tiles) / (my_tiles + opp_tiles)
    else:
        mobilidade = 0

    score = (25 * qtd_pecas) + (30 *(quinas_ocupadas + quinas_proximas)) + (5 * mobilidade) + valor_peca_estatico

    if my_color == 'o':
      return -score
    else:
      return score

  def count_valid_moves(self, board, color):
    my_count = 0
    opp_count = 0
    for i in range(1, 9):
      for j in range(1, 9):
        if board.board[i][j] == board.EMPTY:
          for direction in board.DIRECTIONS:
            move = Move(i, j)

            my_bracket = board._find_bracket(move, color, direction)
            if my_bracket:
              my_count += 1

            opp_bracket = board._find_bracket(move, board._opponent(color), direction)
            if opp_bracket:
              opp_count += 1

    return [my_count, opp_count]

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