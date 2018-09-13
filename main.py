from filter import Filter

# Main function
def main():
  filter = Filter(lambda n, x, y: 0.167772 * (x(n) + y(n - 8)) - x(n - 8))

  for n, (x, y) in filter.test(25).items():
    print("x[{0}] = {1}, y[{0}] = {2}".format(n, x, y))


# Execute the main function
if __name__ == "__main__":
  main()
