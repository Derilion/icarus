from skills.SuperSkill import SuperSkill
from skills.BasicSkills import IDKSkill
from skills.WikipediaSkill import WikipediaSkill
from skills.WolframSkill import WolframSkill
import os
import sys
import re
import inspect
from importlib import import_module
from logger import icarus_logger

PLUGIN_PATH: str = os.path.join('.', 'skills')
STOPWORDS = []  # ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]


class SkillStrategy:

    _skill_list = list()
    skills = dict()
    fallback_skills: list = None
    persistence = None
    skill_handler = None

    def __init__(self, persistence):
        self.persistence = persistence

        self.skill_handler = InvertedSkillIndex()

        # load skills
        self._load_skills()
        # start skills
        self._start_skills()

        # load fallback skills in Order
        self.fallback_skills = [WolframSkill(persistence), WikipediaSkill(persistence), IDKSkill(persistence)]

    def _start_skills(self):
        for index, skill in enumerate(self._skill_list):
            # print(str(index) + skill.name)
            # start skill
            # self._skill_list = skill()
            # hand over index for single source purposes
            self._register_plugin(skill(self.persistence))

    def _load_skills(self):
        """Loads all modules of the plugins package"""
        skills_dict = dict()
        for file in os.listdir(PLUGIN_PATH):
            temp = file.rsplit('.py', 1)
            import_module('skills.' + temp[0])
            for name, obj in inspect.getmembers(sys.modules['skills.' + temp[0]]):
                if inspect.isclass(obj) and issubclass(obj, SuperSkill) and obj is not SuperSkill:

                    icarus_logger.debug("Discovered Plugin \"{}\"".format(obj.name))
                    skills_dict[obj.name] = {"active": True, "creator": obj.creator, "version": obj.version}
                    self._skill_list.append(obj)

    def _register_plugin(self, plugin: SuperSkill):
            self.skill_handler.register_skill(plugin)

    def get_matching_skill(self, message):
        result = self.skill_handler.get_skills(message.msg)
        result += self.fallback_skills

        message.set_skill(result)

        return

    @staticmethod
    def _sort_skills(skills: dict):
        """
        returns a sorted list of the dictionary skills
        :param skills: dictionary with skill - match value tupels
        :return:
        """
        results = list()
        for skill in skills:
            i = 0
            while i < len(results):
                if skills[skill] > skills[results[i]]:
                    results.insert(i, skill)
                    # killing loop w/o break, also suggests successful match
                    i = len(results)
                i += 1
            # len results + 1 would suggest a match was found, if the loop just ended no match was found
            if i < len(results) + 1:
                results.append(skill)
        return results

    def install_skill(self, file_handle) -> int:
        # copy files
        # install requirements
        # add to database
        pass

    def deactivate_skill(self, skill_id):
        # database set deactivated
        pass

    def activate_skill(self, skill_id):
        # database set activated
        pass

    def delete_skill(self, skill_id):
        # database set removed
        # remove files
        pass


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
    def _dictionarize_phrase(phrase: str):
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
