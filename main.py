from filter import AllPassFilter


# Main function
def main():
  filter = AllPassFilter(8 ,0.167772)
  test_results = filter.test(25)

  for n, y in enumerate(test_results):
    print("y[{}] = {}".format(n, y))


# Execute the main function
if __name__ == "__main__":
  main()
