import re

__all__ = ("run", "evaluate")

opening = "[{("
closing = "]})"

regexps = (r"^\s*", r"^\w+", r"^\s*-\s*")
args_re = (r"^\b+", r"^\s*:\s*")

def split_with(string, delimiter):
    not_quoted = out_quotes(string)
    sep_positions = []

    for pos in not_quoted:
        if string[pos] == delimiter:
            sep_positions.append(pos)

    split = [""]
    for i in range(len(string)):
        if i in sep_positions:
            split.append("")
        else: #Skips semicolons
            split[-1] += string[i]
    return split

def tokenise(string):
    
##    parts = []
##    for regex in regexps:
##        found = re.findall(regex, string)
##        parts.append(found[0] if len(found) == 1 else "")
##        string = string[len(parts[-1]):]
##    print(parts)
    not_quoted = out_quotes(string) #Remove all text in quotation marks and apostrophes
    stripped = "" #Spaces removed
    for i in range(len(string)):
        if string[i] == " ":
            if not i in not_quoted:
                stripped += string[i]
        else:
            stripped += string[i]
    string = stripped

    separated = split_with(string, ";")
    for i in range(len(separated)):
        separated[i] = split_with(separated[i], ":")
        separated[i][0] = list(split_with(separated[i][0], ","))
    return separated

def method(multi_key_dict, obj, key):
    type_ = type(obj)
    for k_tuple in multi_key_dict.keys():
        evaluated = tuple(map(eval, k_tuple))
        if type_ in evaluated:
            return multi_key_dict[k_tuple]
    raise KeyError("Key '{}' not found".format(key))

def out_quotes(string):
    indexes = [i for i in range(len(string)) if string[i] == '"']
    inside = []
    iterate = tuple(range(0, len(indexes), 2))
    for i in iterate:
        inside += tuple(range(indexes[i], indexes[i + 1] + 1))
    outside = [i for i in range(len(string)) if not i in inside]
    return outside

def unpack(tokens):
        individual = {}
        for i in range(len(tokens)):
            for x in range(len(tokens[i][0])):
                individual[tokens[i][0][x]] = tokens[i][1]
        return individual

def run(dict_, obj):
    for k, v in dict_.items():
        if eval(k) == type(obj):
            return eval(v)

if __name__ == "__main__":
    split = unpack(tokenise('Foo: obj.num; int, float: obj; str: "You are: "  + obj'))
    class Foo:
        def __init__(self):
            self.num = 10
    
    foo = Foo()
    print(split)
    print(run(split, foo))
