from __future__ import print_function, unicode_literals
import random
import logging
import os

os.environ['NLTK_DATA'] = os.getcwd() + '/nltk_data'

from textblob import TextBlob
from config import FILTER_WORDS #Groserias

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

#start:example-hello.py
#Sentences we'll respond with if the user greets us

GREETING_KEYWORDS = ("hello", "hi", "greetings", "sup", "what's up", "good morning", "good afternoon", "good evening")

GREETING_RESPONSES = ["Hey", "Good morning", "Good afternoon", "Good evening", "Hello", "How can I help you with?", "I'm here to serve"]

def check_for_greeting(sentence):
    #If the user says hi, return a greeting
    for word in sentence.words:
        if word.lower() in GREETING_KEYWORDS:
            return random.choice(GREETING_RESPONSES)

# start:example-none.py
# Sentences we'll respond with if we have no idea what the user just said
NONE_RESPONSES = [
    "Excuse me, I didn't understand",
    "I'm afraid I didn't understand",
    "Sorry, could you repeat your statement please?",
]
# end

# start:example-self.py
# If the user tries to tell us something about ourselves, use one of these responses
COMMENTS_ABOUT_SELF = [
    "I'm here to serve",
    "I'm Astrobot, Astros' best bot (and better than humans, haha).",
    "That's me. How can I help you?",
]
# end

class UnnacceptableUtteranceException(Exception):
    #Si dice una Groseria
    pass

def starts_with_vowel(word):
    #check for pronoun compatibility "a" or "an"
    return True if word[0] in 'aeiou' else False

def broback(sentence):
    #Main program
    logger.info("Astrobot: Respond to %s", sentence)
    resp = respond(sentence)
    return resp

def find_pronoun(sent):
    #Find best pronoun to respond with
    pronoun = None
    for word, part_of_speech in sent.pos_tags:
        if part_of_speech == 'PRP' and word.lower() == 'you':
            pronoun = 'I'
        elif part_of_speech == 'PRP' and word.lower() == 'I':
            pronoun = 'You'
    return pronoun

def find_verb(sent):
    #Candidate verb for the sentence
    verb = None
    pos = None
    for word, part_of_speech in sent.pos_tags:
        if part_of_speech.startswith('VB'):
            verb = word
            pos = part_of_speech
            break
    return verb, pos

def find_noun(sent):
    #Find best candidate noun
    noun = None

    if not noun:
        for w, p in sent.pos_tags:
            if p == 'NN':
                noun = w
                break
    if noun:
        logger.info("Found noun: %s", noun)

    return noun

def find_adjective(sent):
    #Find adjective
    adj = None
    for w, p in sent.pos_tags:
        if p == 'JJ':
            adj = w
            break
    return adj

def construct_response(pronoun, noun, verb):
    #No special cases matched
    resp = []

    if pronoun:
        resp.append(pronoun)

    if verb:
        verb_word = verb[0]
        if verb_word in ('be', 'am', 'is', "'m"):
            if pronoun.lower() == 'you':
                resp.append("aren't really")
            else:
                resp.append(verb_word)

    if noun:
        pronoun = "an" if starts_with_vowel(noun) else "a"
        resp.append(pronoun + " " + noun)

    resp.append(random.choice(("though", "sir", "Mr.")))

    return " ".join(resp)

def check_for_comment_about_bot(pronoun, noun, adjective):
    #Check if the user is saying something about Astrobot
    resp = None
    if pronoun == 'I' and (noun or adjective):
        if noun:
            if random.choice((True,False)):
                resp = random.choice(SELF_VERBS_WITH_NOUN_CAPS_PLURAL).format(**{'noun': noun.pluralize().capitalize()})
            else:
                resp = random.choice(SELF_VERBS_WITH_NOUN_LOWER).format(**{'noun': noun})
        else:
            resp = random.choice(SELF_VERBS_WITH_ADJECTIVE).format(**{'adjective': adjective})

    return resp

# Template for responses that include a direct noun which is indefinite/uncountable
SELF_VERBS_WITH_NOUN_CAPS_PLURAL = [
    "At Astros you can buy or rent different kinds of telescopes and cameras.",
    "Our company is a pioneer in the {noun} business.",
    "I'm not sure there is a planet called {noun}.",
    "Please contact my human boss to talk about {noun}.",
]

SELF_VERBS_WITH_NOUN_LOWER = [
    "I don't know a lot about {noun}.",
    "You can ask me about the different prices we manage {noun}",
    "{noun} is not a valid discount code."
]

SELF_VERBS_WITH_ADJECTIVE = [
    "Some people say Saturn looks {adjective} when in the apogee.",
    "Astronomy is a {adjective} activity",
]
# end

def preprocess_text(sentence):
    #Preprocess the text so it is more understandable
    cleaned = []
    words = sentence.split(' ')
    for w in words:
        if w == 'i':
            w = 'I'
        if w == "i'm":
            w = "I'm"
        cleaned.append(w)
    return ' '.join(cleaned)

def respond(sentence):
    cleaned = preprocess_text(sentence)
    parsed = TextBlob(cleaned)

    pronoun, noun, adjective, verb = find_candidate_parts_of_speech(parsed)

    resp = check_for_comment_about_bot(pronoun, noun, adjective)

    if not resp:
        resp = check_for_greeting(parsed)

    if not resp:
        if not pronoun:
            resp = random.choice(NONE_RESPONSES)
        elif pronoun == 'I' and not verb:
            resp = random.choice(COMMENTS_ABOUT_SELF)
        else:
            resp = construct_response(pronoun, noun, verb)

    if not resp:
        resp = random.choice(NONE_RESPONSES)

    logger.info("Returning phrase '%s'", resp)
    filter_response(resp)

    return resp


def find_candidate_parts_of_speech(parsed):
    pronoun = None
    noun = None
    verb = None
    adjective = None
    for sent in parsed.sentences:
        pronoun = find_pronoun(sent)
        noun = find_noun(sent)
        adjective = find_adjective(sent)
        verb = find_verb(sent)
    logger.info("Pronoun = %s, Noun = %s, Adjective = %s, Verb = $s", pronoun, noun, adjective, verb)
    return pronoun, noun, adjective, verb


def filter_response(resp):
    tokenized = resp.split(' ')
    for word in tokenized:
        if '@' in word or '#' in word or '!' in word:
            raise UnnacceptableUtteranceException()
        for s in FILTER_WORDS:
            if word.lower().startswith(s):
                raise UnnacceptableUtteranceException()
