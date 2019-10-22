from jass.base.const import *
from jass.base.player_round import PlayerRound
from jass.base.round_factory import get_round_from_player_round
from jass.player.mcts.sampler import Sampler
from jass.player.mcts.tree import Tree
from jass.player.mcts.node import Node
from jass.player.random_player_schieber import RandomPlayerSchieber
from jass.player.mcts.UCB import UCB

import time


class MonteCarloTreeSearch:
    @staticmethod
    def monte_carlo_tree_search(rnd: PlayerRound):
        sampled_round = Sampler.sample(rnd)
        tree = Tree()
        root_node = tree.get_root_node()
        root_node.getAction().setPlayerNr(rnd.player)
        root_node.getAction().setRound(sampled_round)

        think_for_seconds = 1
        endtime = time.time() + think_for_seconds
        simulated_rounds = 0
        while time.time() < endtime:
            simulated_rounds += 1
            promisingNode = MonteCarloTreeSearch.selectPromisingNode(root_node)
            if promisingNode.getAction().getRound().nr_cards_in_trick < 4:
                MonteCarloTreeSearch.expandNode(promisingNode, sampled_round)

            nodeToExplore = promisingNode
            if len(promisingNode.getChilds()) > 0:
                nodeToExplore = promisingNode.getRandomChild()

            winScore = MonteCarloTreeSearch.simulateRound(nodeToExplore)
            MonteCarloTreeSearch.backPropagation(nodeToExplore, sampled_round.player, winScore)
        winner = root_node.getChildWithMaxVisitCount().getAction().getCard()
        print(f"{simulated_rounds} rounds simulated in {think_for_seconds} seconds")
        return winner

    @staticmethod
    def selectPromisingNode(rootNode: Node) -> Node:
        node = rootNode
        while len(node.getChilds()) != 0:
            ucb = UCB()
            node = ucb.find_best_node_ucb(node)
        return node

    @staticmethod
    def expandNode(node: Node, rnd: PlayerRound):
        validCards = np.flatnonzero(rnd.get_valid_cards())
        for card in validCards:
            new_node = Node()
            new_node.setParent(node)
            new_node.getAction().setRound(rnd)
            new_node.getAction().setPlayerNr(node.getAction().getRound().player)
            new_node.getAction().setCard(card)
            node.addChild(new_node)

    @staticmethod
    def simulateRound(node: Node):
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

    @staticmethod
    def backPropagation(node: Node, playerNr: int, winScore: int):
        tempNode = node
        while tempNode != None:
            tempNode.getAction().incrementVisit()
            if tempNode.getAction().getPlayerNr() == playerNr:
                tempNode.getAction().setWinScore(winScore)
            tempNode = tempNode.getParent()
