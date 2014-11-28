#!/usr/bin/python

import numpy as np
import cv2
import cv2.cv as cv
import PySynth.pysynth as ps
import math

V_FILE = 'data/hans_richter_rhythm_21.mp4'
N_MAP = {1:'a', 2:'b', 3:'c', 4:'d', 5:'e', 6:'f', 7:'g'}
LEVELS = 8

def get_features(fname):
  intensity = []; x = cv2.VideoCapture(fname)
  fps = x.get(cv.CV_CAP_PROP_FPS)
  while(True):
    # Capture frame-by-frame
    ret, frame = x.read()

    # Our operations on the frame come here
    try:
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    except:
      break

    # Display the resulting frame
    cv2.imshow('frame', gray)
    #if cv2.waitKey(1) & 0xFF == ord('q'):
    #  break
    intensity.append(sum(sum(gray)))

  # When everything done, release the capture
  x.release()
  cv2.destroyAllWindows()
  return (intensity, fps)

#print get_features(V_FILE)

def synth():
  intensities, fps = get_features(V_FILE)
  intensities = intensities[::int(fps)]
  m_value = max(intensities)
  interval_size = 1.0 / LEVELS
  s1 = [['r', 2]]
  for intensity in intensities:
    m_intensity = float(intensity)/float(m_value)
    level = math.floor(m_intensity / interval_size)
    if level == 0 or level == 8:
      s1.append(['r',  2])
    else:
      s1.append([N_MAP.get(level), 2])
  ps.make_wav(s1, fn = "pysynth_scale.wav")

synth()

##
