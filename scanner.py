import io


class Scanner(object):
    def __init__(self, tiny_code=""):
        tiny_code.encode(encoding="utf-8")
        tiny_code = tiny_code.translate(str.maketrans({"-":  r"\-",
                                                       "]":  r"\]",
                                                       "\\": r"\\",
                                                       "^":  r"\^",
                                                       "$":  r"\$",
                                                       "*":  r"\*",
                                                       ".":  r"\.",
                                                       ":":  r"\:"}))
        self.tiny_code = tiny_code
        self.tokens_list = []
        self.code_list = []

    def setTinyCode(self, tiny_code):
        tiny_code.encode(encoding="utf-8")
        self.tiny_code = tiny_code

    def scan(self):
        tokens_list = []
        for tiny_in in io.StringIO(self.tiny_code):
            token_str = ""
            special_chars = ['(', ')', '+', '-', '*', '/',
                             '=', ';', '<', '>', '<=', '>=']
            reversed_words = ["if", "then", "else",
                              "end", "repeat", "until", "read", "write"]
            state = "start"
            i = 0
            while i < len(tiny_in):
                if tiny_in[i] in special_chars and state != "inassign" and state != "incomment":
                    if (token_str != ""):
                        tokens_list.append(token_str)
                        token_str = ""
                    tokens_list.append(tiny_in[i])
                    state = "start"
                elif state == "start":
                    if tiny_in[i] == " ":
                        state = "start"
                    elif tiny_in[i].isalpha():
                        token_str += tiny_in[i]
                        state = "inid"
                    elif tiny_in[i].isdigit():
                        token_str += tiny_in[i]
                        state = "innum"
                    elif tiny_in[i] == ':':
                        token_str += tiny_in[i]
                        state = "inassign"
                    elif tiny_in[i] == '{':
                        token_str += tiny_in[i]
                        state = "incomment"
                    else:
                        state = "done"
                elif state == "inid":
                    if tiny_in[i].isalpha():
                        token_str += tiny_in[i]
                        state = "inid"
                    else:
                        state = "done"
                elif state == "innum":
                    if tiny_in[i].isdigit():
                        token_str += tiny_in[i]
                        state = "innum"
                    else:
                        state = "done"
                elif state == "inassign":
                    if tiny_in[i] == "=":
                        token_str += tiny_in[i]
                        state = "done"
                    else:
                        state = "done"
                elif state == "incomment":
                    if tiny_in[i] == "}":
                        token_str += tiny_in[i]
                        state = "start"
                    else:
                        token_str += tiny_in[i]
                elif state == "done":
                    tokens_list.append(token_str)
                    token_str = ""
                    state = "start"
                    i -= 1

                i += 1
            if (token_str != ""):
                tokens_list.append(token_str)
                token_str = ""
        tokens_output = []
        for t in tokens_list:
            if t in reversed_words:
                tokens_output.append(t)
            elif t in special_chars:
                tokens_output.append(t)
            elif t == ":=":
                tokens_output.append(t)
            elif t.isdigit():
                tokens_output.append("number")
            elif t.isalpha():
                tokens_output.append("identifier")
            else:
                pass
                # tokens_output.append("comment")
        self.code_list = tokens_list
        self.tokens_list = tokens_output

    def createOutputFile(self, filename):
        output_code = self.scan()
        with open(filename, 'w+') as out:
            out.write(output_code)
