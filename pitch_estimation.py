import pyworld as pw
import librosa
import numpy as np
x, fs = librosa.load('/home/hp/Documents/Speech-Analysis/Voxit_v2/Grandfather_passage_clean.wav', sr=None)

print(x)
f0, t = pw.dio(x.astype(np.float64), fs) 

arr1 = np.array(f0)
arr2 = np.array(t)

print(arr1[10000])
print(arr2)