# import pandas as pd
# import re
#
# def clean_text(text):
#     noise_list = ('_0xxx_')
#     # Removing special characters
#     text = re.sub(noise_list, '', text)
#     # Remove non-alphanumeric characters and convert to lowercase
#     text = re.sub(r'\W+', ' ', text).lower().strip()
#     # Remove extra whitespace
#     text = re.sub(r'\s+', ' ', text)
#     return text
#
# df = pd.DataFrame({'A': [' Hello! ', 'world', ' How?', 'Are...', 'you _0xxx_']})
#
# df['A_clean'] = df['A'].apply(clean_text)
#
# print(df)
'-----------------------------------------------------------------------------------------------------------------------'

from difflib import SequenceMatcher
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import re

def clean_text(text):
    noise_list = ('_0xxx_')
    # Removing special characters
    text = re.sub(noise_list, '', text)
    # Remove non-alphanumeric characters and convert to lowercase
    text = re.sub(r'\W+', ' ', text).lower().strip()
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    return text

def is_similar(s1, s2):
    s1_clean = clean_text(s1)
    s2_clean = clean_text(s2)

    # Using SequenceMatcher
    seq_matcher = SequenceMatcher(None, s1_clean, s2_clean)
    ratio = seq_matcher.ratio()

    # Using Cosine Similarity
    vectorizer = CountVectorizer(stop_words='english').fit_transform([s1_clean, s2_clean])
    cos_sim = cosine_similarity(vectorizer)[0][1]

    return ratio*100 >= 90 and cos_sim*100 >= 90

# Create example dataframe
df = pd.DataFrame({'A': ['', 'world', ' How?', 'Are...', 'you _0xxx_'],
                   'B': ['', 'universe', 'how', 'is', 'you.']})

# Add column indicating if strings are similar
df['Similar'] = df.apply(lambda row: is_similar(row['A'], row['B']), axis=1)

# Print dataframe
print(df)
