import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords, wordnet
from string import punctuation
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
import lightgbm as lgb
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords, wordnet
from string import punctuation
import random
from nltk.tokenize import sent_tokenize
from collections import Counter
import re
    
# Download necessary NLTK resources
nltk.download('vader_lexicon')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

x = [{'title': '5.0 out of 5 stars\nNice product', 'review': '5.0 out of 5 stars', 'rating': 'The product is good. With all the features and works well'}, {'title': '4.0 out of 5 stars\nEasy to use and value for money', 'review': '4.0 out of 5 stars', 'rating': 'It is easy and sturdy in usage.. makes some extra noise, which could have been reduced, but heats well, easy to clean and low on maintenance.'}, {'title': '5.0 out of 5 stars\ndebasishdas4321@gmail.com', 'review': '5.0 out of 5 stars', 'rating': "Very good item but missing the owner's manual, cook book and shelf. How can i get those missing materials?"}, {'title': '5.0 out of 5 stars\nVery good.', 'review': '5.0 out of 5 stars', 'rating': 'Worth the money paid.'}, {'title': '5.0 out of 5 stars\ngood to know', 'review': '5.0 out of 5 stars', 'rating': 'Easy to use, working well.'}, {'title': '4.0 out of 5 stars\nNice product with good quality', 'review': '4.0 out of 5 stars', 'rating': 'It has good build quality with all features in solo microwave and can be perfect for solo functions of microvave.'}, {'title': '1.0 out of 5 stars\nReceived defective product', 'review': '1.0 out of 5 stars', 'rating': 'Received defective product it keeps changing time on its own and the panel becomes unresponsive making me switch it off from the main switch. On calling for repair company says ask seller to replace and seller says ask company to repair. Stuck.'}, {'title': '3.0 out of 5 stars\nGood but very noisy.', 'review': '3.0 out of 5 stars', 'rating': 'LG Makes good quality products, but this one is too noisy and poorly designed.I bought it for my office. Opening and closing the lid of this microwave is so loud that everyone in the office knows someone is using the microwave. Makes a loud clunky-plasticky-metally thud when opening or closing the lid. Since the opening and closing of the lid is spring-loaded, you can not avoid the noise even with slow careful operation. Other than that, there is no problem. But this noisy lid is a good enough deal-breaker for me.Would definitely advise to avoid this model if you are buying for an office or for a quiet home.'}, {'title': '4.0 out of 5 stars\nMicrowave LG', 'review': '4.0 out of 5 stars', 'rating': "It's a good product. Except the door makes high noise while closing. Rest everything fine."}, {'title': '4.0 out of 5 stars\nOk product', 'review': '4.0 out of 5 stars', 'rating': 'Ok kind of product but a little noisy. Serves purpose'}]
def Sentimental_score(x):    
    reviews = []
    ratings = []

    # Iterate over each dictionary in x
    for item in x:
        # Append the 'review' and 'rating' values to their respective lists
        reviews.append(item['review'])
        ratings.append(item['rating'])

    list1 = []
    for item in reviews:
        # Use regular expression to match the first number in each string
        match = re.match(r'^(\d+\.\d+|\d+)', item)
        if match:
            # Extract the matched number and append it to list1
            list1.append(match.group())

    #print(list1)

    # Convert each string element to float and then to integer
    integer_list = [int(float(num)) for num in list1]

    #print("Integer list:", integer_list)
    rating=integer_list
    #print(rating)
    review=ratings
    #print(review)

    reviews= ' '.join(review)
    paragraph=reviews
    from googletrans import Translator

    # Define the paragraph
    #paragraph = "Your paragraph goes here."
    #spanish
    #paragraph="Este producto es increíblemente útil en mi día a día. Me encanta lo fácil que es de usar y lo bien que funciona. Definitivamente lo recomendaría a cualquier persona que esté buscando mejorar su vida diaria. ¡Gracias al fabricante por crear un producto tan fantástico"
    #french
    #paragraph="C'est produit est incroyablement utile dans ma vie quotidienne. J'adore à quel point il est facile à utiliser et à quel point il fonctionne bien. Je le recommanderais certainement à quiconque cherche à améliorer son quotidien. Merci au fabricant d'avoir créé un produit si fantastique !"
    # hindi
    #paragraph="यह उत्कृष्ट उत्पाद है! मुझे यह खरीदने का बहुत ही अच्छा निर्णय था। इसकी गुणवत्ता बहुत अच्छी है और इसका काम भी बहुत ही अच्छा है। मैं इसे सभी को सुझाव दूंगा।"
    #kannada
    #paragraph="ಈ ಅದ್ಭುತ ಉತ್ಪನ್ನವಾಗಿದೆ! ಇದನ್ನು ಖರೀದಿಸುವುದು ಒಳ್ಳೆಯ ನಿರ್ಣಯವಾಯಿತು. ಇದರ ಗುಣಮಟ್ಟ ತುಂಬಾ ಚೆನ್ನಾಗಿದೆ ಮತ್ತು ಇದರ ಕೆಲಸವೂ ಅದ್ಭುತವಾಗಿದೆ. ನಾನು ಇದನ್ನು ಎಲ್ಲರಿಗೂ ಶಿಫಾರಸು ಮಾಡುತ್ತೇನೆ."


    # Initialize the translator
    translator = Translator()

        # Detect the language of the paragraph
    language = translator.detect(paragraph).lang

        # If the detected language is not English, translate the paragraph to English
    if language != 'en':
        translated_paragraph = translator.translate(paragraph, src=language, dest='en').text
    else:
        translated_paragraph = paragraph

    # Assign the translated paragraph back to the original variable
    paragraph = translated_paragraph

    # Print the translated paragraph
    #print(paragraph)
    


    # Tokenize the paragraph into sentences
    sentences = sent_tokenize(paragraph)

    # Count the frequency of each sentence
    sentence_count = Counter(sentences)

    # Sort the sentences by frequency (most common first)
    sorted_sentences = sentence_count.most_common()

    # Display the summary
    print("Summary:")
    """for i,(sentence, count) in enumerate(sorted_sentences):
        print(sentence.strip())
    """
    from nltk.sentiment import SentimentIntensityAnalyzer
    from nltk.corpus import stopwords, wordnet
    from string import punctuation

    # Sample paragraph
    #paragraph = "Your paragraph goes here."

    # Initialize VADER sentiment analyzer
    sia = SentimentIntensityAnalyzer()

    # Tokenize the paragraph into words
    words = nltk.word_tokenize(paragraph)

    # Get English stopwords and punctuation marks
    english_stopwords = set(stopwords.words('english'))
    english_punctuation = set(punctuation)

    # Initialize a list to store good, bad, and neutral words
    good_words = []
    bad_words = []
    neutral_words = []

    # Function to check if a word is meaningful
    def is_meaningful(word):
        synsets = wordnet.synsets(word)
        return len(synsets) > 0

    # Classify words as good, bad, or neutral
    for word in words:
        if word.lower() in english_stopwords or word in english_punctuation:
            continue
        if not is_meaningful(word):
            continue

        score = sia.polarity_scores(word)
        if score['compound'] >= 0.05:
            good_words.append(word)
        elif score['compound'] <= -0.05:
            bad_words.append(word)
        else:
            neutral_words.append(word)

    # Convert lists to sets to remove duplicates
    good_words = set(good_words)
    bad_words = set(bad_words)
    neutral_words = set(neutral_words)

    print("Good Words:", good_words)
    print("Bad Words:", bad_words)
    print("Neutral Words:", neutral_words)

    counts = [len(good_words), len(bad_words), len(neutral_words)]
    # Convert the counts to string format
    counts_string = [str(count) for count in counts]

    # Convert the list of counts to a single string
    result_string = ', '.join(counts_string)

    # Print the result string
    #print(type(result_string))
    #print(result_string)

    #print(counts)

    # Assign weights to good, bad, and neutral words
    weight_good = 2
    weight_bad = -2
    weight_neutral = 1

    # Calculate sentiment score based on weighted counts
    sentiment_score = (weight_good * len(good_words)) + (weight_bad * len(bad_words)) + (weight_neutral * len(neutral_words))

    #print("Sentiment Score:", sentiment_score)
    # Sample weights (you can adjust these according to your preference)
    weight_good = 2
    weight_bad = -2
    weight_neutral = 1

    # Calculate the sentiment score
    total_words = len(good_words) + len(bad_words) + len(neutral_words)
    sentiment_score = (len(good_words) * weight_good + len(bad_words) * weight_bad + len(neutral_words) * weight_neutral) / total_words

    # Normalize the sentiment score to ensure it lies between 0 and 1
    normalized_sentiment_score = (sentiment_score + 1) / 2

    #print("Sentiment Score:", normalized_sentiment_score)


    # Sample data generation
    ratings = [random.randint(1, 5) for _ in range(100)]  # Generating 100 random ratings between 1 and 5

    # Reshape the ratings list to a 2D array with one column
    ratings_2d = [[rating] for rating in ratings]

    # Split the data into features (X) and target (y)
    X = ratings_2d
    y = [random.uniform(1, 5) for _ in range(len(ratings))]  # Generating random satisfaction scores as targets

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize models
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(),
        "XGBoost": XGBRegressor(),
        #"LightGBM": lgb.LGBMRegressor()
    }

    # Train and evaluate each model
    from sklearn.metrics import mean_squared_error
    import numpy as np

    for name, model in models.items():
       # print(f"Training {name}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        #print(f"{name} MSE: {mse}")
        #print(f"{name} RMSE: {rmse}")  

    # You can select the best model based on the evaluation metric (e.g., MSE)

    return paragraph , normalized_sentiment_score,result_string
paragraph , y ,z = Sentimental_score(x)
print("Sentiment Score:",y)


def summarize_paragraph(paragraph):
    # Tokenize the paragraph into sentences
    sentences = paragraph.split('.')
    
    # Initialize an empty list to store the summary lines
    summary_lines = []
    
    # Combine sentences to form 10 lines
    line_count = 0
    current_line = ""
    for sentence in sentences:
        if line_count < 10:
            if len(current_line + sentence) <= 100:  # Assuming each line has a maximum of 100 characters
                current_line += sentence.strip() + ". "
            else:
                summary_lines.append(current_line.strip())
                current_line = sentence.strip() + ". "
                line_count += 1
        else:
            break
    
    # Add the last line to the summary lines
    summary_lines.append(current_line.strip())
    
    return summary_lines

# Call the function to get the summary lines
summary_lines = summarize_paragraph(paragraph)

# Print the summary lines
for i, line in enumerate(summary_lines):
    print(f" {i+1}: {line}\n")

#print(paragraph)
print("length of good,bad, neutral:",z)