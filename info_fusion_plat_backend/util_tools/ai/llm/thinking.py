class Thinking:
    """Agent的思考方式
    """

    def __init__(
            self,
            thinking_type
        ):
        self.thinking_type = thinking_type

    class types:
        OPENAI_GPT3 = 'openai_gpt3'
        DEFAULT = OPENAI_GPT3