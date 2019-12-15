from source.jass.base.const import *
from source.jass.base.player_round import PlayerRound
from source.jass.base.round_factory import get_round_from_player_round
from source.jass.player.mcts.sampler import Sampler
from source.jass.player.mcts.tree import Tree
from source.jass.player.mcts.node import Node
from source.jass.player.random_player_schieber import RandomPlayerSchieber
from source.jass.player.mcts.UCB import UCB
from multiprocessing.pool import ThreadPool

import time


class MonteCarloTreeSearch:
    @staticmethod
    def monte_carlo_tree_search(rnd: PlayerRound):
        sampled_round = Sampler.sample(rnd)
        tree = Tree()
        root_node = tree.get_root_node()
        root_node.getAction().setPlayerNr(rnd.player)
        root_node.getAction().setRound(sampled_round)

        think_for_seconds = 9
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
        winner = root_node.getChildWithMaxVisitCount().getAction()
        print(f"{simulated_rounds} rounds simulated in {think_for_seconds} seconds")
        print(f"winner: {winner.getCard()} with visit count {winner.getVisitCount()} ({round(winner.getVisitCount()/simulated_rounds, 3)}), valid cards: {np.flatnonzero(sampled_round.get_valid_cards())}")
        return winner.getCard()

    @staticmethod
    def monte_carlo_tree_search_multisample(rnd: PlayerRound):
        think_for_seconds = 9
        endtime = time.time() + think_for_seconds
        best_visit_count = 0
        best_winner = None
        best_winner_score = 0
        sampled_rounds = 0
        simulated_rounds_total = 0
        simulated_rounds = 0

        while time.time() < endtime:
            sampled_rounds += 1
            sampled_round = Sampler.sample(rnd)
            tree = Tree()
            root_node = tree.get_root_node()
            root_node.getAction().setPlayerNr(rnd.player)
            root_node.getAction().setRound(sampled_round)

            simulated_rounds_total += simulated_rounds
            simulated_rounds = 0
            start_time = time.time()
            while (time.time() - start_time) < think_for_seconds / 8:
                simulated_rounds += 1
                promisingNode = MonteCarloTreeSearch.selectPromisingNode(root_node)
                if promisingNode.getAction().getRound().nr_cards_in_trick < 4:
                    MonteCarloTreeSearch.expandNode(promisingNode, sampled_round)

                nodeToExplore = promisingNode
                if len(promisingNode.getChilds()) > 0:
                    nodeToExplore = promisingNode.getRandomChild()

                winScore = MonteCarloTreeSearch.simulateRound(nodeToExplore)
                MonteCarloTreeSearch.backPropagation(nodeToExplore, sampled_round.player, winScore)
            winner = root_node.getChildWithMaxVisitCount()
            print(
                f"winner of sampled round: {winner.getAction().getCard()} with score {round(winner.getAction().getVisitCount() / simulated_rounds, 3)} and ")
            if winner.getAction().getVisitCount() > best_visit_count:
                best_visit_count = winner.getAction().getVisitCount()
                best_winner = winner.getAction().getCard()
                best_winner_score = round(best_visit_count / simulated_rounds, 3)

        print(
            f"sampled {sampled_rounds} times and simulated {simulated_rounds_total} rounds in {think_for_seconds} seconds")
        print(
            f"winner: {best_winner} with score {best_visit_count} ({best_winner_score}), valid cards: {np.flatnonzero(rnd.get_valid_cards())}")
        return best_winner

    @staticmethod
    def monte_carlo_tree_search_multisample_threading(rnd: PlayerRound):
        think_for_seconds = 5
        sample_count = 2
        start_time = time.time()
        best_visit_count = 0
        best_winner = None
        simulated_rounds = 0

        pools = []
        results = []

        for i in range(0, sample_count):
            pool = ThreadPool(processes=1)
            result = pool.apply_async(MonteCarloTreeSearch.playsampledRound, (rnd, think_for_seconds))
            pools.append(pool)
            results.append(result)

        time.sleep(think_for_seconds)

        for i in range(0, sample_count):
            result = results[i].get()
            simulated_rounds += result[1]
            if result[0].getAction().getVisitCount() > best_visit_count:
                best_visit_count = result[0].getAction().getVisitCount()
                best_winner = result[0].getAction()

        duration = time.time() - start_time
        print(f"winner: {best_winner.getCard()}, valid cards: {np.flatnonzero(rnd.get_valid_cards())}, ran for {round(duration, 3)}, simulated {simulated_rounds} rounds")

        #print(f"sampled {sampled_rounds} times and simulated {simulated_rounds_total} rounds in {think_for_seconds} seconds")
        #print(f"winner: {best_winner.getCard()} with visit ratio {best_winner_score} and win score {best_winner.getWinScore()}, valid cards: {np.flatnonzero(rnd.get_valid_cards())}")
        return best_winner.getCard()

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

    @staticmethod
    def playsampledRound(rnd: PlayerRound, think_for_seconds):
        sampled_round = Sampler.sample(rnd)
        tree = Tree()
        root_node = tree.get_root_node()
        root_node.getAction().setPlayerNr(rnd.player)
        root_node.getAction().setRound(sampled_round)

        simulated_rounds = 0
        start_time = time.time()
        while (time.time() - start_time) < think_for_seconds:
            simulated_rounds += 1
            promisingNode = MonteCarloTreeSearch.selectPromisingNode(root_node)
            if promisingNode.getAction().getRound().nr_cards_in_trick < 4:
                MonteCarloTreeSearch.expandNode(promisingNode, sampled_round)

            nodeToExplore = promisingNode
            if len(promisingNode.getChilds()) > 0:
                nodeToExplore = promisingNode.getRandomChild()

            winScore = MonteCarloTreeSearch.simulateRound(nodeToExplore)
            MonteCarloTreeSearch.backPropagation(nodeToExplore, sampled_round.player, winScore)
        winner = root_node.getChildWithMaxVisitCount()
        print(f"\nwinner of sampled round: {winner.getAction().getCard()} with visit ratio {round(winner.getAction().getVisitCount() / simulated_rounds, 3)} and win score {winner.getAction().getWinScore()}")
        return winner, simulated_rounds