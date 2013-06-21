doc = Document.getCurrentDocument()

def is_valid_ascii(byte):
  return byte >= 0x20 and byte <= 0x7e

def is_null(byte):
  return byte == 0x00

MIN_LEN = 4
strings = []
addresses = []

start_string = 0
curr_string = ""

for seg_id in range(0, doc.getSegmentCount()):
  seg = doc.getSegment(seg_id)

  seg_start = seg.getStartingAddress()
  seg_stop = seg_start + seg.getLength()

  for adr in range(seg_start, seg_stop):
    val = seg.readByte(adr)

    if is_valid_ascii(val):
      curr_string += chr(val)
      if start_string == 0:
        start_string = adr
    elif is_null(val):
      if len(curr_string) > MIN_LEN:
        strings.append(curr_string)
        addresses.append(start_string)
        curr_string = ""
        start_string = 0
      else:
        curr_string = ""
        start_string = 0
    else:
      curr_string = ""
      start_string = 0

for i in range(0, len(strings)):
  string = strings[i]
  adr = addresses[i]
  seg = doc.getSegmentAtAddress(adr)
  seg.setTypeAtAddress(adr, len(string) + 1, Segment.TYPE_ASCII) 

doc.log("Found and marked " + str(len(strings)) + " strings.")
