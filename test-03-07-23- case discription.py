# def jaccard_distance(str1, str2):
#     """
#     Calculates the Jaccard distance between two strings.
#     """
#     set1 = set(str1.lower().split())
#     set2 = set(str2.lower().split())
#     intersection = len(set1.intersection(set2))
#     union = len(set1.union(set2))
#     return 1 - (intersection / union)
#
#
# st1 = '''From: Ted Davis [mailto:tdavis@kjconsulting.net] _x000D_
# Sent: Monday, January 24, 2011 10:10 AM_x000D_
# To: 'DJ Cho (djcho)'_x000D_
# Cc: 'Ted Davis'_x000D_
# Subject: Payment for Audit of $14,239.08-K&J Consulting Services, Inc._x000D_
# Importance: High_x000D_
# _x000D_
#  PI Reference:  33133676_x000D_
# 	Payment 1 of 15.		_x000D_
#    Payment Type:	USD Wire	 	Beneficiary ID:	1233857430	_x000D_
#    Value Date:	01/24/2011	 	Beneficiary:	Cisco	_x000D_
#    Debit Account:	005491205163	 	Beneficiary Bank ID:	026009593	_x000D_
#    Payment Amount:	14,239.08   USD	 	Status:	In Process	_x000D_
# _x000D_
# DJ,_x000D_
# _x000D_
# The wire has been sent and I used the Beneficiary name as: Cisco. Please let me know if this is correct. Thanks _x000D_'''
#
# st2 = '''From: Ted Davis [mailto:tdavis@kjconsulting.net]
# Sent: Monday, January 24, 2011 10:10 AM
# To: 'DJ Cho (djcho)'
# Cc: 'Ted Davis'
# Subject: Payment for Audit of $14,239.08-K&J Consulting Services, Inc.
# Importance: High
#
#  PI Reference:  33133676
# 	Payment 1 of 15.
#    Payment Type:	USD Wire	 	Beneficiary ID:	1233857430
#    Value Date:	01/24/2011	 	Beneficiary:	Cisco
#    Debit Account:	005491205163	 	Beneficiary Bank ID:	026009593
#    Payment Amount:	14,239.08   USD	 	Status:	In Process
#
# DJ,
#
# The wire has been sent and I used the Beneficiary name as: Cisco. Please let me know if this is correct. Thanks
# '''
#
# distance = jaccard_distance(st1, st2)
# print(distance)  # Output: 0.0


'-----------------------------------------------------------------------------------------------------------------------'

# from fuzzywuzzy import fuzz
#
# st1 = "From: Ted Davis [mailto:tdavis@kjconsulting.net] Sent: Monday, January 24, 2011 10:10 AM To: 'DJ Cho (djcho)' Cc: 'Ted Davis' Subject: Payment for Audit of $14,239.08-K&J Consulting Services, Inc. Importance: High PI Reference: 33133676 Payment 1 of 15. Payment Type: USD Wire Beneficiary ID: 1233857430 Value Date: 01/24/2011 Beneficiary: Cisco Debit Account: 005491205163 Beneficiary Bank ID: 026009593 Payment Amount: 14,239.08 USD Status: In Process DJ, The wire has been sent and I used the Beneficiary name as: Cisco. Please let me know if this is correct. Thanks"
#
# st2 = "From: Ted Davis [mailto:tdavis@kjconsulting.net] _x000D_ Sent: Monday, January 24, 2011 10:10 AM_x000D_ To: 'DJ Cho (djcho)'_x000D_ Cc: 'Ted Davis'_x000D_ Subject: Payment for Audit of $14,239.08-K&J Consulting Services, Inc._x000D_ Importance: High_x000D_ _x000D_ PI Reference:  33133676_x000D_ Payment 1 of 15.		_x000D_ Payment Type:	USD Wire	 	Beneficiary ID:	1233857430	_x000D_ Value Date:	01/24/2011	 	Beneficiary:	Cisco	_x000D_ Debit Account:	005491205163	 	Beneficiary Bank ID:	026009593	_x000D_ Payment Amount:	14,239.08   USD	 	Status:	In Process	_x000D_ _x000D_ DJ,_x000D_ _x000D_ The wire has been sent and I used the Beneficiary name as: Cisco. Please let me know if this is correct. Thanks _x000D_"
#
# similarity_score = fuzz.ratio(st1, st2)
# jaccard_distance = fuzz.jaccard(st1, st2)
#
# print("Similarity Score:", similarity_score)
# print("Jaccard Distance:", jaccard_distance)
#
# if similarity_score >= 80 and jaccard_distance <= 0.2:
#     print("The two strings are considered to be the same.")
# else:
#     print("The two strings are different.")


'-----------------------------------------------------------------------------------------------------------------------'

