import sys

from filter import Delay, AllPassFilter
from waveutils import WaveReader, WaveWriter


def apply_filter(input_file, output_file, filter):
  # Create the input file
  reader = WaveReader(input_file)
  print("Input: {!s}".format(reader))

  # Create the output file
  writer = WaveWriter(output_file, 2, reader.sample_width, reader.sample_rate)
  print("Output: {!s}".format(writer))

  # Read the samples from the input file (only first channel)
  print("Reading samples...")
  input_buffer = [sample[0] for sample in reader.read()]

  # Apply the filter to the samples
  print("Applying filter...")
  filter_buffer = filter(input_buffer)

  # Write the samples to the output file (L = input sample, R = filtered sample)
  print("Writing samples...")
  output_buffer = [(input_buffer[n], filter_buffer[n]) for n in range(len(input_buffer))]
  #output_buffer = [(sample,) for sample in filter_buffer]
  for buf in zip(*(output_buffer[i::512] for i in range(512))):
    writer.write(buf)

# Main function
def main(args):
  input_file = "resources/ttd00_mono.wav"
  output_file = "resources/ttd00_allpass.wav"
  #filter = Delay(4000)
  filter = AllPassFilter(8000, 0.02)

  apply_filter(input_file, output_file, filter)


# Execute the main function
if __name__ == "__main__":
  main(sys.argv)
