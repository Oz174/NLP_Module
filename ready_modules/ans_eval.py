from nltk.corpus import stopwords  # => stop words removal
from collections import Counter
import math

Extra_Stop_Words = {"the", ",", "a", "an", "and", "or", "in", "on", "to", "is",
                    "are", "was", "were", "am", "i", "you", "he", "she", "it",
                    "we", "they", "for", "of", "that", "this", "with", "as",
                    "at", "by", "from", "up", "down", "out", "about", "over",
                    "under", "again", "further", "then", "once", "here",
                    "there", "when", "where", "why", "how",
                    "all", "any", "both", "each", "few", "more",
                    "most", "other", "some", "such", "no", "nor",
                    "not", "only", "own", "same", "so", "than",
                    "too", "very", "s",
                    "t", "can", "will", "just", "don", "should", "now"}


class AnswerEvaluator:
    def __init__(self, model_answer, keywords,
                 extra_stop_words=None):
        self.model_answer = model_answer
        self.keywords = keywords
        self.STOP_WORDS = set(stopwords.words("english"))
        if extra_stop_words:
            self.STOP_WORDS = self.STOP_WORDS.union(set(extra_stop_words))

    def calculate_tf(self, document):
        tf = {}
        word_count = Counter(document)
        total_words = len(document)
        for word, count in word_count.items():
            tf[word] = count / total_words
        return tf

    def calculate_idf(self, documents):
        k = 0.3
        total_documents = len(documents)
        all_words = set(word for document in documents for word in document)
        idf = {word: math.log(
            (total_documents + k) /
            (1 + sum(1 for doc in documents if word in doc)))
            for word in all_words}
        return idf

    def calculate_tfidf(self, tf, idf):
        tfidf = {word: tf[word] * idf[word] for word in tf}
        return tfidf

    def cosine_similarity(self, vector1, vector2):
        dot_product = sum(vector1.get(word, 0) * vector2.get(word, 0)
                          for word in set(vector1) & set(vector2))

        magnitude1 = math.sqrt(sum(value ** 2 for value in vector1.values()))
        magnitude2 = math.sqrt(sum(value ** 2 for value in vector2.values()))

        if magnitude1 != 0 and magnitude2 != 0:
            return dot_product / (magnitude1 * magnitude2)
        else:
            return 0

    def keyword_matching_score(self, student_answer, keywords):
        student_answer_lower = student_answer.lower()
        keywords_lower = [keyword.lower() for keyword in keywords]
        score = 0
        for keyword in keywords_lower:
            if keyword in student_answer_lower:
                score += 1
        if keywords_lower:
            score /= len(keywords_lower)
        return score

    def evaluate(self, student_answer, keywords):
        tokens1 = [word for word in self.model_answer.lower().split()
                   if word not in self.STOP_WORDS]
        tokens2 = [word for word in student_answer.lower().split()
                   if word not in self.STOP_WORDS]

        documents = [tokens1, tokens2]
        tf1 = self.calculate_tf(tokens1)
        tf2 = self.calculate_tf(tokens2)
        idf = self.calculate_idf(documents)
        tfidf1 = self.calculate_tfidf(tf1, idf)
        tfidf2 = self.calculate_tfidf(tf2, idf)
        similarity_score = self.cosine_similarity(tfidf1, tfidf2)
        keywords_score = self.keyword_matching_score(student_answer, keywords)
        try:
            final_score = (similarity_score/keywords_score) * \
                (similarity_score + keywords_score)/2
        except ZeroDivisionError:
            final_score = 0
        return 1 if final_score > 1 else final_score
