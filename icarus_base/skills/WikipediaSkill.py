from skills.SuperSkill import SuperSkill
import re
import wikipedia


class WikipediaSkill(SuperSkill):

    name = "Wikipedia Skill"
    version = "1.0"
    creator = ""
    tokens = ["who", "what", "why", "where", "definition"]

    def main(self, message):
        search = re.sub('(who|where|what|why)( is| are)?( a | )?', '', message.msg)
        search_results = wikipedia.search(search)

        if search_results:
            page = self.get_wiki_page(search_results)
            if page:
                result = str(page.summary)
                result = result.split(".")[0]
                result = re.sub('\(.*\) ', '', result)
                message.send(result)

    def get_wiki_page(self, inputs: list, recursion_depth: int = 2):
        if recursion_depth > 0:
            recursion_depth -= 1
            try:
                page = wikipedia.page(inputs[0])
            except wikipedia.DisambiguationError as disambiguation_error:
                page = self.get_wiki_page(disambiguation_error.options, recursion_depth)

            return page
        else:
            print("maximum recursion depth reached, cannot single out a page")
            return None
