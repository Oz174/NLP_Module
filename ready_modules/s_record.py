import os
import speech_recognition as sr
from concurrent.futures import ThreadPoolExecutor


class SoundRecorder:
    @staticmethod
    def process_audio(audio_file):
        r = sr.Recognizer()
        try:
            with sr.AudioFile(audio_file) as source:
                audio_ans = r.record(source)
            sentence = r.recognize_google(audio_ans)
            return sentence
        except Exception as e:
            print(f'Error processing {audio_file}: {e}')
            return None

    @staticmethod
    def get_answers(path_to_answers):
        answers = {}
        try:
            assert os.path.exists(path_to_answers)
            audio_files = [os.path.join(path_to_answers, f)
                           for f in os.listdir(path_to_answers)
                           if f.endswith('.wav')]
        except AssertionError:
            print("Path does not exist")
            print(os.listdir(path_to_answers))
            return answers
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(
                SoundRecorder.process_audio, audio_file): audio_file
                for audio_file in audio_files}
            for future in futures:
                audio_file = futures[future]
                sentence = future.result()
                if sentence is not None:
                    answers[os.path.basename(audio_file)[-6:-4]] = sentence
        return answers
