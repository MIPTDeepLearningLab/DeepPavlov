from deeppavlov.core.common.registry import register
from deeppavlov.core.models.inferable import Inferable


@register("dummy")
class DummySkill(Inferable):
    def __init__(self, vocab_path=None):
        pass

    def infer(self, instance):
        return 'Hello, my name is Kaspar Hauser'

    def reset(self):
        pass
