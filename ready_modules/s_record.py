import speech_recognition as sr
import os


class SoundRecorder:
    @staticmethod
    def get_answers(path_to_answers):
        answers = {}
        r = sr.Recognizer()
        answers_files = [os.path.join(path_to_answers, f) for f in os.listdir(
            path_to_answers) if f.endswith('.wav')]
        for audio in answers_files:
            sentence = ""
            # Use  the  reсоgnize_google()  funсtiоn  tо  reсоgnize  the  аudiо
            with sr.AudioFile(audio) as source:
                audio_ans = r.record(source)
            try:
                sentence = r.recognize_google(audio_ans)
                # In order to take the question number only from the file name
                answers[audio[-6:-4]] = sentence
            except Exception as e:
                print('Error:  ' + str(e))
        return answers
