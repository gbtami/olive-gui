#
import sys
import os
import pickle

from .. import model


class Node:

    def __init__(self):
        self.depth = 0
        self.childIsThreat = False
        self.comments = []

    def setv(self, k, v):
        setattr(self, k, v)
        return self

    def unflatten(self, nodes, offset):

        self.children = []

        while offset < nodes.length:

            # case 1: nodes[offset] is a direct child of this --> add to
            # children and recurse
            if (self.depth + 1 == nodes[offset].depth):
                self.children.push(nodes[offset])
                offset = nodes[offset].unflatten(nodes, offset + 1)

            # case 2: nodes[offset] is a grand-child of this --> create
            # intermediate null-nodes
            elif self.depth + 1 < nodes[offset].depth:
                nn = NullNode(self.depth + 1, self.childIsThreat)
                self.children.append(nn)
                offset = nn.unflatten(nodes, offset)

            # case 3: nodes[offset] is not a child of this
            else:
                return offset

    def linkContinuedTwins(self):
        for i in xrange(1, len(self.children)):
            if self.children[i].isContinued:
                self.children[i].anticipator = self.children[i - 1]

    def make(self, board):
        board.flip()

    def unmake(self, board):
        board.flip()


class NullNode(Node):

    def __init__(self, depth, isThreat):
        super(NullNode, self).__init__()
        self.depth = depth
        self.isThreat = isThreat


class TwinNode(Node):

    def __init__(self, twinId, isContinued):
        super(TwinNode, self).__init__()
        self.depth = 1

        self.twinId = twinId
        self.isContinued = isContinued
        self.anticipator = None
        self.commands = []

    def make(self, board):

        self.oldBoard = pickle.dumps(board)

        board.flip()

        if not self.anticipator is None:
            self.anticipator.make(board)

        for command in self.commands:
            command.execute(board)

    def unmake(self, board):
        board = pickle.loads(self.oldBoard)


class VirtualTwinNode(TwinNode):

    def __init__(self):
        super(VirtualTwinNode, self).__init__()


class TwinCommand:

    def __init__(self, name, args):
        self.name = name
        self.args = args

    def execute(self, b):
        if 'Move' == self.name:
            b.move(self.args[0], self.args[1])
        elif 'Exchange' == self.name:
            b.board[
                self.args[0]], b.board[
                self.args[1]] = b.board[
                self.args[1]], b.board[
                self.args[0]]
        elif 'Remove' == self.name:
            b.drop(self.args[0])
        elif 'Add' == self.name:
            b.add(self.args[0], self.args[1])
        elif 'Rotate' == self.name:
            b.rotate(self.args[0])
        elif 'Mirror' == self.name:
            b.mirror(self.args[0], self.args[1])
        elif 'Shift' == self.name:
            b.shift(self.args[0], self.args[1])
        elif 'PolishType' == self.name:
            b.polishTwin()
        elif 'Imitator' == self.name:
            b.imitators = self.args
