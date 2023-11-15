# // ---------------------------------------------------------------------
# // ------- [Quote Bot] Quotes Helpers
# // ---------------------------------------------------------------------

# // ---- Functions
def pathSafeName(name: str):
    return name.replace(" ", "").replace("\\", "").replace("/", "").lower()

def clamp(num: float|int, min: float|int, max: float|int):
    if num < min:
        return min
    
    if num > max:
        return max
    
    return num

def truncate(text: str, maxLength: int, ending: str = "..."):
    if len(text) <= maxLength:
        return text
    
    return text[:maxLength - len(ending)] + ending