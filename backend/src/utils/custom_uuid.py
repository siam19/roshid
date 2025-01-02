import random
import string

class CustomUUID:
    def __init__(self, length, wordmark=None, dashed=True):
        self.length = length
        self.wordmark = wordmark
        self.dashed = dashed
        self.blocks = []

        # Process wordmark if provided
        if self.wordmark:
            processed_wordmark = self.wordmark.lower().replace(' ', '-')
            wordmark_blocks = processed_wordmark.split('-')
            self.blocks.extend(wordmark_blocks)
        else:
            wordmark_blocks = []

        # Ensure at least one random block for uniqueness
        num_random_blocks = max(2, self.length - len(self.blocks))

        # Generate random blocks
        for _ in range(num_random_blocks):
            block = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
            self.blocks.append(block)

        # Assemble UUID string
        if self.dashed:
            self.uuid_str = '-'.join(self.blocks)
        else:
            self.uuid_str = ''.join(self.blocks)

    def __repr__(self):
        return self.uuid_str

    def __eq__(self, other):
        if isinstance(other, CustomUUID):
            return self.uuid_str == other.uuid_str
        return False

    @classmethod
    def from_string(cls, uuid_string, dashed=True):
        if dashed:
            blocks = uuid_string.split('-')
        else:
            blocks = [uuid_string[i:i+4] for i in range(0, len(uuid_string), 4)]
        instance = cls(length=len(blocks), dashed=dashed)
        instance.blocks = blocks
        instance.uuid_str = uuid_string
        return instance