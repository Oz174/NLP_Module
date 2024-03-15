# pylint disable=line-too-long
""" This module is used to generate feedback messages and spider graph. """
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')


class FeedbackGenerator:
    """
    This class is used to generate feedback messages and spider graph.
    """
    @staticmethod
    def generate_feedback_message(scores: dict,
                                  fb_folder: str = "feedback samples/"):
        """
        This method is used to generate feedback message.
        :param scores: dict
        :param fb_folder: str
        :return: None
        """
        feedback_message = "Here is your feedback:\n"
        mappings = []
        areas = list(scores.keys())
        for _, item in scores.items():
            if item <= 0.5:
                mappings.append("low")
            elif item <= 0.8:
                mappings.append("medium")
            else:
                mappings.append("high")

        for area, category in zip(areas, mappings):
            # shall be removed on higher integration
            try:
                path = fb_folder + area + "/" + category + ".txt"
                with open(path, "r", encoding='utf-8') as file:
                    messages = file.readlines()
                    # random choice of one message from the file
                    feedback_message += messages[np.random.randint(
                        0, len(messages))] + "\n"
            except FileNotFoundError as exc:
                raise FileNotFoundError("Feedback file not found") from exc

        print(feedback_message)

    @staticmethod
    def spider_graph_generator(scores):
        """
        This method is used to generate spider graph.
        :param scores: dict
        :return: None
        """
        # split the dict into 2 lists
        scores_dict = scores
        scores = list(scores_dict.values())

        if max(scores) < 1:
            scores = [round(score, 0)*100 for score in scores]

        scores_dict = list(scores_dict.keys())

        scores_dict_angles = np.linspace(
            0, 2*np.pi, len(scores), endpoint=False)
        scores_dict_angles = np.concatenate(
            (scores_dict_angles, [scores_dict_angles[0]]))
        scores.append(scores[0])
        scores_dict.append(scores_dict[0])

        fig = plt.figure(figsize=(5, 5))
        ax = fig.add_subplot(polar=True)
        # basic plot
        ax.plot(scores_dict_angles, scores, 'o--',
                color='g', linewidth=2, label='Scores')
        # fill plot
        ax.fill(scores_dict_angles, scores, alpha=0.25, color='g')
        # Add labels
        ax.set_thetagrids(scores_dict_angles * 180/np.pi, scores_dict)
        plt.grid(True)
        plt.tight_layout()
        plt.legend()
        plt.show()
