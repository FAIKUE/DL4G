from jass.base.const import *
from jass.base.player_round import PlayerRound
from jass.base.round_factory import get_round_from_player_round
from jass.player.player import Player
from jass.base.rule_schieber import RuleSchieber

from jass.player.mcts.const import Status
from jass.player.mcts.node import Node
from jass.player.mcts.tree import Tree
from jass.player.mcts.UCB import UCB
from jass.player.random_player_schieber import RandomPlayerSchieber
from jass.player.mcts.sampler import Sampler

import time


class MyMCTSPlayer(Player):
    """
    Implementation of a player to play Jass using Monte Carlo Tree Search.
    """

    def select_trump(self, rnd: PlayerRound) -> int:
        """
        Player chooses a trump based on the given round information.

        Args:
            rnd: current round

        Returns:
            selected trump
        """
        # select the trump with the largest number of cards
        trump = 0
        max_number_in_color = 0
        for c in range(4):
            number_in_color = (rnd.hand * color_masks[c]).sum()
            if number_in_color > max_number_in_color:
                max_number_in_color = number_in_color
                trump = c
        return trump

    def play_card(self, rnd: PlayerRound) -> int:
        """
        Player returns a card to play based on the given round information.

        Args:
            rnd: current round

        Returns:
            card to play, int encoded
        """
        # Create Simulation stuff
        # simRound = get_round_from_player_round(rnd, rnd.hands)
        bestcard = self.monte_carlo_tree_search(rnd)

        return bestcard

    def monte_carlo_tree_search(self, rnd: PlayerRound):
        sampled_round = Sampler.sample(rnd)
        tree = Tree()
        root_node = tree.get_root_node()
        root_node.getAction().setPlayerNr(rnd.player)
        root_node.getAction().setRound(sampled_round)

        think_for_seconds = 2
        endtime = time.time() + think_for_seconds
        simulated_rounds = 0
        while time.time() < endtime:
            simulated_rounds += 1
            promisingNode = self.selectPromisingNode(root_node)
            if promisingNode.getAction().getRound().nr_cards_in_trick < 4:
                self.expandNode(promisingNode, sampled_round)

            nodeToExplore = promisingNode
            if len(promisingNode.getChilds()) > 0:
                nodeToExplore = promisingNode.getRandomChild()

            winScore = self.simulateRound(nodeToExplore)
            self.backPropagation(nodeToExplore, sampled_round.player, winScore)
        winner = root_node.getChildWithMaxVisitCount().getAction().getCard()
        print(f"{simulated_rounds} rounds simulated in {think_for_seconds} seconds")
        return winner

    def selectPromisingNode(self, rootNode: Node) -> Node:
        node = rootNode
        while len(node.getChilds()) != 0:
            ucb = UCB()
            node = ucb.find_best_node_ucb(node)
        return node

    def expandNode(self, node: Node, rnd: PlayerRound):
        validCards = np.flatnonzero(rnd.get_valid_cards())
        for card in validCards:
            new_node = Node()
            new_node.setParent(node)
            new_node.getAction().setRound(rnd)
            new_node.getAction().setPlayerNr(node.getAction().getRound().player)
            new_node.getAction().setCard(card)
            node.addChild(new_node)

    def simulateRound(self, node: Node):
        rnd = get_round_from_player_round(node.getAction().getRound(), node.getAction().getRound().hands)
        rnd.action_play_card(node.getAction().getCard())
        cards = rnd.nr_played_cards
        randomPlayer = RandomPlayerSchieber()
        while cards < 36:
            player_rnd = PlayerRound()
            player_rnd.set_from_round(rnd)
            card_action = randomPlayer.play_card(player_rnd)
            rnd.action_play_card(card_action)
            cards += 1

        myPoints = rnd.points_team_0
        pointsEnemy = rnd.points_team_1
        maxPoints = myPoints + pointsEnemy

        if myPoints > pointsEnemy:
            return (myPoints - 0) / (maxPoints - 0)
        else:
            return 0

    def backPropagation(self, node: Node, playerNr: int, winScore: int):
        tempNode = node
        while tempNode != None:
            tempNode.getAction().incrementVisit()
            if tempNode.getAction().getPlayerNr() == playerNr:
                tempNode.getAction().setWinScore(winScore)
            tempNode = tempNode.getParent()
