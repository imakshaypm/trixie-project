import docx2txt
import yake
import spacy
import warnings
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

warnings.filterwarnings('ignore')

def resumes(resumes, jobs):
    resume = docx2txt.process(resumes)
    job = docx2txt.process(jobs)

    text = resume

    kw_extractor = yake.KeywordExtractor()
    keywords = kw_extractor.extract_keywords(text)
        
    text = [resume,job]

    cv = CountVectorizer()
    count_matrix = cv.fit_transform(text)

    matchpercentage = cosine_similarity(count_matrix)[0][1]
    matchpercentage = round(matchpercentage*100,2)
    return matchpercentage