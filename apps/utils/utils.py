
def toMoney(val) -> str:
    l = str(val).split(".")
    start = l[0]
    if len(l) == 1: return [start,"00"]
    end =  l[1]
    if len(end) == 1: end += "0"
    return f"{start}.{end}"