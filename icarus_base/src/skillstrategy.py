from skills.SuperSkill import SuperSkill
from skills.BasicSkills import IDKSkill
from skills.WikipediaSkill import WikipediaSkill
from skills.WolframSkill import WolframSkill
import os
import sys
import re
import inspect
from importlib import import_module

PLUGIN_PATH: str = './skills'


class SkillStrategy:

    _skill_list = list()
    skills = dict()
    fallback_skill = None
    persistence = None
    skill_handler = None

    def __init__(self, persistence):
        self.persistence = persistence

        # load skills
        self._load_skills()
        # start skills
        self._start_skills()

        # load fallback skills
        self.fallback_skill = [WolframSkill(persistence), WikipediaSkill(persistence), IDKSkill(persistence)]

        self.skill_handler = InvertedSkillIndex()

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

                    print("Discovered Plugin \"{}\"".format(obj.name))
                    skills_dict[obj.name] = {"active": True, "creator": obj.creator, "version": obj.version}
                    self._skill_list.append(obj)
                    # self._register_plugin(obj)
        self.persistence.save_persistent_dict("SKILLS", skills_dict)

    def _register_plugin(self, plugin: SuperSkill):

        for token in plugin.tokens:
            if token in self.skills:
                self.skills[token].append(plugin)
            else:
                self.skills[token] = [plugin]

    def get_matching_skill(self, message):
        result_dict = dict()
        for token in message.get_tokens():
            if token in self.skills:
                for skill in self.skills[token]:
                    if skill not in result_dict:
                        result_dict[skill] = 1
                    else:
                        result_dict[skill] += 1

        result = self._sort_skills(result_dict)
        result += self.fallback_skill

        # get skills instead of indizes
        # for index, skill in enumerate(result):
        #    result[index] = self._skill_list[skill]

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

    # get all skills with their tokens in a list
    # get each new query
    # calculate the vector and how similar it is
    # give it a reasonable threshold


class InvertedSkillIndex:
    """A Strategy to find the respective Skill"""

    inverted_index = None
    # Looks like: "a": [[d1, 5], [d2, 8]]

    # option: für jeden satz ein abgleich oder für jeden skill [alle sätze als ein datensatz]

    def __init__(self):
        self.inverted_index = dict()
        self.phrase_skills = dict()

    def register_skill(self, skill: SuperSkill):
        """Index a new skill using call phrases"""
        for index in range(0, len(skill.phrases)):
            # todo: weight words
            phrase = self._prepare_input(skill.phrases[index])
            word_dict = self._dictionarize_phrase(phrase)
            for word in word_dict:
                tupel = [skill, index, word_dict[word]]
                if word in self.inverted_index:
                    self.inverted_index[word].append(tupel)
                else:
                    self.inverted_index[word] = [tupel]

    @staticmethod
    def _dot(A, B):
        return sum(a * b for a, b in zip(A, B))

    def _get_cos_sim(self, a, b):
        return self._dot(a, b) / ((self._dot(a, a) ** .5) * (self._dot(b, b) ** .5))

    def get_cos_sim_skills(self, user_input: str) -> list:
        """return a list of skills sorted by cos similarity"""
        # create vector from input
        user_input = self._dictionarize_phrase(self._prepare_input(user_input))
        print()
        return []

    def remove_skill(self, skill: SuperSkill):
        """removes a skill from the inverted index"""
        pass

    @staticmethod
    def _dictionarize_phrase(phrase: str):
        result = dict()
        bag_of_words = phrase.split(" ")
        for word in bag_of_words:
            if word in result:
                result[word] += 1
            else:
                result[word] = 1
        return result

    @staticmethod
    def _prepare_input(text: str) -> str:
        """removes special characters, sets everything to lower case and """
        special_characters_regex = "[^a-z|^0-9]"
        text = text.lower()
        text = re.sub(special_characters_regex, "", text)
        return text