# from fuzzywuzzy import fuzz
#
# st1 = '''From: Ted Davis [mailto:tdavis@kjconsulting.net]
# Sent: Monday, January 24, 2011 10:10 AM
# To: 'DJ Cho (djcho)'
# Cc: 'Ted Davis'
# Subject: Payment for Audit of $14,239.08-K&J Consulting Services, Inc.
# Importance: High
#
#  PI Reference:  33133676
#     Payment 1 of 15.
#    Payment Type:    USD Wire        Beneficiary ID:    1233857430
#    Value Date:    01/24/2011        Beneficiary:    Cisco
#    Debit Account:    005491205163        Beneficiary Bank ID:    026009593
#    Payment Amount:    14,239.08   USD        Status:    In Process
#
# DJ,
#
# The wire has been sent and I used the Beneficiary name as: Cisco. Please let me know if this is correct. Thanks'''
#
# st2 = '''From: Ted Davis [mailto:tdavis@kjconsulting.net] _x000D_
# Sent: Monday, January 24, 2011 10:10 AM_x000D_
# To: 'DJ Cho (djcho)'_x000D_
# Cc: 'Ted Davis'_x000D_
# Subject: Payment for Audit of $14,239.08-K&J Consulting Services, Inc._x000D_
# Importance: High_x000D_
# _x000D_
#  PI Reference:  33133676_x000D_
#     Payment 1 of 15.        _x000D_
#    Payment Type:    USD Wire        Beneficiary ID:    1233857430    _x000D_
#    Value Date:    01/24/2011        Beneficiary:    Cisco    _x000D_
#    Debit Account:    005491205163        Beneficiary Bank ID:    026009593    _x000D_
#    Payment Amount:    14,239.08   USD        Status:    In Process    _x000D_
# _x000D_
# DJ,_x000D_
# _x000D_
# The wire has been sent and I used the Beneficiary name as: Cisco. Please let me know if this is correct. Thanks _x000D_'''
#
# # Calculate the Jaccard similarity using the token set approach
# jaccard_similarity = fuzz.token_set_ratio(st1, st2)
#
# # Print the Jaccard similarity
# print("Jaccard similarity:", jaccard_similarity)
#
# # Calculate the Levenshtein distance
# levenshtein_distance = fuzz.ratio(st1, st2)
#
# # Print the Levenshtein distance
# print("Levenshtein distance:", levenshtein_distance)

'-----------------------------------------------------------------------------------------------------------------------'

# from difflib import SequenceMatcher
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
#
# st1 = '''From: Ted Davis [mailto:tdavis@kjconsulting.net]
# Sent: Monday, January 24, 2011 10:10 AM
# To: 'DJ Cho (djcho)'
# Cc: 'Ted Davis'
# Subject: Payment for Audit of $14,239.08-K&J Consulting Services, Inc.
# Importance: High
#
#  PI Reference:  33133676
# 	Payment 1 of 15.
#    Payment Type:	USD Wire	 	Beneficiary ID:	1233857430
#    Value Date:	01/24/2011	 	Beneficiary:	Cisco
#    Debit Account:	005491205163	 	Beneficiary Bank ID:	026009593
#    Payment Amount:	14,239.08   USD	 	Status:	In Process
#
# DJ,
#
# The wire has been sent and I used the Beneficiary name as: Cisco. Please let me know if this is correct. Thanks'''
#
# st2 = '''From: Mark [mailto:tdavis@kjconsulting.net]
# Sent: Monday, December 24, 2011 10:10 PM
# To: 'DJ Cho (djcho)'
# Cc: 'Ted Davis'_x000D_
# Subject: Payment for Audit of $14,239.08-K&J Consulting Services, Inc.
# Importance: High
#
#  PI Reference:  3313
# 	Payment 1 of 15.
#    Payment Type:	USD Wire	 	Beneficiary ID:	1233
#    Value Date:	01/24/2012	 	Beneficiary:	Cisco
#    Debit Account:	0054912	 	Beneficiary Bank ID:	02
#    Payment Amount:	14,239.08   USD	 	Status:	In Process
#
# DJ,
#
# The wire has been sent and I used the Beneficiary name as: Cisco. Please let me know if this is correct. Thanks
# '''
#
# # Using SequenceMatcher
# seq_matcher = SequenceMatcher(None, st1, st2)
# ratio = seq_matcher.ratio()
# print("SequenceMatcher Ratio:", ratio)
#
# # Using Cosine Similarity
# vectorizer = CountVectorizer().fit_transform([st1, st2])
# cos_sim = cosine_similarity(vectorizer)[0][1]
# print("Cosine Similarity:", cos_sim)
#
# if ratio*100 and cos_sim*100 >= 90:
#     print("The two strings are considered to be the same.")
# else:
#     print("The two strings are different.")
#
'-----------------------------------------------------------------------------------------------------------------------'

