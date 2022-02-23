import numpy as np

from pyics import Model

class CASim(Model):
    def __init__(self):
        Model.__init__(self)

        self.t = 0
        self.rule_set = []
        self.config = None
        self.transient_length = -1

        self.make_param('r', 1)
        self.make_param('k', 2)
        self.make_param('width', 50)
        self.make_param('height', 50)
        self.make_param('initial_random', True)
        self.make_param('labda', 0.0)

    def setter_rule(self, val):
        """Setter for the rule parameter, clipping its value between 0 and the
        maximum possible rule number."""
        rule_set_size = self.k ** (2 * self.r + 1)
        max_rule_number = self.k ** rule_set_size
        return max(0, min(val, max_rule_number - 1))

    def setter_labda(self, val):
        return max(0, min(val, 1))

    def build_rule_set(self):
        """Sets the rule set for the current rule.
        A rule set is a list with the new state for every old configuration.

        For example, for rule=34, k=3, r=1 this function should set rule_set to
        [0, ..., 0, 1, 0, 2, 1] (length 27). This means that for example
        [2, 2, 2] -> 0 and [0, 0, 1] -> 2."""
        self.rule_set = np.zeros(self.k ** (2 * self.r + 1))
        nonvisited = [i for i in range(len(self.rule_set))]

        for _ in range(int(len(self.rule_set) * self.labda)):
            rand_idx = np.random.choice(nonvisited)
            self.rule_set[rand_idx] = np.random.randint(1, self.k)
            nonvisited.remove(rand_idx)

        return self.rule_set

    def check_rule(self, inp):
        """Returns the new state based on the input states.

        The input state will be an array of 2r+1 items between 0 and k, the
        neighbourhood which the state of the new cell depends on."""
        length = len(self.rule_set) - 1
        result = ''
        for elem in inp:
            result += str(int(elem))
        result = int(result, self.k)

        end = self.rule_set[length - result]
        return end

    def setup_initial_row(self):
        """Returns an array of length `width' with the initial state for each of
        the cells in the first row. Values should be between 0 and k."""
        if self.initial_random == True:
            return [np.random.randint(0, self.k) for _ in range(self.width)]
        else:
            ones = [0 for _ in range(self.width)]
            ones[len(ones) // 2] = 1
            return ones

    def reset(self):
        """Initializes the configuration of the cells and converts the entered
        rule number to a rule set."""

        self.t = 0
        self.config = np.zeros([self.height, self.width])
        self.config[0, :] = self.setup_initial_row()
        self.build_rule_set()
        self.transient_length = -1
        self.shannonlist = []
        self.entropy = None

    def draw(self):
        """Draws the current state of the grid."""

        import matplotlib
        import matplotlib.pyplot as plt

        plt.cla()
        if not plt.gca().yaxis_inverted():
            plt.gca().invert_yaxis()
        plt.imshow(
            self.config,
            interpolation='none',
            vmin=0,
            vmax=self.k - 1,
            cmap=matplotlib.cm.binary,
        )
        plt.axis('image')
        plt.title('t = %d' % self.t)

    def step(self):
        """Performs a single step of the simulation by advancing time (and thus
        row) and applying the rule to determine the state of the cells."""
        self.calculated = False
        self.t += 1
        if self.t >= self.height:
            self.entropy = np.mean(self.shannonlist)
            print(int((self.r-1)*22+(self.k-2)*11+self.labda*10))
            return True

        number_dict = {x: 0 for x in range(self.k ** (2 * self.r + 1))}

        for patch in range(self.width):
            # We want the items r to the left and to the right of this patch,
            # while wrapping around (e.g. index -1 is the last item on the row).
            # Since slices do not support this, we create an array with the
            # indices we want and use that to index our grid.
            indices = [
                i % self.width
                for i in range(patch - self.r, patch + self.r + 1)
            ]
            values = self.config[self.t - 1, indices]
            self.config[self.t, patch] = self.check_rule(values)
            string = ''
            for elem in values:
                string += str(int(elem))
            num = int(string, self.k)
            number_dict[num] += 1

        for i in range(self.t):
            if (
                np.all(self.config[i] == self.config[self.t])
                and self.calculated != True
            ):
                self.transient_length = i
                self.calculated = True

        # self.shannonlist = []
        shannonsum = -sum(
            number_dict[x] / self.width * np.log2(number_dict[x] / self.width)
            for x in number_dict
            if number_dict[x] != 0
        )
        self.shannonlist.append(shannonsum)



if __name__ == '__main__':
    sim = CASim()
    # from pyics import GUI

    # cx = GUI(sim)
    # cx.start()
    from pyics import paramsweep

    sim.reset()
    paramsweep(
        sim,
        10,
        {
            'width': 40,
            'height': 1000,
            'k': [2, 3],
            'r': [1, 2],
            'labda': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
        },
        ['transient_length', 'entropy'],
        csv_base_filename='data',
        measure_interval=0,
    )
