class Words:
    GREETING_KEYWORDS = ["hello", "hi", "greetings", "sup", "what's up"]
    GREETING_RESPONSES = ["'sup bro", "hey", "*nods*", "hey you get my snap?"]
    def greetings(sentence):
        for word in sentence.words():
            if(word.lower() in GREETING_KEYWORDS):
                return random.choice(GREETING_RESPONSES);

    def respond(sentence):
        #Clean the sentence
        cleaned = preprocess_text(sentence)
        parsed = TextBlob(cleaned)

        #Extract relevant parts of the sentences
        pronoun, noun, adjective, verb = find_candidate_parts_of_speech(parsed)

        #Find if the user is talking about the bot
        resp = check_for_comment_about_bot(pronoun, noun, adjective)

        #Give general greeeting response
        if not resp:
            resp = greetings(parsed)

        #If he didn't say hello
        if not resp:
            if not pronoun:
                resp = random.choice(NONE_RESPONSES)
            elif pronoun == 'I' and not verb:
                resp = construct_response(pronoun, noun, verb)

        #If the processing didnt catch anything, throw a random answer
        if not resp:
            resp = random.choice(NONE_RESPONSES)

        logger.info("Returning phrase '%s'", resp)

        #Elliminate bad words
        filter_response(resp)

        return resp

    def find_candidate_parts_of_speech(parsed):
        #Finds best pronoun, noun, verb, or adjective.
        pronoun = None
        noun = None
        adjective = None
        verb = None
        for sent in parsed.sentences:
            pronoun = find_pronoun(sent)
            noun = find_noun(sent)
            adjective = find_adjective(sent)
            verb = find_verb(sent)
        logger.info("Pronoun: %s Noun: %s Adjective: %s Verb: %s", pronoun, noun, adjective, verb)

        return pronoun, noun, adjective, verb

    def find_pronoun(sent):
        #Finds an appropiate pronoun to respond with
        pronoun = None
        for word, part_of_speech in sent.pos_tags:
            #Disambiguate pronouns
            if part_of_speech == 'PRP' and word.lower() == 'you':
                pronoun = 'I'
            elif part_of_speech == 'PRP' and word == 'I':
                pronoun = 'You'
        return pronoun

    def check_for_comment_about_bot(pronoun, noun, adjective):
        #Check if the input is about the bot
        resp = None
        if pronoun == 'I' and (noun or adjective):
            if noun:
                if random.choice((True, False)):
                    resp = random.choice(SELF_VERBS_WITH_NOUN_CAPS_PLURAL.format(**{'noun': noun.pluralize().capitalize()}))
                else:
                    resp = random.choice(SELF_VERBS_WITH_NOUN_LOWER.format(**{'noun': noun}))
            else:
                resp = random.choice(SELF_VERBS_WITH_ADJECTIVE).format(**{'adjective': adjective})
        return resp

    def construct_response(pronoun, noun, verb):
        #No special cases, trying to construct a good answer
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

        resp.append(random.choice(("tho", "bro", "lol", "bruh", "smh", "")))
        return " ".join(resp)

    def filter_response(resp):
        #Dont allow any word to match our filter list
        tokenized = resp.split(' ')
        for word in tokenized:
            if '@' in word or '#' in word or '!' in word:
                raise UnnacceptableUtteranceException()
            for s in FILTER_WORDS:
                if word.lower().startswith(s):
                    raise UnnacceptableUtteranceException()



    SELF_VERBS_WITH_NOUN_CAPS_PLURAL = [
        "My last startup totally crushed the {noun} vertical",
        "Were you aware I was a serial entrepreneur in the {noun} sector",
    ]

    SELF_VERBS_WITH_NOUN_LOWER = [
        "Yeah but I know a lot about {noun}",
        "My bros always ask me about {noun}"
    ]

    SELF_VERBS_WITH_ADJECTIVE = [
        "I'm personally building the {adjective} Economy",
        "I consider myself to be a {adjective}preneur",
    ]

    FILTER_WORDS = [
        "Perra",
        "Zorra",
        "Puto",
        "Puta",
        "Cabron",
        "Pendejo",
        "Imbecil",
        "Whore",
        "Bitch",
    ]