# from difflib import SequenceMatcher
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
#
# st1 = "From: Ted Davis [mailto:tdavis@kjconsulting.net] \
# Sent: Monday, January 24, 2011 10:10 AM \
# To: 'DJ Cho (djcho)' \
# Cc: 'Ted Davis' \
# Subject: Payment for Audit of $14,239.08-K&J Consulting Services, Inc. \
# Importance: High \
#  \
#  PI Reference:  33133676 \
#     Payment 1 of 15.         \
#    Payment Type: USD Wire    Beneficiary ID: 1233857430    \
#    Value Date: 01/24/2011    Beneficiary: Cisco    \
#    Debit Account: 005491205163    Beneficiary Bank ID: 026009593    \
#    Payment Amount: 14,239.08   USD    Status: In Process    \
#  \
# DJ, \
#  \
# The wire has been sent and I used the Beneficiary name as: Cisco. Please let me know if this is correct. Thanks"
#
# st2 = "From: Ted Davis [mailto:tdavis@kjconsulting.net] _x000D_ \
# Sent: Monday, January 24, 2011 10:10 AM_x000D_ \
# To: 'DJ Cho (djcho)'_x000D_ \
# Cc: 'Ted Davis'_x000D_ \
# Subject: Payment for Audit of $14,239.08-K&J Consulting Services, Inc._x000D_ \
# Importance: High_x000D_ \
# _x000D_ \
#  PI Reference:  33133676_x000D_ \
#     Payment 1 of 15.        _x000D_ \
#    Payment Type: USD Wire    Beneficiary ID: 1233857430    _x000D_ \
#    Value Date: 01/24/2011    Beneficiary: Cisco    _x000D_ \
#    Debit Account: 005491205163    Beneficiary Bank ID: 026009593    _x000D_ \
#    Payment Amount: 14,239.08   USD    Status: In Process    _x000D_ \
# _x000D_ \
# DJ,_x000D_ \
# _x000D_ \
# The wire has been sent and I used the Beneficiary name as: Cisco. Please let me know if this is correct. Thanks _x000D_"
#
# # Compute SequenceMatcher similarity score
# s = SequenceMatcher(None, st1, st2)
# seq_match_ratio = s.ratio()
#
# # Compute cosine similarity score
# vectorizer = CountVectorizer().fit_transform([st1, st2])
# cos_sim = cosine_similarity(vectorizer)[0][1]
#
# # Set the similarity threshold
# threshold = 0.9
#
# # Check if the similarity scores are above the threshold
# if seq_match_ratio > threshold and cos_sim > threshold:
#     print("The two strings are a match!")
# else:
#     print("The two strings do not match.")

'-----------------------------------------------------------------------------------------------------------------------'

# from difflib import SequenceMatcher
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import pandas as pd
# import re
#
# def clean_text(text):
#     noise_list = ['_x000D_']
#     # Removing special characters
#     text = re.sub(noise_list, '', text)
#     # Remove non-alphanumeric characters and convert to lowercase
#     text = re.sub(r'\W+', '', text).lower().strip()
#     # Remove extra whitespace
#     text = re.sub(r'\s+', '', text)
#     return text
#
# # Create example dataframe
# df = pd.DataFrame({'A': [' Hello! ', 'world', ' How?', 'Are...', 'you _0xxx_'],
#                    'B': ['Hello', 'universe', 'how', 'is', 'it.']})
#
# for i in range(min(len(df['A']), len(df['B']))):
#     s1 = clean_text(df['A'][i])
#     s2 = clean_text(df['B'][i])
#
#     # Using SequenceMatcher
#     seq_matcher = SequenceMatcher(None, s1, s2)
#     ratio = seq_matcher.ratio()
#
#     # Using Cosine Similarity
#     vectorizer = CountVectorizer().fit_transform([s1, s2])
#     cos_sim = cosine_similarity(vectorizer)[0][1]
#
#     print(f"Comparing '{s1}' and '{s2}':")
#     print("SequenceMatcher Ratio:", ratio)
#     print("Cosine Similarity:", cos_sim)
#
#     if ratio*100 and cos_sim*100 >= 90:
#         print("The two strings are considered to be the same.\n")
#     else:
#         print("The two strings are different.\n")

'-----------------------------------------------------------------------------------------------------------------------'

from difflib import SequenceMatcher
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import re

def clean_text(text):
    if not text:
        return ''
    noise_list = ('_0xxx_')
    # Removing special characters
    text = re.sub(noise_list, '', text)
    # Remove non-alphanumeric characters and convert to lowercase
    text = re.sub(r'\W+', ' ', text).lower().strip()
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    return text

def is_similar(s1, s2):
    try:
        s1_clean = clean_text(s1)
        s2_clean = clean_text(s2)

        # Using SequenceMatcher
        seq_matcher = SequenceMatcher(None, s1_clean, s2_clean)
        ratio = seq_matcher.ratio()

        # Using Cosine Similarity
        vectorizer = CountVectorizer(stop_words='english', min_df=1).fit_transform([s1_clean, s2_clean])
        cos_sim = cosine_similarity(vectorizer)[0][1]

        return ratio*100 >= 90 and cos_sim*100 >= 90
    except:
        return True

# Create example dataframe
df = pd.DataFrame({'A': ['', 'world', ' How is??', 'Are...', 'you _0xxx_'],
                   'B': ['', 'universe', 'how??  is', 'is', 'you.'],
                   'C': ['11111', '22222', '33333', '444444', '55555'],
                   'D': ['1111', '22222', '33333', '444444', '55555']})

# Add column indicating if strings are similar
df['Similar- AB'] = df.apply(lambda row: is_similar(row['A'], row['B']), axis=1)
df['Similar- CD'] = df.apply(lambda row: is_similar(row['C'], row['D']), axis=1)

# Print dataframe
print(df)

