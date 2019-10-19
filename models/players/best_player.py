class BestPlayer:
  def __init__(self, color):
    self.color = color

  def play(self, board):
    for move in board.valid_moves(self.color):
      print "Move X:", move.x, "Y:", move.y
      clone = board.get_clone()
      clone.play(move, self.color)
      for opmove in clone.valid_moves(board._opponent(self.color)):
        print "Opponent Move X:", opmove.x, "Y:", opmove.y

    return self.getNearestCorner(board.valid_moves(self.color))

  def generateTree(self, board, depth):
      for i in range(depth):
        clone = board.get_clone()

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
