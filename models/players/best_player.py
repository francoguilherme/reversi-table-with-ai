from anytree import RenderTree
from models.playNode import PlayNode
from models.move import Move

class BestPlayer:
  MAX_DEPTH = 4

  def __init__(self, color):
    self.color = color

  def play(self, board):
    import time

    root = PlayNode(name="root", color="")

    start_time = time.time()
    self.generateTree(board, root)
    elapsed_time = time.time() - start_time
    print "Total time:", elapsed_time

    #for pre, fill, node in RenderTree(root):
    #  print "%s%s" % (pre, node.name)

    return self.getNearestCorner(board.valid_moves(self.color))

  def generateTree(self, board, root):
    if root.depth >= self.MAX_DEPTH:
      self.heuristic(board)
      return

    #Save current player color and switch to generate opponent moves
    current = self.color
    self.color = board._opponent(self.color)

    previousMove = [0,0]
    for move in board.valid_moves(current):
      if move.x == previousMove[0] and move.y == previousMove[1]:
        continue
      node = PlayNode(name="%s_X:%d_Y:%d" % (current, move.x, move.y), color="", move=move, parent=root)
      previousMove[0] = move.x
      previousMove[1] = move.y
      clone = board.get_clone()
      clone.play(move, current)
      self.generateTree(clone, node)

    #After generating opponent moves, return original color
    self.color = board._opponent(self.color)

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
    my_tiles = len(board.valid_moves(my_color))
    opp_tiles = len(board.valid_moves(opp_color))
    if my_tiles > opp_tiles:
      m = (100.0 * my_tiles)/(my_tiles + opp_tiles)
    elif my_tiles < opp_tiles:
      m = -(100.0 * opp_tiles)/(my_tiles + opp_tiles)
    else:
      m = 0

    score = (10 * p) + (801.724 * c) + (382.026 * l) + (78.922 * m)
    return score

  