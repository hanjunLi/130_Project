# note: python 3.6.4 used
# note: may need to adjust if other research papers have different formats
import xml.etree.ElementTree as ET
ns = '{http://www.tei-c.org/ns/1.0}'  # xml namespace

# get title and author from TEI/teiHeader/fileDesc/sourceDesc/biblStruct/analytic
# title in <title>, authors each in <author>
# input: <analytic> Element
# output: metadata dict
def metadata(analytic):
    metadata = {}
    # get title
    try:
        title = analytic.find(ns+'title').text
    except AttributeError:
        title = 'No title found'
    print('title is', title)
    metadata['title'] = title

    # get authors
    authors = ""
    for node in analytic.iter(ns+'persName'):
        forename = node.find(ns+'forename')
        try:
            authors += forename.text + ' '
        except AttributeError:
            authors += 'FirstNameUnknown '
        surname = node.find(ns+'surname')
        try:
            authors += surname.text + ', '
        except AttributeError:
            authors += 'LastNameUnknown, '
    if authors == "":
        authors = "No authors found"
    else:
        authors = authors[:-2]  # remove ', ' from last author
    print('authors are', authors)
    metadata['authors'] = authors
    print(metadata)
    return metadata

# get each track from each div in TEI/text/body
# each div has paragraphs in <p> and formulas in <formula>
# input: <body> Element
# output: tracks dict (does not include abstract yet)
def tracks(body):
    tracks = {}
    tracknum = 1

    for div in body.iter(ns+'div'):
        content = ''
        head = div.find(ns+'head')
        try:
            sec_num = head.attrib['n'] + ' '
        except (KeyError, AttributeError):
            sec_num = ''
        try:
            sec_title = head.text
        except AttributeError:
            sec_title = 'No section title'
        id = sec_num + sec_title
        print('id is', id)
        for p in div.iter(ns+'p'):  # formulas ignored for now
            content += p.text + ' '
        if content != '':
            content = content[:-1]  # take off last space
        print('content is', content)
        this_track = {}
        this_track['id'] = id
        this_track['content'] = content
        tracks[str(tracknum)] = this_track
        tracknum += 1

    print(tracks)
    return tracks


def main():
  tree = ET.parse('/Users/sherrylin/Documents/cs130/project/groupex.xml')
  root = tree.getroot()
  tracks(root.find(ns+'text').find(ns+'body'))
  metadata(root.find(ns+'teiHeader').find(ns+'fileDesc').find(ns+'sourceDesc').find(ns+'biblStruct').find(ns+'analytic'))


if __name__ == "__main__":
    main()