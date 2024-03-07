from nlp import NLP_MODULE


if __name__ == "main":
    nlp_class_module = NLP_MODULE(
        "../audio samples/interviewee_answer", "../questions.json")
    nlp_class_module.prepare_data()
    nlp_class_module.generate_results()
    nlp_class_module.export_results_to_json()
