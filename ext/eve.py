from sphinx.util.compat import Directive


class EFT(Directive):

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {}

    def run(self):
        pass
