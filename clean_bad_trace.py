def clean_bad_trace(trace):
    """Clean up a bad trace from microcontroller"""

    # Remove line endings from text file
    global dummy
    trace_2 = []
    for i in trace:
        trace_2.append(i.rstrip())

    # Remove empty strings, fix line skipping and convert to floating point
    trace_3 = []
    for i in list(filter(None, trace_2)):
        if 5 >= float(i) >= 3:
            trace_3.append(float(i))
            dummy = i
        else:
            trace_3[-1] = float(dummy + i)

    return trace_3
