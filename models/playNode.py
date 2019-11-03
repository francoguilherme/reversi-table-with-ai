from anytree import Node, NodeMixin, AnyNode
import operator

class PlayNode(AnyNode, NodeMixin):  # Add Node feature
  def __init__(self, name=None, color=None, move=None, board=None, value=None, parent=None, children=None):
    super(AnyNode, self).__init__()
    self.name = name
    self.color = color
    self.move = move
    self.board = board
    self.value = value
    self.parent = parent
    if children:
      self.children = children