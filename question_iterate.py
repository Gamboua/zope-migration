import sys
import json
from lxml import etree


def create_question_element(item):
    question = etree.Element('question', type='multichoice')

    item['title'] = item.get('title').rstrip()

    name = etree.SubElement(question, 'name')
    etree.SubElement(name, 'text').text = '<![CDATA[<p>%s</p>' % item.get('title')

    questiontext = etree.SubElement(question, 'questiontext', format='html')
    etree.SubElement(questiontext, 'text').text = '<![CDATA[<p>%s</p>' % item.get('title')

    etree.SubElement(question, 'shuffleanswert').text = 'true'
    etree.SubElement(question, 'defaultgrade').text = '1.0000000'
    etree.SubElement(question, 'answernumbering').text = 'abc'
    etree.SubElement(question, 'single').text = 'true'

    for alternative in item.get('alternatives'):
        answer = etree.SubElement(question, 'answer', fraction='100' if alternative.get('correct') else '0')
        etree.SubElement(answer, 'text').text = alternative.get('answer')

    return question


if len(sys.argv) != 2:
    print "Usage: %s <json_file>.json" % (sys.argv[0])
    sys.exit(1)

# Read json and parser to python dict array
with open(sys.argv[1], 'r') as f:
    j = json.loads(f.read())

root = etree.Element('quiz')

question_0 = etree.SubElement(root, "question", type='category')
question_0_cat = etree.SubElement(question_0, 'category')
etree.SubElement(question_0_cat, 'text').text = '$course$/$cat2$/Quiz'


for lists in j.get('cursos')[0].get('quiz').get('questions'):
    if lists:
        for item in lists:
            root.append(create_question_element(item))


with open('test.xml', 'w') as f:
    obj = etree.ElementTree(root)
    obj.write(f, pretty_print=True)