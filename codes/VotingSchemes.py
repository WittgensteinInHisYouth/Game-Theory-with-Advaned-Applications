import numpy as np
from collections import Counter
from copy import deepcopy


class VotingScheme(object):
    def __init__(self, rankings):

        assert isinstance(rankings, dict)

        self.rankings = rankings
        self.ranking_mat = []
        for key, val in rankings.items():
            for _ in range(val):
                self.ranking_mat.append(list(key))
        self.ranking_mat = np.array(self.ranking_mat)
        self.num_sample, self.num_outcomes = self.ranking_mat.shape

    def plurality(self, num_top_candiates = None):
        """

        pick the outcome which is most-preferred by the most people

        """

        counter = Counter(self.ranking_mat[:, 0])
        return counter.most_common(num_top_candiates)

    def pluralityWithElimination(self, verbose=False):
        """

        Plurality with elimination (“instant runoff”, “transferable
        voting”)
        * if some outcome has a majority, it is the winner
        * otherwise, the outcome with the fewest votes is eliminated (may
        * need some tie-breaking procedure)
        * repeat until there is a winner.

        """

        counter = Counter(self.ranking_mat[:, 0])
        ranking_mat = deepcopy(self.ranking_mat)

        while not self._existMajorityQ(counter):
            counter_ls = counter.most_common()
            (loser, loser_count) = min(counter_ls, key=lambda x: x[1])

            num_samples, num_outcomes = ranking_mat.shape
            # flatten the matrix into a list, pop the loser out, and reshape into the matrix
            mat_flattened = ranking_mat.flatten().tolist()
            mat_flattened = [outcome for outcome in mat_flattened if outcome != loser]
            ranking_mat = np.array(mat_flattened).reshape((num_samples, -1))
            # ranking_dict = self._rankingMat2Dict(ranking_mat[:, 0])
            counter = Counter(ranking_mat[:, 0])
            
            if verbose:
                print('###########')
                print('Loser: ', loser)
                print('After elemiantions, counter is', counter)
                input()


        return self._existMajorityQ(counter)

    def _rankingMat2Dict(self, ranking_mat):

        dictionary = {}
        for occurence in ranking_mat:
            occurence = tuple(occurence)
            if occurence in dictionary:
                dictionary[occurence] += 1
            else:
                dictionary[occurence] = 1

        return dictionary

    def _existMajorityQ(self, count_ls):

        candiates, counts = zip(*count_ls.most_common())
        counts = np.array(counts) # enable element-wise comparison

        if any(counts > sum(counts)*0.5):
            return candiates[np.argmax(counts)]
        else:
            return False

def main():

    votes = {
        ('A', 'B', 'D', 'C'): 400,
        ('D', 'C', 'B', 'A'): 300,
        ('B', 'D', 'C', 'A'): 200,
        ('C', 'A', 'B', 'D'): 100,
        ('C', 'D', 'A', 'B'): 2
    }
    # votes = {
    #     ('A', 'B', 'C'): 499,
    #     ('B', 'C', 'A'): 3,
    #     ('C', 'B', 'A'): 498
    # }
    voteSystem = VotingScheme(votes)
    res = voteSystem.plurality()
    # res = voteSystem.pluralityWithElimination(verbose=False)
    print(res)

if __name__ == '__main__':
    main()
