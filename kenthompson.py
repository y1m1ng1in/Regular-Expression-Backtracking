# .*.*=.*
from graphs import Plotting 
import argparse

expression = ".*.*=.*"

# .* concat .* concat = concat .*
infix_exp = [
  '.', '*',
  'concat',
  '.', '*',
  'concat',
  '=',
  'concat',
  '.', '*',
]

# .* .* = .* concat concat concat
postfix_exp = [
  '.', '*', '.', '*', '=', '.', '*',
  'concat','concat','concat',
]

UNARY_OP = 1
BINARY_OP = 2

# each value represents [the type of op, precedence]
ops = {
  '*':      [UNARY_OP, 2],
  'concat': [BINARY_OP, 1]
}


class Fragment:
  
  def __init__(self, frag_type, literal, 
               fragment, fragment2=None):
    self.nfa = {}
    self.id = 1
    
    if frag_type == 'literal':
      self.nfa = {
        self.id: { literal: set([self.id + 1]) }
      }
      if literal == '.':  # add an epsilon transition due to '.'
        self.nfa[self.id]['E'] = set([self.id + 1])
      self.start = self.id
      self.accept = self.id + 1
      self.state_num = 2

    elif frag_type == 'star':
      self.__migrate(fragment.nfa, 0)
      self.__epsilon_trans_at_accept(fragment.accept, fragment.start)
      # copy args into current construction
      self.id = fragment.id 
      self.start = fragment.start 
      self.accept = fragment.accept 
      self.state_num = fragment.state_num

    elif frag_type == 'concat':
      self.__migrate(fragment2.nfa, fragment.state_num)
      self.__migrate(fragment.nfa, 0)
      self.__epsilon_trans_at_accept(fragment.accept, fragment.state_num + fragment2.start)
      self.accept = fragment.state_num + fragment2.accept
      self.start = fragment.start
      self.state_num = fragment.state_num + fragment2.state_num
      self.id = -1  # temp

  def __migrate(self, nfa: dict, id_increment: int):
    for key in nfa:
      self.nfa[key + id_increment] = {}
      for lit in nfa[key]:
        self.nfa[key + id_increment][lit] = set([
          state + id_increment for state in nfa[key][lit]])

  def __epsilon_trans_at_accept(self, accept_id, trans_to):
    if accept_id not in self.nfa:
      self.nfa[accept_id] = {}
    if 'E' in self.nfa[accept_id]:
      self.nfa[accept_id]['E'].add(trans_to)
    else:
      self.nfa[accept_id]['E'] = set([trans_to])


class Construction:

  def __init__(self, postfix_exp, op):
    self.frag_stack = []
    for item in postfix_exp:
      if item not in op:
        self.frag_stack.append(Fragment('literal', item, None))
      else:
        if item == '*':
          top = self.frag_stack.pop()
          self.frag_stack.append(Fragment('star', None, top))
        elif item == 'concat':
          frag_back = self.frag_stack.pop()
          frag_front = self.frag_stack.pop()
          self.frag_stack.append(Fragment('concat', None, frag_front, frag_back))
    assert len(self.frag_stack) == 1
    self.nfa = self.frag_stack.pop()


class Simulation:

  def __init__(self, nfa, string):
    self.string = string
    self.nfa = nfa
    self.current_states = set([self.nfa.start])
    self.step = 0

  def run(self):
    for char in self.string:
      print("consume char:", char)
      new_states = set()
      for state in self.current_states:
        self.step += 1
        assert state in self.nfa.nfa
        new_states.update(self.__epsilon_trans(state))
        if '.' in self.nfa.nfa[state]:
          new_states.update(self.nfa.nfa[state]['.'])
        if char in self.nfa.nfa[state]:
          new_states.update(self.nfa.nfa[state][char])
      self.current_states = new_states
      print("in states:", self.current_states)
    return self.__is_accepted()

  def __is_accepted(self):
    return self.nfa.accept in self.current_states

  def __epsilon_trans(self, state):
    """ Return a set of all reachable states by epsilon transition
    """
    reachables = set()
    queue = []
    explored_trans = set()
    done = False
    self.step += 1
    if 'E' in self.nfa.nfa[state]:
      queue.extend(self.nfa.nfa[state]['E'])
      reachables.update(self.nfa.nfa[state]['E'])
      explored_trans.update([(state, trans_to) for trans_to in self.nfa.nfa[state]['E']])
    while not done:
      if len(queue) == 0:
        return reachables
      s = queue.pop(0)
      if 'E' in self.nfa.nfa[s]:
        for s1 in self.nfa.nfa[s]['E']:
          if s1 not in queue and (s, s1) not in explored_trans:
            queue.append(s1)
            reachables.add(s1)
            explored_trans.add((s, s1))
    return reachables


parser = argparse.ArgumentParser(description='ken thompson\'s algorithm simulator')
parser.add_argument('--num', 
                    '-n', 
                    type=int,
                    default=200, 
                    help="number of experiment to execute")
parser.add_argument('--disable-graph',
                    '-d',
                    action="store_true",
                    help="disable print charts")
args = parser.parse_args()

graph_disabled = args.disable_graph

nfa = Construction(postfix_exp, ops)
steps = []
exp_num = args.num

for i in range(1, exp_num + 1):
  string = "x=" + "x" * i
  print("\nmatching", string)
  s = Simulation(nfa.nfa, string)
  r = s.run()
  print(r, s.step)
  steps.append(s.step)

if not graph_disabled:
  p = Plotting("ken thompson's algorithm", steps, exp_num)
  p.plot()


