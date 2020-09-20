"""
    Controls Skill handling
"""

# imports
import os
import sys
from importlib import import_module
import inspect

# import used classes
from src.Persistence.persistence import Persistence
from src.SkillManagement.InvertedIndex import InvertedSkillIndex
from src.message import Context
from logger import icarus_logger

# import fallback skills
from skills.WolframSkill import WolframSkill
from skills.WikipediaSkill import WikipediaSkill
from skills.BasicSkills import SuperSkill, IDKSkill

# statics
PLUGIN_PATH: str = os.path.join('.', 'skills')


class SkillManager:
    """ Manages Skills within """

    persistence = None
    fallback_skills = None

    def __init__(self, persistence: Persistence):
        self.persistence = persistence
        self.skill_handler = InvertedSkillIndex()

        self.fallback_skills = [WolframSkill(persistence), WikipediaSkill(persistence), IDKSkill(persistence)]
        self.register_skills()

    def register_skills(self):
        """ Find skills in the skill directory and register them in the skill handler """

        # search all files in plugin path
        for file in os.listdir(PLUGIN_PATH):

            if 'py' in file:
                # import all files into python
                temp = file.rsplit('.py', 1)
                import_module('skills.' + temp[0])

                # check if any contained classes are children of "SuperSkill"
                for name, obj in inspect.getmembers(sys.modules['skills.' + temp[0]]):
                    if inspect.isclass(obj) and issubclass(obj, SuperSkill) and obj is not SuperSkill:
                        icarus_logger.debug("Discovered Plugin \"{}\"".format(obj.name))

                        # init object and hand over to indexer
                        skill = obj(self.persistence)
                        self.skill_handler.register_skill(skill)

    def find_skills(self, msg: Context):
        """ Gets an ordered list of skills and attaches them to the message """
        result = self.skill_handler.get_skills(msg.msg)     # get list of skills from the skill handler
        result += self.fallback_skills                      # attach fallback skills to the end
        msg.set_skill(result)                               # set skill list in the message
