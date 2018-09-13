from collections import OrderedDict

# Filter class
class Filter:
  # Constructor
  def __init__(self, function):
    self.function = function

  # Return the input (impulse at x[0]) for a given index
  def x(self, n):
    return 1 if n == 0 else 0

  # Return the output for a given index
  def y(self, n):
    return self.function(n, self.x, self.y) if n >= 0 else 0

  # Return a dict with test results in the format n: (x,y)
  def test(self, num_samples):
    return OrderedDict((n, (self.x(n), self.y(n))) for n in range(0, num_samples))
