#!/usr/bin/env python
from bs4 import BeautifulSoup
import urllib
import sys
import codecs

# Change encoding to fix a bug on windows
sys.stdout = codecs.getwriter("iso-8859-1")(sys.stdout, 'xmlcharrefreplace')

# Download a copy of the EC2 Instance Types from Amazon and scrape the content
site_content = urllib.urlopen('https://aws.amazon.com/ec2/instance-types/').read()
soup = BeautifulSoup(site_content, 'lxml')
aws_tables = soup.find_all("div", {"class": "aws-table"});

for table_div in aws_tables:
    trs = table_div.find('table').tbody.find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        rng = len(tds)
        line = ''
        if rng > 0:
            for i in range(0, rng):
                if i > 0:
                    line += ', '
                line += tds[i].get_text().strip()
            print(line)
    print('\n')
