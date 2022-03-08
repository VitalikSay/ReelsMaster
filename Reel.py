import numpy as np

class Reel():
    def __init__(self, ind):
        self.symbols = []
        self.weights = []
        self.ln = 0
        self.number_of_stacks = 0
        self.index = ind


    def SetSymbols(self, symbols):
        self.symbols = symbols
        self.ln = len(self.symbols)
        self.weights = [1 for _ in range(self.ln)]


    def MakeReelofCommonSymbols(self, common_symbols, window_height):
        not_shuffled_reel = self._CreateNotShuffledReelWithoutSpSymbols(common_symbols)
        shuffled_reel = self._RandomShuffle(not_shuffled_reel)
        need_change_reel = False

        for i in range(self.number_of_stacks):
            current_symbol = shuffled_reel[i][1]
            left_neighbors = self._LeftNeighbors(shuffled_reel, i, window_height)
            right_neighbors = self._RightNeighbors(shuffled_reel, i, window_height)

            if (current_symbol in left_neighbors) or (current_symbol in right_neighbors):
                need_change = True
                for j in range(self.number_of_stacks):
                    inside_cur_symbol = shuffled_reel[j][1]
                    inside_left_neighbors = self._LeftNeighbors(shuffled_reel, j, window_height)
                    inside_right_neighbors = self._RightNeighbors(shuffled_reel, j, window_height)
                    if (current_symbol not in inside_left_neighbors) and (current_symbol not in inside_right_neighbors) \
                            and (inside_cur_symbol not in left_neighbors) and (inside_cur_symbol not in right_neighbors):
                        temp = shuffled_reel[i]
                        shuffled_reel[i] = shuffled_reel[j]
                        shuffled_reel[j] = temp
                        need_change = False
                        break
                if need_change:
                    need_change_reel = True
                    break
        if need_change_reel:
            shuffled_reel = self.MakeReelofCommonSymbols(common_symbols, window_height)
        return shuffled_reel


    def InsertSpecialSymbols(self, ready_reel, special_symbols, dist_bet_sp_symbols):
        sp_symbols = []
        indexes_between_huge_stacks = []
        for i, stack in ready_reel[:-dist_bet_sp_symbols]:
            if (stack[0] > 1) and (ready_reel[(i+1) % self.number_of_stacks][0] > 1):
                if not indexes_between_huge_stacks:
                    indexes_between_huge_stacks.append(i + 1)
                    continue
                dist_bt_indexes = 0
                for st in ready_reel(indexes_between_huge_stacks[-1], i+1):
                    dist_bt_indexes += st[0]
                if dist_bt_indexes >= dist_bet_sp_symbols:
                    indexes_between_huge_stacks.append(i+1)

        sp_symbols_list = []
        for symbol, stacks in special_symbols.items():
            sp_symbols.append(symbol)
            for stack in stacks:
                for i in range(stack[0]):
                    sp_symbols_list.append([stack[1], symbol])


        ## Работает ли эта тема правильно большой вопрос
        while len(sp_symbols_list) != 0 and len(indexes_between_huge_stacks) != 0:
            inserted_indexes = []
            rand_sp_stack_index = np.random.choice(*range(sp_symbols_list))
            del sp_symbols_list[rand_sp_stack_index]
            rand_place_index = np.random.choice(*range(indexes_between_huge_stacks))
            inserted_indexes.append(indexes_between_huge_stacks[rand_place_index])
            ready_reel.insert(indexes_between_huge_stacks[rand_place_index]
                              + sum([ind for ind in inserted_indexes if ind < indexes_between_huge_stacks[rand_place_index]]),
                              sp_symbols_list[rand_sp_stack_index])
            del indexes_between_huge_stacks[rand_place_index]


        if len(sp_symbols_list) == 0:
            return ready_reel

        for i, stack in ready_reel:






    def MakeWeights(self, weight_patterns, weight_percentage):
        pass


    def PrintReel(self):
        pass


    def _CreateNotShuffledReelWithoutSpSymbols(self, common_symbols):
        self.ln = 0
        self.number_of_stacks = 0
        not_shuffled_reel = []
        for symbol, stacks in common_symbols.items():
            for stack in stacks:
                self.ln += stack[0] * stack[1]
                self.number_of_stacks += stack[0]
                for number_of_stacks in range(stack[0]):
                    not_shuffled_reel.append([stack[1], symbol])
        return not_shuffled_reel


    def _RandomShuffle(self, not_shuffled_reel):
        indexes = [*range(len(not_shuffled_reel))]
        shuffled_reel = []
        for i in range(len(not_shuffled_reel)):
            rand_index = np.random.choice(indexes)
            del indexes[indexes.index(rand_index)]
            shuffled_reel.append(not_shuffled_reel[rand_index])
        return shuffled_reel


    def _LeftNeighbors(self, reel, stack_index, window_height):
        left_neighbors = []
        while len(left_neighbors) != (window_height - 1):
            left_stack = reel[stack_index - 1]
            for i in range(left_stack[0]):
                left_neighbors.insert(0, left_stack[1])
                if len(left_neighbors) == (window_height - 1):
                    break
            stack_index -= 1
        return left_neighbors


    def _RightNeighbors(self, reel, stack_index, window_height):
        right_neighbors = []
        while len(right_neighbors) != (window_height - 1):
            right_stack = reel[(stack_index + 1) % self.number_of_stacks]
            for i in range(right_stack[0]):
                right_neighbors.append(right_stack[1])
                if len(right_neighbors) == (window_height - 1):
                    break
            stack_index += 1
        return right_neighbors


r = Reel(0)
d = {}
d[0] = [[5,1], [2,2], [1,3]]
d[1] = [[5,1], [2,2], [1,3]]
d[2] = [[5,1], [2,2], [1,3]]
d[3] = [[5,1], [2,2], [1,3]]
d[4] = [[5,1], [2,2], [1,3]]
d[5] = [[5,1], [2,2], [1,3]]
#d[6] = [[5,1], [2,2], [1,3]]

print(r.MakeReelofCommonSymbols(d, 5))
print(r.ln)
print(r.number_of_stacks)

