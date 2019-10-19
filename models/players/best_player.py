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

    for pre, fill, node in RenderTree(root):
      print "%s%s" % (pre, node.name)

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
