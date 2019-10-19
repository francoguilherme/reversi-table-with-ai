#pip install anytree
from anytree import Node, RenderTree, NodeMixin, AnyNode
import operator
from controllers.board_controller import BoardController
from models.move                  import Move
from models.board                 import Board

controller = BoardController()
controller.init_game()