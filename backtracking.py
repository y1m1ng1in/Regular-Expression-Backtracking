# .*.*=.*
from graphs import Plotting

class Backtracking:

  def __init__(self, string):
    # the string to be matched against 
    self.string = string
    
    # the actual length of string (ending 'E' not included)
    self.string_len = len(self.string) - 1  

    # the splited components of a regular expression
    self.pattern_exp = ['.*', '.*', '=', '.*']

    # whether the algorithm is done
    self.done = False

    # the upper bound of index of string
    self.max_string_index = len(string) - 1

    # index intervals [,) for each .* to consume chars in string 
    self.intervals = [
      [0, self.max_string_index], 
      [self.max_string_index, self.max_string_index], 
      [self.max_string_index, self.max_string_index]
    ]

    # keep track of the number of steps
    self.step = 1

    # whether current step is a backtrack step
    self.backtrack_step = False

    # current index that points to the pattern_exp
    self.pattern_pointer = 0

  def find_steps(self, index_from, index_to, in_backtrack):
    assert index_from <= index_to
    if index_from == index_to or in_backtrack:
      return 1
    return index_to - index_from

  def print_step(self, index_from, index_to, index_ptn, in_backtrack):
    print_num = { 0: '1st', 1: '2nd', 2: '3rd' }
    if not in_backtrack:
      print("step", self.step, "Greedily match chars with", print_num[index_ptn], ".*")
    else:
      print("step", self.step, "Backtrack and rematch", print_num[index_ptn], ".*")
    if index_from == index_to:
      print("step", self.step, "match empty string with", print_num[index_ptn], ".*")
    else:
      print("step", self.step, "match index ", "[" + str(index_from) + ", " + str(index_to) + ")", 
            "with", print_num[index_ptn], ".*")
    if not in_backtrack:
      return 2
    return 1

  def backtrack_intervals(self, intervals, max_string_index):
    assert len(intervals) == 3
    if intervals[1][1] <= intervals[1][0]:
      intervals[0][1] -= 1
      intervals[1][0] -= 1
      intervals[1][1] = max_string_index
      return 0
    else:
      intervals[1][1] -= 1
      return 1

  def run(self):
    while not self.done:
      if self.pattern_pointer == 0:
        self.step += self.print_step(self.intervals[0][0], 
                                     self.intervals[0][1], 
                                     self.pattern_pointer, 
                                     self.backtrack_step)
        self.backtrack_step = False
        self.pattern_pointer += 1

      if self.pattern_pointer == 1:
        self.step += self.print_step(self.intervals[1][0], 
                                     self.intervals[1][1], 
                                     self.pattern_pointer, 
                                     self.backtrack_step)
        self.pattern_pointer += 1
      
      if self.pattern_pointer == 2: 
        # backtrack needed
        if self.pattern_exp[self.pattern_pointer] != self.string[self.intervals[1][1]]:
          print("step", self.step, 
                "match index " 
                + str(self.intervals[1][1]) 
                + " " 
                + self.string[self.intervals[1][1]] 
                + " with =, backtrack")
          self.step += 1
          self.pattern_pointer = self.backtrack_intervals(self.intervals, self.max_string_index)
          self.backtrack_step = True
          continue
        else: 
          # match '=' successfully, then match the rest of chars with the last '.*'
          print("step", self.step, "attemp to match =")
          print("step", self.step, 
                "match index " 
                + str(self.intervals[1][1]) 
                + " " + self.string[self.intervals[1][1]] 
                + " with =")
          self.step += 2
          self.intervals[2][0] = self.intervals[1][1]
          if self.intervals[1][0] == self.intervals[1][1]:
            self.intervals[2][0] += 1
          self.pattern_pointer += 1
          
      if self.pattern_pointer == 3:
        self.step += self.print_step(self.intervals[2][0], len(self.string), 2, False)
        self.done = True
        print("step", self.step, "done!")


steps = []
exp_num = 200

for i in range(1, exp_num + 1):
  b = Backtracking("x=" + "x" * i + "E")
  b.run()
  steps.append(b.step)

p = Plotting("backtracking algorithm", steps, exp_num)
p.plot()