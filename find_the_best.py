import requests
import json

with open('speech_key.json') as f:
    key = json.load(f)
key = key['key']

phrases = []
with open('phrases.txt', 'r') as f:
    for row in f:
        phrases.append(row.rstrip('\n'))

audio_data = ''
with open('14_36_01.log') as f:
    audio_data = f.read()


# def classify_language_transcription(languages: list) -> list:
#     confidence_percentage_for_each_language = []

#     if (languages.__len__() == 0):
#         return confidence_percentage_for_each_language

#     language_with_confidence_level = request_for_transcription(languages.pop(0))
#     confidence_percentage_for_each_language.append(
#         language_with_confidence_level
#     )

#     return classify_language_transcription(languages)


def request_for_transcription(language: str) -> dict:
    result =\
    requests.post(f'https://speech.googleapis.com/v1/speech:recognize?key={key}',
    headers={
        "Content-Type": "application/json"
    },
    data=json.dumps({
        "config": {
            "encoding": "FLAC",
            "sampleRateHertz": 44100,
            "languageCode": language,
            "speechContexts": [
                {
                    "phrases": phrases
                }
            ],
            "maxAlternatives": 10
        },
        "audio": {
            "content": audio_data
        }
    }))

    retrieve_confidence_with_transcription(result.json())
    # return json.loads(result)


def retrieve_confidence_with_transcription(transcription_result: dict) -> dict:
    all_transcription_possible =\
        json.dumps(transcription_result["results"][0]["alternatives"])

    retrieve_transcription_with_highest_confidence(
        all_transcription_possible
    )


def retrieve_transcription_with_highest_confidence(
    all_transcriptions: list,
    previous_transcript: dict ) -> dict:

    transcription_with_highest_confidence = {}
    current_highest_confidence_level = previous_transcript["confidence"]

    if (all_transcriptions.__len__() == 0):
        return transcription_with_highest_confidence

    current_transcript = all_transcriptions.pop(0)

    if (current_highest_confidence_level < current_transcript["confidence"]):
        transcription_with_highest_confidence = current_transcript

request_for_transcription('en-GB')
# if __name__ == '__main__':
#     langauges = ['en-GB', 'en-SA', 'en-US']
#     classify_language_transcription(langauges)