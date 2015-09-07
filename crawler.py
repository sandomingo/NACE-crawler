__author__ = 'sandomingo'
from bs4 import BeautifulSoup
from bs4 import Tag
import urllib2
import sys
import os


class NPeople(object):
    def __init__(self):
        self.name = ''
        self.company = ''
        self.position = ''
        self.address = ''
        self.phone = ''
        self.fax = ''
        self.email = ''
        self.website = ''

    def __str__(self):
        return "Name:%s, Company:%s, Position:%s, Address:%s, Phone:%s, Fax:%s, Email:%s, Website:%s" % (
            self.name, self.company, self.position, self.address, self.phone, self.fax, self.email, self.website
        )

    def to_string(self):
        return self.__str__()


dlist = [1, 2, 21, 22, 23, 24, 25, 26, 27, 28, 29, 3, 30, 31, 32, 33, 34,
         35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
         51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 63]


dlist_name_map = {54: "Audio:Visual",
                  31: "Business:Industry Catering",
                  1: "Caterer",
                  36: "Catering Equipment",
                  34: "Chef",
                  24: "Clu: Private:Country",
                  55: "Computer:Software",
                  25: "Convention Center",
                  42: "Corporate Event Planner",
                  59: "Custom Printing",
                  40: "Destination Management Company",
                  48: "Entertainment (DJ:Band:etc.)",
                  51: "Event Equipment Rentals",
                  52: "Event Furnishings:Decor",
                  3: "Event Planner",
                  39: "Event Venue",
                  47: "Florist",
                  35: "Food Supply",
                  29: "Hospital Catering",
                  60: "Hospitality Staffing Services",
                  26: "Hotel:Resort Catering",
                  46: "Ice Sculpture",
                  27: "Kosher Catering",
                  53: "Lighting",
                  58: "Marketing:Publications",
                  41: "Meeting:Conference Planner",
                  2: "Member - All put here on import.",
                  56: "Ministerial Services",
                  43: "Non-profit Planner",
                  28: "Off-Premise Catering",
                  63: "Other",
                  49: "Photography",
                  33: "Restaurant",
                  21: "School:University Catering",
                  22: "School:University Faculty",
                  23: "School:University Staff:Administration",
                  32: "Social Event Catering",
                  44: "Special Event Planner",
                  37: "Specialty Beverages",
                  38: "Specialty Desserts",
                  61: "Specialty Linen",
                  30: "Sports Arena Catering",
                  57: "Transportation",
                  50: "Videography",
                  45: "Wedding Planner",
                  }

base_url = "http://www.nace.net/af_memberdirectory.asp?keyword=&intpage=1&page=1&action=n&dlist=54"
# custom url can custom 3 item: intpage, action & dilst
custom_url = "http://www.nace.net/af_memberdirectory.asp?keyword=&intpage=%d&page=1&action=%s&dlist=%d"


def get_page_url(page_num, category_num):
    if page_num == 1:
        return custom_url % (1, "f", category_num)
    else:
        return custom_url % (page_num - 1, "n", category_num)


def crawl(category_num, output, start_page_num=1):
    """
    crawl each category's data, output each the data to the output file
    :param ditem: item in dlist
    """
    with open(output, 'w') as out:
        page_num = start_page_num
        last_result_string = ""
        while True:
            url = get_page_url(page_num, category_num)
            resp = urllib2.urlopen(url).read()
            print "Crawl pageNum:%d, categoryNum:%d, url:%s" % (page_num, category_num, url)

            result = parse_html(resp)
            result_string_list = []
            for one in result:
                result_string_list.append(one.to_string())
            result_string = "\n".join(result_string_list)
            if last_result_string == result_string:
                break
            last_result_string = result_string
            # print last_result_string
            out.write(last_result_string.encode("utf-8"))
            out.write("\n")
            page_num += 1


def parse_html(html_doc):
    """
    Parse the response html code to a json object
    :param html_doc: the response html code
    :return: the parsed npeople object list
    """
    result = []
    soup = BeautifulSoup(html_doc, 'html.parser')
    tables = soup.find_all("table", id="Table3")
    # each table contains at most one people's info
    for table in tables:
        npeople = NPeople()
        table_str = '\n'.join(table.td.strings)
        # skip non-people info table
        if 'First' in table_str and 'Back' in table_str and 'Next' in table_str and 'Last' in table_str:
            continue
        for content in table.td:
            if isinstance(content, Tag):
                if content.font is not None:
                    if content.font['size'] == "3":
                        npeople.company = content.font.string
                    elif content.font['size'] == "2":
                        npeople.name = content.font.string
                if content.i is not None:
                    npeople.position = content.i.string
        # people's address consists of several parts
        address_list = []
        next_line_type = None
        for line in table_str.split("\n"):
            line = line.strip()
            if len(line) == 0:
                continue
            if next_line_type is not None:
                if next_line_type == "Email":
                    npeople.email = line
                elif next_line_type == "Website":
                    npeople.website = line
                next_line_type = None
                continue
            if line == npeople.name or line == npeople.position or line == npeople.company:
                continue
            if line.startswith("Phone"):
                npeople.phone=line[6:]
            elif line.startswith("Fax"):
                npeople.fax = line[4:]
            elif line.startswith("Email"):
                next_line_type = "Email"
            elif line.startswith("Website"):
                next_line_type = "Website"
            else:
                address_list.append(line)
        npeople.address = ",".join(address_list)
        result.append(npeople)
    return result


def print_usage():
    print "Usage: python crawler.py category_num output start_page_num"


def rename_files():
    """
    for debug and data exchange only.
    """
    for i in dlist:
        filename = "/Users/sandomingo/Workbench/san-wb/NACE-crawler/info/%d.txt" % i
        newfilename = "/Users/sandomingo/Workbench/san-wb/NACE-crawler/info/%s.txt" % dlist_name_map[i]
        if os.path.isfile(filename):
            os.renames(filename, newfilename)
        else:
            print "File does not exist: %s" % filename


# rename_files()

if __name__ == '__main__':
    argvs = sys.argv
    if len(argvs) == 4:
        category_num = int(argvs[1])
        output = argvs[2]
        start_page_num = int(argvs[3])
        print "Start to deal with category: %d, start from Page: %d" % (category_num, start_page_num)
        crawl(category_num, output, start_page_num)
    else:
        print_usage()


