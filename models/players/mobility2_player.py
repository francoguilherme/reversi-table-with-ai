from anytree import RenderTree

from models.board import Board
from models.playNode import PlayNode
from models.move import Move

class Mobility2Player:
  from time import time

  MAX_DEPTH = 3
  TIME_LIMIT = 3.0

  def __init__(self, color):
    self.color = color
    self.start_time = 0
    self.elapsed_time = 0

  def play(self, board):
    self.start_time = self.time()

    root = PlayNode(name="root", color="")    
    self.generateTree(board, root)
    
    if self.color == board.BLACK:
      root.value = self.negamaxAlfaBeta(root, -float("inf"), float("inf"), 1)
    elif self.color == board.WHITE:
      root.value = -self.negamaxAlfaBeta(root, -float("inf"), float("inf"), -1)

    candidates=[child.move for child in root.children if child.value == root.value]
    bestMove = self.getNearestCorner(candidates)

    self.elapsed_time = self.time() - self.start_time

    #for pre, fill, node in RenderTree(root):
    #  if node==root:
    #    print "%s%s = %f" % (pre, node.name, node.value)
    #  else:
    #    if node.value != None:
    #      print "%s%s_X:%d_Y:%d = %f" % (pre, node.color, node.move.x, node.move.y, node.value)
    #    else:
    #      print "%s%s_X:%d_Y:%d" % (pre, node.color, node.move.x, node.move.y)
    print "Total time:", self.elapsed_time

    return bestMove

  def generateTree(self, board, root):
    # Corte por limite de profundidade OU Corte de tempo (com margem de erro)
    if root.depth >= self.MAX_DEPTH or self.time() - self.start_time >= self.TIME_LIMIT*0.95:
      root.value = self.heuristic(board)
      return

    # Save current player color and switch to generate opponent moves
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
    p = c = l = m = 0.0

    cores = board.score()
    my_tiles = cores[0]
    opp_tiles = cores[1]

    #qtd de pecas no tabuleiro
    if my_tiles > opp_tiles:
      p = (100.0 * my_tiles)/(my_tiles + opp_tiles)
    elif my_tiles < opp_tiles:
      p = -(100.0 * opp_tiles)/(my_tiles + opp_tiles)
    else:
      p = 0

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
    c = 25 * (my_tiles - opp_tiles)

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
    l = -12.5 * (my_tiles - opp_tiles)

    #mobilidade
    my_tiles = self.count_valid_moves(board, my_color)
    opp_tiles = self.count_valid_moves(board, opp_color)
    if my_tiles > opp_tiles:
      m = (100.0 * my_tiles)/(my_tiles + opp_tiles)
    elif my_tiles < opp_tiles:
      m = -(100.0 * opp_tiles)/(my_tiles + opp_tiles)
    else:
      m = 0

    score = (10 * p) + (801.724 * c) + (382.026 * l) + (78.922 * m)
    if my_color == 'o':
      return -score
    else:
      return score

  @staticmethod
  def getNearestCorner(moves):
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

  @staticmethod
  def count_valid_moves(board, color):
    ret = 0
    for i in range(1, 9):
      for j in range(1, 9):
        if board.board[i][j] == Board.EMPTY:
          for direction in Board.DIRECTIONS:
            bracket = board._find_bracket(Move(i, j), color, direction)
            if bracket:
              ret += 1
    return ret
