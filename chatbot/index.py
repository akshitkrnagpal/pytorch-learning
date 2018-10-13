import codecs
import csv
import os


# Fields of data files
MOVIE_LINE_FIELDS = ['lineID', 'characterID', 'movieID', 'character', 'text']
MOVIE_CONVERSATIONS_FIELDS = ['character1ID', 'character2ID', 'movieID', 'utteranceIDs']

# Print contents of file
def printLines(file, n=10):
    with open(file, 'rb') as datafile:
        lines = datafile.readlines()
    for line in lines[:n]:
        print(line)

# This parses all the lines according to given fields
def loadLines(fileName, fields):
    lines = {}
    with open(fileName, 'r', encoding='iso-8859-1') as f:
        for line in f:
            values = line.split( ' +++$+++ ');
            # Extract fields
            lineObj = {}
            for i, field in enumerate(fields):
                lineObj[field] = values[i]
            lines[lineObj['lineID']] = lineObj
    return lines

# This parses all the conversations
def loadConversations(fileName, lines, fields):
    conversations = []
    with open(fileName, 'r', encoding='iso-8859-1') as f:
        for line in f:
            values = line.split(' +++$+++ ')
            # Extract fields
            convObj = {}
            for i, field in enumerate(fields):
                convObj[field] = values[i]
            lineIDs = eval(convObj['utteranceIDs'])
            convObj['lines'] = []
            for lineID in lineIDs:
                convObj['lines'].append(lines[lineID])
            conversations.append(convObj)
    return conversations

# This extract each pair of question and answer from conversations
def extractSentencePairs(conversations):
    qa_pairs = []
    for conversation in conversations:
        for i in range(len(conversation['lines']) - 1):
            inputLine = conversation['lines'][i]['text'].strip();
            targetLine = conversation['lines'][i+1]['text'].strip();
            if inputLine and targetLine:
                qa_pairs.append([inputLine, targetLine])
    return qa_pairs

# Load all the lines from data file
lines = {}
lines = loadLines(os.path.join('data', 'movie_lines.txt'), MOVIE_LINE_FIELDS)

# Load them into conversations
conversations = []
conversations = loadConversations(os.path.join('data', 'movie_conversations.txt'), lines, MOVIE_CONVERSATIONS_FIELDS)

# Generate QA pairs
qa_pairs = []
qa_pairs = extractSentencePairs(conversations)



datafile = os.path.join('formatted_movie_line.txt')

delimiter = '\t'
delimiter = str(codecs.decode(delimiter, 'unicode_escape'))

# Generate a formatted data file
with open(datafile, 'w', encoding='utf-8') as outputfile:
    writer = csv.writer(outputfile, delimiter=delimiter)
    for pair in qa_pairs:
        writer.writerow(pair)

printLines(datafile, 1)
