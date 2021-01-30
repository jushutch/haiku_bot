from random import randint
import requests
import json
from twython import Twython
import pathlib
import twitter_keys

MAX_RESULTS = 1
WORD_FILE_PATH = str(pathlib.Path(__file__).parent.absolute()) + "/nouns.txt"
WORDLIST = open(WORD_FILE_PATH).read().splitlines()
SCORE_PERCENTILE = 0.5


def get_topic_word() -> str:
    random_word = WORDLIST[randint(0, len(WORDLIST) - 1)]
    request = requests.get("https://api.datamuse.com/words?",
                           params={
                               "sp": random_word,
                               "md": "s",
                               "max": MAX_RESULTS,
                           })
    if request.status_code == 200:
        content = json.loads(request.content.decode("utf-8"))
        word = content[0]["word"]
        return word
    
def get_line(total_syllables: int, seed: str, part_of_speech: str) -> str :
    words = []
    get_line_recursive(total_syllables, seed, part_of_speech, words)
    return " ".join(words)


def get_line_recursive(total_syllables: int, seed: str, part_of_speech: str, words: list):
    if total_syllables <= 0:
        return ""
    request = requests.get("https://api.datamuse.com/words?",
                           params=get_params_by_part_of_speech(seed, part_of_speech))
    if request.status_code == 200:
        content = json.loads(request.content.decode("utf-8"))
        while len(content) > 0:
            random_index = randint(0, int(len(content)*SCORE_PERCENTILE))
            word = content[random_index]["word"]
            syllables = content[random_index]["numSyllables"]
            pos = content[random_index].get("tags", ["u"])[0]
            if syllables <= total_syllables and word != "." and word not in words:
                # print(f"Word: {word} \t NumSyllables: {syllables}")
                total_syllables -= syllables
                if pos == "n":
                    get_line_recursive(total_syllables, word, pos, words)
                    words.append(word)
                    return
                elif pos == "adj":
                    words.append(word)
                    get_line_recursive(total_syllables, word, pos, words)
                    return
                words.append(word)
                get_line_recursive(total_syllables, word, pos, words)
                return
            else:
                content.pop(random_index)
        raise Exception("No words for syllable criteria")
    raise Exception("Problem communicating with server")


def get_params_by_part_of_speech(seed: str, part_of_speech: str) :
    if part_of_speech == "n":
        return {
            "rc": seed,
            "md": "sp",
            "rel_jjb": seed,
            "max":998,
        }
    elif part_of_speech == "adj":
        return {
            "lc": seed,
            "md":"sp",
            "rel_jja": seed,
            "max":998,
        }
    return {
        "lc": seed,
        "topics": seed,
        "md": "sp",
    }


def post_haiku_to_twitter(title: str, haiku: str):
    api = Twython(twitter_keys.CONSUMER_KEY, 
		twitter_keys.CONSUMER_SECRET, 
		twitter_keys.ACCESS_KEY, 
		twitter_keys.ACCESS_SECRET)
    response = api.update_status(status=f"Title: {title}\n\n{haiku}")
    print(response["created_at"])
    print(f"Title: {title}\n{haiku}\n\n")


if __name__ == "__main__":
    topic = get_topic_word()
    first_line  = get_line(5, topic, "n")
    second_line = get_line(7, topic, "n")
    third_line  = get_line(5, topic, "n")
    haiku = f"{first_line}\n{second_line}\n{third_line}"
    post_haiku_to_twitter(topic, haiku)

