from collections import OrderedDict
from time import time


# Filter class
class Filter:
  # Constructor
  def __init__(self, function):
    self.function = function

  # Apply the filter to an input buffer and return the output buffer
  def __call__(self, input_buffer, overhead = 0):
    # Create the output buffer
    output_buffer = []

    # Create the input function
    def x(n):
      return input_buffer[n] if n in range(len(input_buffer)) else 0

    # Create the output function
    def y(n):
      if n in range(len(output_buffer)):
        return output_buffer[n]
      elif n in range(len(input_buffer) + overhead):
        return self.function(n, x, y)
      else:
        return 0

    # Iterate over the input buffer and apply the filter to each sample
    for n in range(len(input_buffer) + overhead):
      output_buffer.append(y(n))

    # Return the output buffer
    return output_buffer

  # Apply the filter to the impulse and return the impluse response
  def impulse_response(self, length):
    impulse = [1]
    return self(impulse, length - len(impulse))


# Delay class
class Delay(Filter):
  # Return a new instance
  def __new__(cls, samples):
    return Filter(lambda n, x, y: x(n - samples))


# All pass filter class
class AllPassFilter(Filter):
  # Return a new instance
  def __new__(cls, order, coefficient):
    return Filter(lambda n, x, y: coefficient * (x(n) + y(n - order)) - x(n - order))
