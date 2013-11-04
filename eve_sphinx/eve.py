from docutils import nodes
from sphinx.util.compat import Directive


from utils import eft2dna


class eft(nodes.General, nodes.Element):
    pass


class EFT(Directive):

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {}

    def run(self):
        node = eft()
        node['eft'] = '\n'.join(self.content)
        node['dna'] = eft2dna(node['eft'])
        return [node]
