# note: python 3.6.4 used
# note: may need to adjust if other research papers have different formats
import xml.etree.ElementTree as ET
import json
from collections import OrderedDict
import os

ns = '{http://www.tei-c.org/ns/1.0}'  # xml namespace
proj_dir = '/Users/sherrylin/130_Project/'


# get title and author from TEI/teiHeader/fileDesc/sourceDesc/biblStruct/analytic
# input: <analytic> Element
# output: metadata OrderedDict
def get_metadata(analytic):
    metadata = OrderedDict()
    # get title
    try:
        title = analytic.find(ns + 'title').text
    except AttributeError:
        title = 'No title found'
    # print('title is', title)
    metadata['title'] = title

    # get authors
    authors = ""
    for node in analytic.iter(ns + 'persName'):
        forename = node.find(ns + 'forename')
        try:
            authors += forename.text + ' '
        except AttributeError:
            authors += 'FirstNameUnknown '
        surname = node.find(ns + 'surname')
        try:
            authors += surname.text + ', '
        except AttributeError:
            authors += 'LastNameUnknown, '
    if authors == "":
        authors = "No authors found"
    else:
        authors = authors[:-2]  # remove ', ' from last author
    # print('authors are', authors)
    metadata['authors'] = authors
    return metadata


# get abstract from TEI/teiHeader/profileDesc/abstract
# input: <abstract> Element
# output: abstract OrderedDict(track 2)
def get_abstract(abs_elem):
    abs_track = OrderedDict()
    abs_p = ""

    for elem in abs_elem.iter():
        tag = elem.tag
        if tag == ns + 'ref':
            abs_p += elem.text + ' '
            if elem.tail is not None:
                if not elem.tail.isspace():  # don't add if tail is just whitespace
                    abs_p += str.replace(elem.tail, '- ', '') + ' '
        elif tag == ns + 'p':
            abs_p += '\n' + str.replace(elem.text, '- ', '')
        elif tag == ns + 'formula':
            abs_p += '[math] '
    if abs_p == "":
        abs_p = "No abstract found"
    else: # remove last space and first newline
        if abs_p[0] == '\n':
            abs_p = abs_p[1:]
        if abs_p[-1] == ' ':
            abs_p = abs_p[:-1]
    abs_track["id"] = "abstract"
    abs_track["content"] = abs_p
    return abs_track


# get each track from each div in TEI/text/body
# input: <body> Element
# output: tracks OrderedDict (first two tracks missing)
def get_tracks(body):
    tracks = OrderedDict()
    tracknum = 3  # 1 should be "title and authors"; 2 should be "abstract"

    for div in body.iter(ns + 'div'):
        content = ""
        head = div.find(ns + 'head')
        try:
            sec_num = head.attrib['n'] + ' '
        except (KeyError, AttributeError):
            sec_num = ''
        try:
            sec_title = head.text
        except AttributeError:
            sec_title = 'No section title'
        my_id = sec_num + sec_title
        # print('id is', my_id)
        for elem in div.iter():  # should handle references and formulas
            tag = elem.tag
            if tag == ns + 'ref':
                content += elem.text + ' '
                if elem.tail is not None:
                    if not elem.tail.isspace():  # don't add if tail is just whitespace
                        content += str.replace(elem.tail, '- ', '') + ' '
            elif tag == ns + 'p':
                content += '\n' + str.replace(elem.text, '- ', '')
            elif tag == ns + 'formula':
                content += '[math] '
        if content == '':
            content = "No content found"
        else:  # remove last space and first newline
            if content[0] == '\n':
                content = content[1:]
            if content[-1] == ' ':
                content = content[:-1]
        # print('content is', content)
        this_track = OrderedDict()
        this_track['id'] = my_id
        this_track['content'] = content
        tracks[str(tracknum)] = this_track
        tracknum += 1
    return tracks

def xml_parser(file_name, xml_str=''):
    if not xml_str:
        tree = ET.parse(file_name)
        root = tree.getroot()
    else:
        root = ET.fromstring(xml_str)
        
    output = OrderedDict()

    metadata = get_metadata(
        root.find(ns + 'teiHeader').find(ns + 'fileDesc').find(ns + 'sourceDesc').find(ns + 'biblStruct').find(
            ns + 'analytic'))
    tracks = get_tracks(root.find(ns + 'text').find(ns + 'body'))

    # add "title and authors", "abstract" sections to tracks OrderedDict
    title_and_authors = OrderedDict()
    title_and_authors['id'] = 'title and authors'
    title_and_authors['content'] = metadata['title'] + ' by ' + metadata['authors']

    tracks['1'] = title_and_authors
    tracks['2'] = get_abstract(root.find(ns + 'teiHeader').find(ns + 'profileDesc').find(ns + 'abstract'))
    tracks.move_to_end('2', last=False)  # move tracks 1,2 to the beginning
    tracks.move_to_end('1', last=False)
    output['metadata'] = metadata
    output['tracks'] = tracks

    json_str = json.dumps(output, indent=2)
    return json_str


def main():
    json_str = xml_parser(proj_dir + "/test/4_short.pdf.tei.xml")
    decoded = bytes(json_str, "utf-8").decode("unicode_escape")
    print(decoded)
    f = open(proj_dir + 'test/test.json', 'w+')
    f.write(decoded)
    f.close()
    g = open(proj_dir + 'test/json.json', 'w+')
    g.write(json_str)
    g.close()



if __name__ == "__main__":
    main()
