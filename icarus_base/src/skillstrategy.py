from skills.SuperSkill import SuperSkill
from skills.BasicSkills import IDKSkill
from skills.WikipediaSkill import WikipediaSkill
from skills.WolframSkill import WolframSkill
import os
import sys
import inspect
from importlib import import_module

PLUGIN_PATH: str = './skills'


class SkillStrategy:

    _skill_list = list()
    skills = dict()
    fallback_skill = [WolframSkill(), WikipediaSkill(), IDKSkill()]

    def __init__(self):
        # load skills
        self._load_skills()
        # start skills
        self._start_skills()

    def _start_skills(self):
        for index, skill in enumerate(self._skill_list):
            # print(str(index) + skill.name)
            # start skill
            # self._skill_list = skill()
            # hand over index for single source purposes
            self._register_plugin(skill())

    def _load_skills(self):
        """Loads all modules of the plugins package"""

        for file in os.listdir(PLUGIN_PATH):
            temp = file.rsplit('.py', 1)
            import_module('skills.' + temp[0])
            for name, obj in inspect.getmembers(sys.modules['skills.' + temp[0]]):
                if inspect.isclass(obj) and issubclass(obj, SuperSkill) and obj is not SuperSkill:

                    print("Discovered Plugin \"{}\"".format(obj.name))
                    self._skill_list.append(obj)
                    # self._register_plugin(obj)

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
    # give it a reasonable threashhold
