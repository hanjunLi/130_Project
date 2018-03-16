# note: python 3.6.4 used
import xml.etree.ElementTree as ET
import json
from collections import OrderedDict
import re

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
        title = 'no title found'
    # print('title is', title)
    metadata['title'] = title

    # get authors
    authors = ""
    for node in analytic.iter(ns + 'persName'):
        # there may be 2 forenames (one is a middle name), so use for and iter()
        authors_forename = ''
        for forename in node.iter(ns + 'forename'):
            try:
                authors_forename += forename.text + ' '
            except AttributeError:
                authors_forename += 'ForenameUnknown '
        if authors_forename == '':
            authors_forename = 'ForenameUnknown '
        authors += authors_forename
        surname = node.find(ns + 'surname')
        try:
            authors += surname.text + ', '
        except (AttributeError, TypeError):
            authors += 'LastNameUnknown, '
    if authors == "":
        authors = "no authors found"
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

    abs_p = handle_div(abs_elem)

    abs_track["id"] = "Abstract"
    abs_track["content"] = abs_p
    return abs_track


# helper function for get_abstract and get_tracks
# contains duplicate code for handling a single <div> or <abstract>
def handle_div(div):
    content = ""
    for elem in div.iter():
        tag = elem.tag
        if tag == ns + 'ref':
            content += elem.text + ' '
            if elem.tail is not None:
                content += str.replace(elem.tail, '- ', '') + ' '
        elif tag == ns + 'p':
            content += '\n' + str.replace(elem.text, '- ', '')
        elif tag == ns + 'formula':
            content += ' [math] '
    if content == '':
        content = "No content found"
    else:  # remove extra spaces
        content = content.strip()
        content = re.sub(' +', ' ', content)
        content = str.replace(content, ' ,', ',')
        content = str.replace(content, '( ', ' (')
        content = str.replace(content, ' )', ')')
        content = str.replace(content, ' .', '.')
        content = str.replace(content, ' ;', ';')
        content = str.replace(content, ' :', ':')
    return content


# get each track from each div in TEI/text/body
# input: <body> Element
# output: tracks OrderedDict (first two tracks missing)
def get_tracks(body):
    tracks = OrderedDict()
    tracknum = 3  # 1 should be "title and authors"; 2 should be "abstract"

    for div in body.iter(ns + 'div'):
        head = div.find(ns + 'head')
        try:
            sec_num = head.attrib['n'] + ' '
        except (KeyError, AttributeError, TypeError):
            sec_num = ''
        try:
            sec_title = head.text
            my_id = sec_num + sec_title
        except (AttributeError, TypeError):
            my_id = sec_num + 'No section title'
        # print('id is', my_id)
        content = handle_div(div)
        # print('content is ' + content)
        this_track = OrderedDict()
        this_track['id'] = my_id
        this_track['content'] = content
        tracks[str(tracknum)] = this_track
        tracknum += 1
    return tracks


# constructs the final output and returns a json string
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
    title_and_authors['id'] = 'Title and Authors'
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
    json_str = xml_parser(proj_dir + "/test/3.pdf.tei.xml")
    decoded = bytes(json_str, "utf-8").decode("unicode_escape")
    print(decoded)
    f = open(proj_dir + 'test/3.json', 'w+')
    f.write(decoded)
    f.close()
    g = open(proj_dir + 'test/3json.json', 'w+')
    g.write(json_str)
    g.close()


if __name__ == "__main__":
    main()
