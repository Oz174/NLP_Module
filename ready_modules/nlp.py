# pylint: disable=line-too-long
import os
from ans_eval import AnswerEvaluator
from s_record import SoundRecorder
from fb_gen import FeedbackGenerator
import json
import sys
import numpy as np


class NLP_MODULE:
    def __init__(self, path_to_interviewee_answers: str, model_answers_json: str):
        self.path_to_interviewee_answers = path_to_interviewee_answers
        self.model_answers_json = model_answers_json
        self.questions_w_model_answers = {}
        self.interviewee_answers = {}
        self.results = {}

    def prepare_data(self):
        # Takes too long , need to be optimized by threading
        if self.model_answers_json is None or not self.model_answers_json.endswith("json"):
            raise TypeError(
                "Incorrect name or not json format")

        with open(self.model_answers_json, "r") as file:
            questions_w_model_answers = json.load(file)

        interviewee_answers = [f for f in os.listdir(
            self.path_to_interviewee_answers)]
        # Assert 1
        assert len(questions_w_model_answers) == len(
            interviewee_answers), "Length Mismatch between audio files and answers"
        # Assert 2
        def ans_no(x): return x[:-4]
        assert list(questions_w_model_answers.keys()) == list(
            map(ans_no, interviewee_answers)), "Keys Mismatch among questions' numbers"
        del ans_no
        self.interviewee_answers = SoundRecorder.get_answers(
            self.path_to_interviewee_answers)
        self.questions_w_model_answers = dict(
            sorted(questions_w_model_answers.items()))
        return self.questions_w_model_answers, self.interviewee_answers

    def generate_results(self):
        results = {}
        for ques_no, answer in self.questions_w_model_answers.items():
            model_answer = answer['model_answer']
            keywords = answer['hint_keywords']
            # print(f"Model Answer : {answer['model_answer']}
            # \n Keywords: {answer['hint_keywords']}")
            a_evaluator = AnswerEvaluator(model_answer, keywords)
            for q_no, ans in self.interviewee_answers.items():
                if q_no == ques_no:
                    results[q_no] = a_evaluator.evaluate(ans, keywords)
        print("Scores for each question ...  ")
        print(results)
        self.results["technical"] = np.mean(list(results.values()))
        self.results["personal"] = np.random.random()
        self.results["social"] = np.random.random()
        print(self.results)
        FeedbackGenerator.generate_feedback_message(self.results)
        FeedbackGenerator.spider_graph_generator(self.results)
        del self.questions_w_model_answers
        del self.interviewee_answers
        return

    def export_results_to_json(self):
        with open("results.json", "w") as file:
            json.dump(self.results, file, indent=4)
        del self.results
        return


if __name__ == "__main__":
    # take arguments from command line
    # nlp_class_module = NLP_MODULE(sys.argv[0], sys.argv[1])
    nlp_class_module = NLP_MODULE(
        "audio samples/interviewee_answer", "questions.json")
    nlp_class_module.prepare_data()
    nlp_class_module.generate_results()
    nlp_class_module.export_results_to_json()
