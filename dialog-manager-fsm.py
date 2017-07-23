import sys

# =========================================================================
# Notes
#
# - Problem: Only one succeeding state can be specified per state so far.
# - Solution: Associate each state with more than one state (check, if
#   there is already a state associated for a state. If it is, then create
#   a list of succeeding states, if not, fine!)
# =========================================================================

class FSM(object):
    def __init__(self, initial_state, memory=None):
        self.state_transitions = {}
        self.state_transitions_any = {}
        self.default_transition = None

        self.input_symbol = None
        self.initial_state = initial_state
        self.current_state = self.initial_state
        self.next_state = None
        self.action = None
        self.memory = memory

    def reset(self):
        self.current_state = self.initial_state
        self.input_symbol = None

    def add_transition(self, input_symbol, state, action=None, next_state=None):
        if next_state is None:
            next_state = state
        self.state_transitions[(input_symbol, state)] = (action, next_state)

    def add_transition_list(self, input_symbols_list, state, action=None,
                            next_state=None):
        if next_state is None:
            next_state = state
        for input_symbol in input_symbols_list:
            self.add_transition(input_symbol, state, action, next_state)

    def add_transition_any(self, state, action=None, next_state=None):
        if next_state is None:
            next_state = state
        self.state_transitions_any[state] = (action, next_state)

    def set_default_transition(self, action, next_state):
        self.default_transition = (action, next_state)

    def get_transition(self, input_symbol, state):
        if self.state_transitions.has_key((input_symbol, state)):
            return self.state_transitions[(input_symbol, state)]
        elif self.state_transitions_any.has_key(state):
            return self.state_transitions_any[state]
        elif self.default_transition is not None:
            return self.default_transition
        else:
            raise Exception()

    def process (self, input_symbol):
        self.input_symbol = input_symbol
        (self.action, self.next_state) = self.get_transition(
            self.input_symbol, self.current_state)
        if self.action is not None:
            self.action(self)
        self.current_state = self.next_state
        self.next_state = None

    def process_list (self, input_symbols):
        for s in input_symbols:
            self.process(s)

class DialogManager(object):
    def __init__(self):
        self.fsm = FSM('START', [])
        self.name = ()
        self.gender = None
        self.salutation = 'Mr./Mrs.'
        self.destination = None

        self.greetings = ['Hello']
        self.destinations = ['Destination']
        self.farewells = ['Farewell']

    def greet(self, fsm):
        print 'Hello.'
        print 'What is your first name?'
        sys.stdout.write('> ')
        first_name = sys.stdin.readline().rstrip()
        print 'What is your second name?'
        sys.stdout.write('> ')
        last_name = sys.stdin.readline().rstrip()
        self.name = (first_name, last_name)

    def check_gender(self):
        # TODO
        # 1. Get gender by analyzing the name (likelihood check)
        # 2. Set salutation based on the gender
        pass

    def query_destination(self, fsm):
        print 'What is your destination?'
        sys.stdout.write('> ')
        self.destination = sys.stdin.readline().rstrip()

    def query_age(self):
        print 'How old are you?'
        sys.stdout.write('> ')
        age = sys.stdin.readline()
        print 'Your age: ' + age

    def farewell(self, fsm):
        print 'See you again, ' + self.salutation + ' ' + self.name[1].rstrip() + '!'

    def error(self, fsm):
        # TODO
        # Implement proper error handling
        print 'Error!'
        print str(fsm.input_symbol)

    def do_nothing(self, fsm):
        pass


    def run(self, input):
        self.fsm.set_default_transition(self.error, 'START')
        self.fsm.add_transition_any('START', None, 'START')
        self.fsm.add_transition     ('#',               'START',       self.do_nothing,      'GREETING')
        # self.fsm.add_transition     ('#',               'START',       self.do_nothing,      'AGE')
        # self.fsm.add_transition     ('Age',             'AGE',         self.query_age,         'GREETING')
        self.fsm.add_transition_list(self.greetings,    'GREETING',    self.greet,           'DESTINATION')
        self.fsm.add_transition_list(self.destinations, 'DESTINATION', self.query_destination, 'FAREWELL')
        self.fsm.add_transition_list(self.farewells,    'FAREWELL',    self.farewell,        'END')

        self.fsm.process_list(input)

if __name__ == '__main__':
    dialogManager = DialogManager()
    dialogManager.run(['#', 'Hello', 'Destination', 'Farewell'])
