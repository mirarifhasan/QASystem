import spacy
import warnings
import gspread
from oauth2client.service_account import ServiceAccountCredentials

warnings.filterwarnings("ignore", message=r"\[W008\]", category=UserWarning)

# lang = 'en_vectors_web_lg'
lang = 'en_core_web_lg'
# lang = 'en_core_web_md'
# lang = 'en_core_web_sm'
# lang = 'en'

minSimilarity = 0.40

nlp = spacy.load(lang)
merge_nps = nlp.create_pipe("merge_noun_chunks")
nlp.add_pipe(merge_nps)

prefix = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX dbo:<http://dbpedia.org/ontology/>
            PREFIX res:<http://dbpedia.org/resource/> """

# DBs
TABLE_PHRASE = 'phrase'
TABLE_KEYWORD = 'keyword'
TABLE_RELATION = 'relation'

COLUMN_ID = 'id'
COLUMN_PHRASE = 'phrase'
COLUMN_KEYWORD = 'keyword'
COLUMN_PHRASE_ID = 'phraseId'
COLUMN_KEYWORD_ID = 'keywordId'
COLUMN_RELATION_ID = 'relationId'

# Google Sheet for Log
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
quesGSheet = client.open("Code Behaviours").worksheet('Code_InputQ')
logsGSheet = client.open("Code Behaviours").worksheet('Code_Logs')
