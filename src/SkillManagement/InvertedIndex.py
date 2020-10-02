"""
    Inverted Index to calculate cosine similarity
"""

from skills.SuperSkill import SuperSkill
from src.logger import icarus_logger
import re

STOPWORDS = []      # here can be words which should be ignored


class InvertedSkillIndex:
    """A Strategy to find the respective Skill"""

    index: dict = None              # is: [hash]: [vector_dict]
    skill_map: dict = None          # is: [hash]: [[skill, token_id]]
    inverted_index: dict = None     # is: [word]: [hashlist]

    threshold = 0.65                # minimal similarity rating to appear in the result list

    # option: für jeden satz ein abgleich oder für jeden skill [alle sätze als ein datensatz]

    def __init__(self):
        self.index = dict()
        self.skill_map = dict()
        self.inverted_index = dict()

    def register_skill(self, skill: SuperSkill):
        """Index a new skill using call phrases"""
        # add IDF calculation: log(N/df)
        for index in range(0, len(skill.phrases)):
            # todo: weight words
            hash_val = hash((skill, index))
            icarus_logger.debug(str(hash_val) + ": " + skill.name)
            word_dict = self._dictionarize_phrase(self._prepare_input(skill.phrases[index]))
            self.index[hash_val] = word_dict
            self.skill_map[hash_val] = [skill, index]
            for key in word_dict.keys():
                if key in self.inverted_index:
                    self.inverted_index[key].append(hash_val)
                else:
                    self.inverted_index[key] = [hash_val]

    @staticmethod
    def _dot(A, B):
        """ matrix multiplication """
        return sum(a * b for a, b in zip(A, B))

    def _get_cos_sim(self, a, b):
        """ calculates cosinus similarity for two lists"""
        return self._dot(a, b) / ((self._dot(a, a) ** .5) * (self._dot(b, b) ** .5))

    def get_skills(self, user_input: str) -> list:
        """return a list of skills sorted by cos similarity"""
        # create vector from input
        user_input = self._dictionarize_phrase(self._prepare_input(user_input))
        # get all relevant tokens
        relevant_phrases = []
        for word in user_input.keys():  # get values of dict
            if word in self.inverted_index:
                relevant_phrases = relevant_phrases + self.inverted_index[word]
        unique_relevant_phrases = []
        [unique_relevant_phrases.append(x) for x in relevant_phrases if x not in unique_relevant_phrases]
        results = []
        # build vectors and immediately do cosine similarity
        for phrase in unique_relevant_phrases:
            vector = []
            for word in user_input.keys():
                if word in self.index[phrase]:
                    vector.append(self.index[phrase][word])
                else:
                    vector.append(0)
            cos_sim = self._get_cos_sim(user_input.values(), vector)
            if cos_sim > self.threshold:
                results.append((phrase, cos_sim))

        # sort list of tupels
        results.sort(key=lambda tup: tup[1], reverse=True)
        icarus_logger.debug(results)
        for x in range(0, len(results)):
            results[x] = self.skill_map[results[x][0]][0]  # get skill for hash and overwrite existing
        return results

    def remove_skill(self, skill: SuperSkill):
        """removes a skill from the inverted index"""
        pass

    @staticmethod
    def _dictionarize_phrase(phrase: str) -> dict:
        result = dict()
        bag_of_words = sorted(phrase.split(" "))
        for word in bag_of_words:
            if word in result:
                result[word] += 1
            elif word not in result and word not in STOPWORDS:
                result[word] = 1
        return result

    @staticmethod
    def _prepare_input(text: str) -> str:
        """removes special characters and sets everything to lower case """
        special_characters_regex = "[^a-z|^0-9|^ ]"
        text = text.lower()
        text = re.sub(special_characters_regex, "", text)
        return text