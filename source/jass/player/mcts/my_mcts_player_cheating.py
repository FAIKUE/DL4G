from jass.base.const import*
from jass.base.player_round_cheating import PlayerRoundCheating
from jass.base.round_factory import get_round_from_player_round
from jass.player.player_cheating import PlayerCheating
from jass.base.rule_schieber import RuleSchieber
from jass.player.mcts.const import Status
from jass.player.mcts.node import Node
from jass.player.mcts.tree import Tree
from jass.player.mcts.UCB import UCB
from jass.player.random_player_schieber import RandomPlayerSchieber
from jass.player.mcts.sampler import Sampler

import time
import random

class MyMCTSPlayerCheating(PlayerCheating):
    """
    Implementation of a player to play Jass using Monte Carlo Tree Search.
    """
    def select_trump(self, rnd: PlayerRoundCheating) -> int:
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

    def play_card(self, rnd: PlayerRoundCheating) -> int:
        """
        Player returns a card to play based on the given round information.

        Args:
            rnd: current round

        Returns:
            card to play, int encoded
        """
        #Create Simulation stuff
        #simRound = get_round_from_player_round(rnd, rnd.hands)
        print(rnd.hands)
        bestcard = self.montecarlotreesearch(rnd)

        return bestcard

    def montecarlotreesearch(self, rnd: PlayerRoundCheating):
        tree = Tree()
        rootNode = tree.get_root_node()
        rootNode.getAction().setPlayerNr(rnd.player)
        rootNode.getAction().setRound(rnd)

        think_for_seconds = 5
        endtime = time.time() + think_for_seconds
        simulated_rounds = 0
        while time.time() < endtime:
            simulated_rounds += 1
            promisingNode = self.selectPromisingNode(rootNode)
            if promisingNode.getAction().getRound().nr_cards_in_trick < 4:
                self.expandNode(promisingNode, rnd)

            nodeToExplore = promisingNode
            if len(promisingNode.getChilds()) > 0:
                nodeToExplore = promisingNode.getRandomChild()

            winScore = self.simulateRound(nodeToExplore)
            self.backPropagation(nodeToExplore, rnd.player, winScore)
        winner = rootNode.getChildWithMaxVisitCount().getAction().getCard()
        print(f"{simulated_rounds} rounds simulated in {think_for_seconds} seconds\n")
        return winner

    def selectPromisingNode(self, rootNode: Node)->Node:
        node = rootNode
        while len(node.getChilds()) != 0:
            ucb = UCB()
            node = ucb.find_best_node_ucb(node)
        return node


    def expandNode(self, node:Node, rnd: PlayerRoundCheating):
        validCards = np.flatnonzero(rnd.get_valid_cards())
        for card in validCards:
            new_node = Node()
            new_node.setParent(node)
            new_node.getAction().setRound(rnd)
            new_node.getAction().setPlayerNr(node.getAction().getRound().player)
            new_node.getAction().setCard(card)
            node.addChild(new_node)

    def simulateRound(self, node: Node):
        # other_player_cards = np.ones(36, int)
        # tricks = node.getAction().getRound().tricks.flatten()
        # other_player_cards[tricks] = 0
        # my_hand = node.getAction().getRound().hand
        # other_player_cards = np.ma.masked_where(my_hand == 1, other_player_cards).filled(0)
        # print(f"my hand:\n{my_hand}")
        # print(f"other player cards:\n{other_player_cards}")
        # other_player_cards = convert_one_hot_encoded_cards_to_int_encoded_list(other_player_cards)
        # other_player_cards = np.split(np.array(other_player_cards), 3)
        # hands = np.zeros(27, np.int32)
        # hands[other_player_cards] = 1
        # random.shuffle(hands)
        # hands = hands.reshape((9, 3))

        rnd = get_round_from_player_round(node.getAction().getRound(), node.getAction().getRound().hands)
        rnd.action_play_card(node.getAction().getCard())
        cards = rnd.nr_played_cards
        randomPlayer = RandomPlayerSchieber()
        while cards < 36:
            player_rnd = PlayerRoundCheating()
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
