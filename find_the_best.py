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
with open('15_59_53.log') as f:
    audio_data = f.read()


def classify_language_transcription(languages: list, confidence_percentage_for_each_language: list) -> list:

    if (languages.__len__() == 0):
        return confidence_percentage_for_each_language

    language_with_confidence_level = request_for_transcription(languages.pop(0))

    confidence_percentage_for_each_language.append(
        language_with_confidence_level
    )

    return classify_language_transcription(languages, confidence_percentage_for_each_language)


def request_for_transcription(language: str) -> dict:
    result = requests.\
        post(f'https://speech.googleapis.com/v1/speech:recognize?key={key}',
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

    return retrieve_confidence_with_transcription(result.json())


def retrieve_confidence_with_transcription(transcription_result: dict) -> dict:
    all_transcription_possible =\
        transcription_result["results"][0]["alternatives"]

    return retrieve_transcription_with_highest_confidence(
        all_transcription_possible, {"confidence": 0}, {"confidence": 0}
    )


def retrieve_transcription_with_highest_confidence(
    all_transcriptions: list,
    previous_transcript: dict,
    transcription_with_highest_confidence: dict ) -> dict:

    if (all_transcriptions.__len__() == 0):
        return transcription_with_highest_confidence

    current_transcript = all_transcriptions.pop(0)

    if (current_transcript["confidence"] > previous_transcript["confidence"]\
        and current_transcript["confidence"] > transcription_with_highest_confidence["confidence"]):
            transcription_with_highest_confidence = current_transcript

    return retrieve_transcription_with_highest_confidence(
        all_transcriptions, current_transcript, transcription_with_highest_confidence )


if __name__ == '__main__':
    langauges = ['en-GB', 'en-ZA', 'en-US']
    c = classify_language_transcription(langauges, [])
    print(c)