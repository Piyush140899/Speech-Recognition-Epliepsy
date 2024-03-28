def plot_feature(feat_ind,feat_names,features_df,t):
  # feat_ind = 0
  # plt.clf()
  import matplotlib.pyplot as plt
  feat_name = feat_names[feat_ind]
  import matplotlib.pyplot as plt
  ind = np.shape(features_df)[0]
  # t = 5
  x = np.arange(0, ind*t, t)

  y = features_df.iloc[:, feat_ind].to_numpy()
  plt.plot(x, y)
  plt.xlabel('Time (seconds)')
  plt.ylabel(' {} value'.format(feat_name))
  plt.xticks(x)
  plt.grid()
  # plt.show()
  s = '/content/Plots/feature_'+feat_name+'.png'
  plt.savefig(s)
  plt.close()

def extract_feature_os(audio_file):
  import opensmile
  import numpy as np
  import librosa
  import pandas as pd

  # Create a SMILE extractor object
  smile = opensmile.Smile(
      feature_set=opensmile.FeatureSet.eGeMAPSv02,
      feature_level=opensmile.FeatureLevel.Functionals,
  )

  # Load the audio file
 
  signal, sr = librosa.load(audio_file, sr=None)

  # Set the segment length in seconds
  segment_length = 20

  # Divide the audio into segments and extract features
  features_list = []
  for i, start in enumerate(range(0, len(signal), sr * segment_length)):
      end = min(start + sr * segment_length, len(signal))
      segment = signal[start:end]
      features = smile.process_signal(segment, sr)
      features_list.append(features.to_numpy().flatten())

  # Convert the list of features to a pandas DataFrame
  features_df = pd.DataFrame(features_list)
  return features_df

if __name__ == "__main__":
  audio_file_path = r'/home/hp/Documents/Speech-Analysis/Voxit_v2/Grandfather_passage_clean.wav'
  df = extract_feature_os(audio_file_path)
  print(df.shape)
  