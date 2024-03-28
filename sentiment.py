import csv

def calculate_sentiment_scores(text):
    lexicon_path = "/home/hp/Documents/Speech-Analysis/Voxit_v2/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt"

    # Create a dictionary to store the emotion scores for each word
    emotion_scores = {}

    # Open the lexicon file
    with open(lexicon_path, "r") as file:
        reader = csv.reader(file, delimiter="\t")
        for row in reader:
            word = row[0]
            emotion = row[1]
            score = int(row[2])

            # Check if the word is already in the dictionary
            if word in emotion_scores:
                emotion_scores[word][emotion] = score
            else:
                emotion_scores[word] = {emotion: score}

    # Tokenize the text into individual words
    words = text.lower().split()

    # Calculate the sentiment scores for the text
    sentiment_scores = {emotion: 0 for emotion in emotion_scores["abandon"].keys()}  # Initialize sentiment scores

    for word in words:
        if word in emotion_scores:
            for emotion, score in emotion_scores[word].items():
                sentiment_scores[emotion] += score

    # Convert the sentiment scores to a list
    score_list = list(sentiment_scores.values())
    return score_list

# Example usage
text = """You wished to know all about my grandfather. Well, he is nearly ninety-three years
old; he dresses himself in an ancient black frock coat, usually minus several buttons;
yet he still thinks as swiftly as ever. A long, flowing beard clings to his chin, giving
those who observe him a pronounced feeling of the utmost respect. When he speaks,
his voice is just a bit cracked and quivers a trifle. Twice each day he plays skilfully
and with zest upon our small organ. Except in the winter when the ooze or snow or ice
prevents, he slowly takes a short walk in the open air each day. We have often urged
him to walk more and smoke less, but he always answers, “Banana oil!” Grandfather
likes to be modern in his language."""
scores = calculate_sentiment_scores(text)
print(scores)