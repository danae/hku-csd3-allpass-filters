import struct
import wave


# Constants
sample_width_formats = {1: 'B', 2: 'h', 4: 'i'}

# Convert frames to tuples of samples per channel
def frames_to_samples(frames, channels, sample_width):
  # Unpack the frames and normalize them
  format = "<{}{}".format(int(len(frames) / sample_width), sample_width_formats[sample_width])
  frames = struct.unpack(format, frames)
  samples = [frame / 2 ** (7 * sample_width) for frame in frames]

  # Split the samples per channel
  samples = zip(*(samples[i::channels] for i in range(channels)))

  # Return the samples
  return samples

# Convert a tuple of samples per channel to a frame
def samples_to_frames(samples, channels, sample_width):
  # Check if the samples have the correct number of channels
  for sample in samples:
    if len(sample) != channels:
      raise RuntimeError("Sample {!r} has not the required amount of channels ({})".format(sample, channels))

  # Merge the channeled samples
  samples = [channel for sample in samples for channel in sample]

  # Clip samples between -1 and 1
  samples = [max(-1.0, min(sample, 1.0)) for sample in samples]

  # Denormalize the samples and pack them
  format = "<{}{}".format(len(samples), sample_width_formats[sample_width])
  frames = [int(sample * 2 ** (7 * sample_width)) for sample in samples]
  frames = struct.pack(format, *frames)

  # Return the frames
  return frames


# Wave reader class
class WaveReader:
  # Constructor
  def __init__(self, file_name):
    # Create the wave file
    self.file_name = file_name
    self.file = wave.open(file_name,'rb')

    # Get the parameters
    self.channels = self.file.getnchannels()
    self.sample_width = self.file.getsampwidth()
    self.sample_rate = self.file.getframerate()

  # Read the next frame as a tuple of samples per channel
  def read(self, chunk_size = 512):
    # Iterate over the frames
    while self.file.tell() < self.file.getnframes():
      # Read a chunk of frames and convert them to samples
      frames = self.file.readframes(chunk_size)
      samples = frames_to_samples(frames, self.channels, self.sample_width)

      # Yield the samples
      for sample in samples:
        yield sample

  # Convert to string
  def __str__(self):
    return "{}, channels: {}, sample width: {} bits, sample rate: {} Hz".format(self.file_name, self.channels, self.sample_width * 8, self.sample_rate)


# Wave reader class
class WaveWriter:
  # Constants
  width_formats = {1: 'B', 2: 'h', 4: 'i'}

  # Constructor
  def __init__(self, file_name, channels, sample_width = 2, sample_rate = 44100):
    # Create the wave file
    self.file_name = file_name
    self.file = wave.open(file_name,'wb')

    # Set the parameters
    self.channels = channels
    self.sample_width = sample_width
    self.sample_rate = sample_rate

    self.file.setnchannels(channels)
    self.file.setsampwidth(sample_width)
    self.file.setframerate(sample_rate)

  # Write a tuple of samples per channel to the file
  def write(self, samples):
    # Convert samples to frames and write them to the file
    frames = samples_to_frames(samples, self.channels, self.sample_width)
    self.file.writeframes(frames)

  # Convert to string
  def __str__(self):
    return "{}, channels: {}, bit depth: {} bit, sample rate: {} Hz".format(self.file_name, self.channels, self.sample_width * 8, self.sample_rate)
