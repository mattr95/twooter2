import sys
import re
import os

def extractTerms(instring):
    i = 0
    terms = re.findall(r'[0-9a-zA-Z_]+|&#[0-9a-zA-Z_]+;', instring)
    while i<len(terms):
        terms[i] = terms[i].lower()
        term = terms[i]
        if (len(term) < 3) or (term[0]=='&'):
            del terms[i]
        else:
            i += 1
    terms2 = []

    # for term in terms:
    #     # ignore duplicates
    #     if not (term in terms2):
    #         terms2 += [term]

    return terms

def main():
    os.system('clear')####
    # take .xml file name as input
    argc = len(sys.argv)
    argv = sys.argv

    # open .xml file
    try:
        f = open(argv[1], "r")
    except:
        print("\nInvalid Filename!\n")
        return -1
    
    # open write files
    terms = open("terms.txt", "w")
    dates = open("dates.txt", "w")
    tweets = open("tweets.txt", "w")
    
    xml = f.read()

    status_list = xml.split("<status>")

    for status in status_list:
        begflag = '<id>'
        endflag = '</id>'
        beg = status.find(begflag) + len(begflag)
        end = status.find(endflag)

        if end == -1:
            # ignore elements without id
            continue
        
        tid = status[beg:end]

        begflag = '<created_at>'
        endflag = '</created_at>'
        beg = status.find(begflag) + len(begflag)
        end = status.find(endflag)

        date = status[beg:end]

        begflag = '<text>'
        endflag = '</text>'
        beg = status.find(begflag) + len(begflag)
        end = status.find(endflag)

        text = status[beg:end]

        begflag = '<retweet_count>'
        endflag = '</retweet_count>'
        beg = status.find(begflag) + len(begflag)
        end = status.find(endflag)

        retweets = status[beg:end]

        begflag = '<name>'
        endflag = '</name>'
        beg = status.find(begflag) + len(begflag)
        end = status.find(endflag)

        name = status[beg:end]

        begflag = '<location>'
        endflag = '</location>'
        beg = status.find(begflag) + len(begflag)
        end = status.find(endflag)

        location = status[beg:end]

        begflag = '<description>'
        endflag = '</description>'
        beg = status.find(begflag) + len(begflag)
        end = status.find(endflag)

        description = status[beg:end]

        begflag = '<url>'
        endflag = '</url>'
        beg = status.find(begflag) + len(begflag)
        end = status.find(endflag)

        url = status[beg:end]

        # terms.txt: [flag]-[term]:[tid]
        #       term len >= 3

        # write terms from text
        terms_list = extractTerms(text)
        flag = 't'
        for t in terms_list:
            terms.write('{}-{}:{}\n'.format(flag, t, tid))
        
        # write terms from name
        terms_list = extractTerms(name)
        flag = 'n'
        for t in terms_list:
            terms.write('{}-{}:{}\n'.format(flag, t, tid))

        # write terms from location
        terms_list = extractTerms(location)
        flag = 'l'
        for t in terms_list:
            terms.write('{}-{}:{}\n'.format(flag, t, tid))

        # dates.txt: [date]:[tid]
        dates.write('{}:{}\n'.format(date, tid))

        # tweets.txt
        tweets.write('{}:<status> <id>{}</id> <created_at>{}</created_at> <tex'
            't>{}</text> <retweet_count>{}</retweet_count> <user> <name>{}</na'
            'me> <location>{}</location> <description>{}</description> <url>{}'
            '</url> </user> </status>\n'.format(tid, tid, date, text, retweets, name, location, description, url))

        # ATTRIBUTES:
        # tid, date, text, retweets, name, location, description, url

if __name__ == '__main__':
    main()