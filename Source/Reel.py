import numpy as np
from collections import defaultdict


class Reel():
    def __init__(self, ind):
        self.symbols = []
        self.symbol_in_stacks = []
        self.weights = []
        self.ln = 0
        self.number_of_stacks = 0
        self.index = ind
        self._pattern_counter = defaultdict(int)
        self._pattern_indexes = defaultdict(list)
        self._weight_to_input = 1000


    def SetSymbols(self, symbols):
        self.symbols = symbols
        self.ln = len(self.symbols)
        self.weights = [1 for _ in range(self.ln)]

    def SetWeights(self, weights):
        self.weights = weights
        if not self.symbols:
            print("\nSymbols for these weights are not set, symbols will be a list of ones")
            self.symbols = [1 for _ in range(len(weights))]
            self.ln = len(self.weights)


    def MakeReel(self, common_symbols, sp_symbols, dist_between_sp_symbols, window_height):
        ready_reel_without_sp_symbols = self._MakeReelofCommonSymbols(common_symbols, window_height)
        ready_reel_with_sp_symbols = self._InsertSpecialSymbols(ready_reel_without_sp_symbols,
                                                                sp_symbols,
                                                                dist_between_sp_symbols)
        for stack in ready_reel_with_sp_symbols:
            self.symbol_in_stacks.append(stack)
        self._UnpackSymbolStacks()


    def MakeWeights(self, weight_patterns, weight_percentage, window_height):
        self._FindPatternsInReels(weight_patterns, window_height)
        self._AddWeightForPatterns(weight_patterns, weight_percentage)
        self._PrintPatternInfo(weight_percentage)


    def PrintReel(self, start_symbol=''):
        printing_symbols = ''
        printing_symbols += '<Symbols>'
        for symbol in self.symbols:
            printing_symbols += str(symbol) + ','
        printing_symbols = printing_symbols[:-1]
        printing_symbols += '</Symbols>'

        printing_weights = ''
        printing_weights += '<Weights>'
        for weight in self.weights:
            printing_weights += str(weight) + ','
        printing_weights = printing_weights[:-1]
        printing_weights += '</Weights>'
        print(start_symbol + printing_symbols)
        print(start_symbol + printing_weights)


    def _PrintPatternInfo(self, weight_percentage):
        print("Reel", self.index, "pattern info: ")
        patterns_available = 0
        for i in range(-1, len(self._pattern_counter)-1):
            if self._pattern_counter[i] > 0:
                patterns_available += 1
            if i == -1:
                weigh_perc = 100 - sum(weight_percentage)
            else:
                weigh_perc = weight_percentage[i]
            print("\tNumber of Patterns", i, ":", self._pattern_counter[i], "(Weight", int(weigh_perc * self._weight_to_input / 100), ")")
        print("\tTotal input weight:", self._weight_to_input, " (", patterns_available, "of", len(self._pattern_counter), "patterns available)")


    def _PrintPattern(self, pattern):
        for i, row_pat in enumerate(pattern):
            print("Row ", i, ": ", row_pat, sep='')


    def _CheckWeightPatternsCounter(self):  # True - все ок, False - каие-то паттерны отсутствуют
        no_pattern_indexes = []
        for pattern_index, pattern_counter in self._pattern_counter:
            if pattern_counter == 0:
                no_pattern_indexes.append(pattern_index)
        print("In reel no such patterns:")


    def _FindPattern(self, window, patterns):
        pattern_bool_vector = [False for _ in range(len(patterns))]
        for i, pattern in enumerate(patterns):
            window_same_to_pattern = True
            for j, row_pattern in enumerate(pattern):
                if (window[j] in row_pattern) or row_pattern == [-1]:
                    continue
                else:
                    window_same_to_pattern = False
                    break
            if window_same_to_pattern:
                pattern_bool_vector[i] = True
        if sum(pattern_bool_vector) > 1:
            print("\nERROR: Same weight patterns in reel", self.index)
            return 0
        return pattern_bool_vector


    def _FindPatternsInReels(self, weight_patterns, window_height):
        for i, pattern in enumerate(weight_patterns):
            self._pattern_counter[i] = 0
        for i in range(len(self.symbols)):
            window = self.TakeWindow(i, window_height)
            weight_bool_pattern_vec = self._FindPattern(window, weight_patterns)
            if sum(weight_bool_pattern_vec) == 0:
                self._pattern_counter[-1] += 1  # Под ключем -1 находятся все окна не подходящие ни под один из паттернов
                self._pattern_indexes[-1].append(i)
            else:
                true_index = weight_bool_pattern_vec.index(True)
                self._pattern_counter[true_index] += 1
                self._pattern_indexes[true_index].append(i)


    def _CompareWeightsAndPatternCounter(self, weight_of_patterns):
        for i, weight in enumerate(weight_of_patterns):
            if weight < self._pattern_counter[i]:
                return False
        return True


    def _AddWeightForPatterns(self, weight_patterns, weight_percentage):
        if len(weight_percentage) != len(weight_patterns):
            print("\nERROR: Number of weight patterns not equal to number of weight percents in reel", self.index)
            return 0
        percents_sum = sum(weight_percentage)
        if percents_sum > 100 or percents_sum < 0:
            if percents_sum > 100:
                print("\nERROR: Sum of percents in reel", self.index, "more than 100")
            else:
                print("\nERROR: Sum of percents in reel", self.index, "less than 0")
            return 0

        percents_of_not_patterns = 100 - percents_sum
        self.weights = [0 for _ in range(self.ln)]

        weight_of_not_patterns = int(self._weight_to_input * percents_of_not_patterns / 100)
        weights_of_patterns = []
        for percent in weight_percentage:
            weights_of_patterns.append(percent * self._weight_to_input / 100)
        while (weight_of_not_patterns < self._pattern_counter[-1] and
               self._CompareWeightsAndPatternCounter(weights_of_patterns)):
            self._weight_to_input *= 10
            weight_of_not_patterns = int(self._weight_to_input * percents_of_not_patterns / 100)
            weights_of_patterns = []
            for percent in weight_percentage:
                weights_of_patterns.append(percent * self._weight_to_input / 100)

        while(weight_of_not_patterns > 0):
            if self._pattern_counter[-1] == 0:  # Если в риле нету подобных паттернов, то он просто пропускается
                break
            for window_index in self._pattern_indexes[-1]:
                self.weights[window_index] += 1
                weight_of_not_patterns -= 1
                if weight_of_not_patterns <= 0:
                    break

        for pattern_index, pattern_index_in_reel in self._pattern_indexes.items():
            if pattern_index == -1:  # Пропускаем не паттерны
                continue
            weight = weights_of_patterns[pattern_index]
            if self._pattern_counter[pattern_index] == 0:  # Если в риле нету подобных паттернов, то он просто пропускается
                continue
            while(weight > 0):
                for window_index in pattern_index_in_reel:
                    self.weights[window_index] += 1
                    weight -= 1
                    if weight <= 0:
                        break


    def TakeWindow(self,i, window_height):
        start_index = i
        end_index = i + window_height
        if i > self.ln:
            i %= self.ln
            end_index = i + window_height
        if end_index > self.ln:
            first_part = self.symbols[i:]
            second_part = self.symbols[:window_height - len(first_part)]
            return first_part + second_part
        else:
            return self.symbols[i:i + window_height]


    def _UnpackSymbolStacks(self):
        for stack in self.symbol_in_stacks:
            self.symbols += [stack[1] for _ in range(stack[0])]



    def _MakeReelofCommonSymbols(self, common_symbols, window_height):
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
            shuffled_reel = self._MakeReelofCommonSymbols(common_symbols, window_height)
        return shuffled_reel


    def _InsertSpecialSymbols(self, ready_reel, special_symbols, dist_bet_sp_symbols):
        sp_symbols = []
        indexes_between_huge_stacks = []

        for i, stack in enumerate(ready_reel):
            if (stack[0] > 1) and (ready_reel[(i+1) % self.number_of_stacks][0] > 1):
                indexes_between_huge_stacks.append(i+1)

        sp_symbols_list = []
        for symbol, stacks in special_symbols.items():
            sp_symbols.append(symbol)
            for stack in stacks:
                for i in range(stack[0]):
                    sp_symbols_list.append([stack[1], symbol])

        ready_reel, sp_symbols_list = self._InsertSpSymbols(ready_reel,
                                                            indexes_between_huge_stacks,
                                                            sp_symbols_list,
                                                            sp_symbols,
                                                            dist_bet_sp_symbols)

        if len(sp_symbols_list) == 0:
            return ready_reel

        indexes_to_input_sp_symbols = []
        for i, stack in enumerate(ready_reel):
            if self._CanIInsertSpSymbolInthisIndex(ready_reel, i, sp_symbols, dist_bet_sp_symbols + 1):
                indexes_to_input_sp_symbols.append(i)

        ready_reel, sp_symbols_list = self._InsertSpSymbols(ready_reel,
                                                            indexes_to_input_sp_symbols,
                                                            sp_symbols_list,
                                                            sp_symbols,
                                                            dist_bet_sp_symbols)

        if len(sp_symbols_list) != 0:
            print("\nWARNING !!! In reel not enough place to input special symbols,", len(sp_symbols_list), "special symbols not inserted.")
        return ready_reel


    def _CanIInsertSpSymbolInthisIndex(self, reel, index, sp_symbols, dist_bet_sp_symbols):
        left_neigh = self._LeftNeighbors(reel, index, dist_bet_sp_symbols+1)
        right_neigh = self._RightNeighbors(reel, index, dist_bet_sp_symbols+1, True)

        good_place = True
        for sp_symbol in sp_symbols:
            if (sp_symbol not in left_neigh) and (sp_symbol not in right_neigh):
                continue
            else:
                good_place = False
                break
        return good_place


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


    def _RightNeighbors(self, reel, stack_index, window_height, change_or_insert = False): #False - change True - insert
        right_neighbors = []
        step = (0 if change_or_insert else 1)
        while len(right_neighbors) != (window_height - 1):
            right_stack = reel[(stack_index + step) % self.number_of_stacks]
            for i in range(right_stack[0]):
                right_neighbors.append(right_stack[1])
                if len(right_neighbors) == (window_height - 1):
                    break
            stack_index += 1
        return right_neighbors


    def _InsertSpSymbols(self, reel, indexes_to_input, sp_symbols_list, sp_symbols, dist_bet_sp_symbols):
        inserted_indexes = []
        while len(sp_symbols_list) != 0 and len(indexes_to_input) != 0:

            rand_sp_stack_index = np.random.choice([*range(len(sp_symbols_list))])
            rand_place_index = np.random.choice([*range(len(indexes_to_input))])

            if self._CanIInsertSpSymbolInthisIndex(reel, indexes_to_input[rand_place_index] +
                                                               sum([1 for ind in inserted_indexes if
                                                                    ind < indexes_to_input[
                                                                        rand_place_index]]),
                                                   sp_symbols, dist_bet_sp_symbols):
                inserted_indexes.append(indexes_to_input[rand_place_index])
                reel.insert(indexes_to_input[rand_place_index]
                                  + sum(
                    [1 for ind in inserted_indexes if ind < indexes_to_input[rand_place_index]]),
                                  sp_symbols_list[rand_sp_stack_index])
                self.ln += sp_symbols_list[rand_sp_stack_index][0]
                self.number_of_stacks += 1
                del sp_symbols_list[rand_sp_stack_index]
            del indexes_to_input[rand_place_index]

        return reel, sp_symbols_list


if __name__ == "__main__":
    r = Reel(0)
    d = {}
    d[0] = [[10, 1], [5, 2], [3, 3]]
    d[1] = [[10, 1], [5, 2], [3, 3]]
    d[2] = [[10, 1], [5, 2], [3, 3]]
    d[3] = [[10, 1], [5, 2], [3, 3]]
    d[4] = [[10, 1], [5, 2], [3, 3]]
    d[5] = [[10, 1], [5, 2], [3, 3]]
    d[6] = [[10, 1], [5, 2], [3, 3]]
    d[7] = [[10, 1], [5, 2], [3, 3]]
    d[8] = [[10, 1], [5, 2], [3, 3]]
    d[9] = [[10, 1], [5, 2], [3, 3]]

    s = {}
    s[10] = [[20, 1]]
    r.MakeReel(d, s, 4, 3)
    percent = [10, 50, 35]
    patterns = [[[10], [1,2,3,4,5,6,7,8,9], [1,2,3,4,5,6,7,8,9]], [[1,2,3], [4,5,6], [7,8,9]], [[7,8,9], [5,6], [1,2,3]]]
    r.MakeWeights(patterns, percent, 3)
    print(r.symbols)
    print(r.weights)
