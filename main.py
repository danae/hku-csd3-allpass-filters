from filter import AllPassFilter


# Main function
def main():
  filter = AllPassFilter(8 ,0.167772)
  test_results = filter.impulse_response(1000)


# Execute the main function
if __name__ == "__main__":
  main()
