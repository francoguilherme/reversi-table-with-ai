from anytree import RenderTree
from models.playNode import PlayNode
from models.move import Move

class BestPlayer:
  MAX_DEPTH = 3

  def __init__(self, color):
    self.color = color

  def play(self, board):
    import time

    root = PlayNode(name="root", color="")

    start_time = time.time()
    self.generateTree(board, root)
    elapsed_time = time.time() - start_time

    #for pre, fill, node in RenderTree(root):
      #print "%s%s" % (pre, node.name)

    print "Time of execution:", elapsed_time

    return self.getNearestCorner(board.valid_moves(self.color))

  def generateTree(self, board, root):
    if root.depth >= self.MAX_DEPTH:
      return

    moves = [Move(-1,-1)] * len(board.valid_moves(self.color))
    nodes = [PlayNode(name="", color="") for move in xrange(len(moves))]

    #Save current player color and switch to generate opponent moves
    current = self.color
    self.color = board._opponent(self.color)

    for i in range(len(board.valid_moves(current))):
      moves[i] = board.valid_moves(current)[i]
      nodes[i].name = "%s_X:%d_Y:%d" % (current, moves[i].x, moves[i].y)
      nodes[i].parent = root
      clone = board.get_clone()
      clone.play(moves[i], current)
      self.generateTree(clone, nodes[i])

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

  def heuristica(board):
    my_tiles = 0, opp_tiles = 0, my_front_tiles = 0, opp_front_tiles = 0
    x = 0, y = 0
    p = 0.0, c = 0.0, l = 0.0, m = 0.0, f = 0.0, d = 0.0

    X1 = {-1, -1, 0, 1, 1, 1, 0, -1};
	  Y1 = {0, 1, 1, 1, 0, -1, -1, -1};

    V = [
      {20, -3, 11, 8, 8, 11, -3, 20},
      {-3, -7, -4, 1, 1, -4, -7, -3},
      {11, -4, 2, 2, 2, 2, -4, 11},
      {8, 1, 2, -3, -3, 2, 1, 8},
      {8, 1, 2, -3, -3, 2, 1, 8},
      {11, -4, 2, 2, 2, 2, -4, 11},
      {-3, -7, -4, 1, 1, -4, -7, -3},
      {20, -3, 11, 8, 8, 11, -3, 20}
    ]

    for i in range(0,8):
      for j in range(0,8):
        if board[i][j] == self.color:
          d = d + V[i][j]
          my_tiles += 1
        elif board[i][j] == _opponent.color:
          d = d - V[i][j]
          opp_tiles += 1
        if board[i][j] != 'vazio':
          for k in range(0,8):
            x = i + X1[k]
            y = j + Y1[k]
            if x>= 0 and x < 8 and y >=0 and y < 8 and grid[x][y] == 'vazio':
              if board[i][j] == self.color:
                my_front_tiles += 1
              else:
                opp_front_tiles += 1
              break
    if my_tiles > opp_tiles:
      p = (100.0 * my_tiles)/(my_tiles + opp_tiles)
    elif my_tiles < opp_tiles:
      p = -(100.0 * opp_tiles)/(my_tiles + opp_tiles)
    else:
      p = 0

    if my_front_tiles > opp_front_tiles:
      f = -(100.0 * my_front_tiles)/(my_front_tiles + opp_front_tiles)
    elif my_front_tiles < opp_front_tiles:
      f = (100.0 * opp_front_tiles)/(my_front_tiles + opp_front_tiles)
    else:
      f = 0

    #quinas ocupadas
    my_tiles = 0, opp_tiles = 0
    if board[0][0] == self.color:
      my_tiles += 1
    elif board[0][0] == _opponent.color:
      opp_tiles += 1
    if board[0][7] == self.color:
      my_tiles += 1
    elif board[0][7] == _opponent.color:
      opp_tiles += 1
    if board[7][0] == self.color:
      my_tiles += 1
    elif board[7][0] == _opponent.color:
      opp_tiles += 1
    if board[7][7] == self.color:
      my_tiles += 1
    elif board[7][7] == _opponent.color:
      opp_tiles += 1
    c = 25 * (my_tiles - opp_tiles)

    #proximidade das quinas
    my_tiles = 0, opp_tiles = 0
    if board[0][0] == 'vazio':
      if board[0][1] == self.color:
        my_tiles += 1
      elif board[0][1] == _opponent.color:
        opp_tiles += 1
      if board[1][1] == self.color:
        my_tiles += 1
      elif board[1][1] == _opponent.color:
        opp_tiles += 1
      if board[1][0] == self.color:
        my_tiles += 1
      elif board[1][0] == _opponent.color:
        opp_tiles += 1

    if board[0][7] == 'vazio':
      if board[0][6] == self.color:
        my_tiles += 1
      elif board[0][6] == _opponent.color:
        opp_tiles += 1
      if board[1][6] == self.color:
        my_tiles += 1
      elif board[1][6] == _opponent.color:
        opp_tiles += 1
      if board[1][7] == self.color:
        my_tiles += 1
      elif board[1][7] == _opponent.color:
        opp_tiles += 1

    if board[7][0] == 'vazio':
      if board[7][1] == self.color:
        my_tiles += 1
      elif board[7][1] == _opponent.color:
        opp_tiles += 1
      if board[6][1] == self.color:
        my_tiles += 1
      elif board[6][1] == _opponent.color:
        opp_tiles += 1
      if board[6][0] == self.color:
        my_tiles += 1
      elif board[6][0] == _opponent.color:
        opp_tiles += 1

    if board[7][7] == 'vazio':
      if board[6][7] == self.color:
        my_tiles += 1
      elif board[6][7] == _opponent.color:
        opp_tiles += 1
      if board[6][6] == self.color:
        my_tiles += 1
      elif board[6][6] == _opponent.color:
        opp_tiles += 1
      if board[7][6] == self.color:
        my_tiles += 1
      elif board[7][6] == _opponent.color:
        opp_tiles += 1
    l = -12.5 * (my_tiles - opp_tiles)

    #mobilidade
    my_tiles = board.valid_moves(self.color)
    opp_tiles = board.valid_moves(_opponent.color)
    if my_tiles > opp_tiles:
      m = (100.0 * my_tiles)/(my_tiles + opp_tiles)
    elif my_tiles < opp_tiles:
      m = -(100.0 * opp_tiles)/(my_tiles + opp_tiles)
    else:
      m = 0

  score = (10*p) + (801.724 * c) + (382.026 * l) + (78.922 * m) + (74.396 * f) + (10 * d)
  return score