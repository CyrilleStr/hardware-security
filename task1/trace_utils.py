# %% [markdown]
# # Load and analyze measured traces
# 
# You need:
# * `traceLength.txt`: how many samples per trace (one decimal number)
# * `traces.bin`: raw measured traces, one byte per sample (uint8), all traces together continuously
# 
# There should be also PT and CT files
# * `plaintext.txt`: all PT blocks, (one block per line, in hex, bytes separated by spaces)
# * `ciphertext.txt`: all CT blocks, (one block per line, in hex, bytes separated by spaces)
# 
# And a screenshot and scope config files

# %%
import matplotlib.pyplot as plt
import numpy as np
import os

# %%
# Load PT of CT from file
def load_text(file_name: str):
    """
    Load any text PT/CT from file containing hex strings with bytes 
    separated by spaces, one block per line
    
    Arguments:
        file_name -- File name string

    Returns:
        Output is a matrix of bytes (np.array)
    """
    txt_str = open(file_name).readlines()
    if (txt_str[-1].rstrip() == ""): del txt_str[-1] #discard last empty line
    #split each line into bytes and convert from hex
    txt_bytes_list = list(
        map(lambda line: 
                list(
                    map(lambda s: int(s, 16),
                        line.rstrip().split(" "))
                ),
            txt_str)
        )
    return np.array(txt_bytes_list, 'uint8')

# %%
# read length of one complete trace (number of samples per trace)
def read_trace_length(fname: str):
  """
  Reads trace length from a text file, usually traceLength.txt

  Arguments:
    fname -- File name string
  
  Returns:
    The trace length (int)
  """
  with open(fname, "r") as fin:
    trace_length = int(fin.readline())
  return trace_length

# %%
def load_traces(fname: str, trace_length: int, tr_start: int, tr_len: int, dtype='uint8'):
  """
  Load specified slice of all traces from file

  Arguments:
    fname -- file name string. File contains raw traces stored linearly without header

    trace_length -- length of each trace in samples

    tr_start -- starting sample of each trace
    
    tr_len -- length of slice from each trace

  Keyword Arguments:
    dtype -- data type of samples in the file (default 'uint8')

  Returns:
    Matrix with the selected slice of all traces (np.array)
  """
  # trim each trace - select interesting part
  traces_file_name = fname
  traces_file_size = os.path.getsize(traces_file_name)
  num_of_traces = traces_file_size // trace_length
  if traces_file_size % trace_length:
    print(f"Traces file {traces_file_name} has size {traces_file_size}, which is not divisible by {trace_length}! That seems wrong.")
  print(f"Traces file {traces_file_name} assumed shape ({num_of_traces} x {trace_length})")
  print(f"Reading all {num_of_traces} traces, each from {tr_start}, length {tr_len}")
  traces = np.zeros([num_of_traces, tr_len], dtype = dtype)
  with open(traces_file_name, "rb") as f:
    for i in range(num_of_traces):
      f.seek(i * trace_length + tr_start, 0)
      traces[i] = np.frombuffer(f.read(tr_len), dtype = dtype)
  return traces


