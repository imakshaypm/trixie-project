import yake
import warnings

warnings.filterwarnings('ignore')

def keywords(answer):
    probability = []
    text = answer
    kw_extractor = yake.KeywordExtractor()
    keywords = kw_extractor.extract_keywords(text)
    # for key, prob in keywords:
    #     probability.append(prob)
    # probability.sort()
    # for key, prob in keywords:
    #     if prob == probability[-1]:
    #         print(key)
    return keywords[-1]

# ans = "JavaScript is a scripting or programming language that allows you to implement complex features on web pages — every time a web page does more than just sit there and display static information for you to look at — displaying timely content updates, interactive maps, animated 2D/3D graphics, scrolling video jukeboxes, etc. — you can bet that JavaScript is probably involved. It is the third layer of the layer cake of standard web technologies, two of which (HTML and CSS) we have covered in much more detail in other parts of the Learning Area."

# keyword = keywords(ans)
# print(keyword)