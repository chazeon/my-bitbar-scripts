from typing import List
import textwrap

class BitBarMessage:

    # content: str
    # attrs: dict

    def __init__(self, content, attrs=None):
        self.content = content
        self.attrs = attrs if attrs else {}

    @property
    def _parts(self):
        return [self.content] + [f"{key}={val}" for key, val in self.attrs.items()]

    def __str__(self):
        return self.content if len(self.attrs) == 0 else "%s|%s" % (
            self.content,
            " ".join([f"{key}={val}" for key, val in self.attrs.items()])
        )

class BitBarMessageParent(BitBarMessage):

    # children: List[BitBarMessage] = None

    def __init__(self, content, attrs=None, children=None):
        super().__init__(content, attrs=attrs)
        self.children = children if children else []

    def append(self, *args, **argv):
        if isinstance(args[0], BitBarMessage):
            self.children.append(args[0])
        else:
            self.children.append(BitBarMessage(*args, **argv))
    
    def extend(self, others: List[BitBarMessage]):
        self.children.extend(others)
    
    def __str__(self):
        return "%s\n%s" % (
            super().__str__(),
            textwrap.indent("\n".join(str(child) for child in self.children), "--")
        )


class BitBarMessagePack:

    # title: List[BitBarMessage]
    # messages: List[BitBarMessage]

    def __init__(self, title: str, attrs=None, messages=None):
        self.title = title
        self.attrs = attrs if attrs else {}
        self.messages = messages if messages else []
    
    def append(self, *args, **argv):
        if isinstance(args[0], BitBarMessage):
            self.messages.append(args[0])
        else:
            self.messages.append(BitBarMessage(*args, **argv))

    def __str__(self):
        return "%s\n---\n%s" % (
            self.title,
            "\n".join(str(msg) for msg in self.messages)
        )
