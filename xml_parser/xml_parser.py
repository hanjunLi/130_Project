# note: python 3.6.4 used
# note: may need to adjust if other research papers have different formats
import xml.etree.ElementTree as ET
import json
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
    #print('title is', title)
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
    #print('authors are', authors)
    metadata['authors'] = authors

    json_str = json.dumps(metadata, indent=4)
    print(json_str)

    #this few lines do not seem to work, no data appearing in data.json
    with open('data.json', 'w') as f:
        f.write(json.dumps(metadata, indent=4))

    #print(metadata)
    return json_str

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
        #print('id is', id)
        for p in div.iter(ns+'p'):  # formulas ignored for now
            content += p.text + ' '
        if content != '':
            content = content[:-1]  # take off last space
        #print('content is', content)
        this_track = {}
        this_track['id'] = id
        this_track['content'] = content
        tracks[str(tracknum)] = this_track
        tracknum += 1

    #print(tracks)
    json_str = json.dumps(tracks, indent=4, sort_keys = True, ensure_ascii=True)
    '''
    with open('data.json', 'w') as f:
        f.write(json.dumps(tracks, sort_keys = True, ensure_ascii=True))
    '''
    print(json_str)
    return json_str


def main():
  tree = ET.parse('test1.pdf.tei.xml')
  root = tree.getroot()
  #print(root.tag)
  #print(root.find('body'))
  #tracks(root.find('body'))
  '''
  output = {}
  output['tracks']=tracks(root.find(ns+'text').find(ns+'body'))
  output['metadata']=metadata(root.find(ns+'teiHeader').find(ns+'fileDesc').find(ns+'sourceDesc').find(ns+'biblStruct').find(ns+'analytic'))
  '''
  b =tracks(root.find(ns+'text').find(ns+'body'))
  a =metadata(root.find(ns+'teiHeader').find(ns+'fileDesc').find(ns+'sourceDesc').find(ns+'biblStruct').find(ns+'analytic'))

  

if __name__ == "__main__":
    main()