import requests, csv
from bs4 import BeautifulSoup as BS
from datetime import date

def list_to_csv(list, filename):
    filepath = 'csv/' + filename + '.csv'
    f = open(filepath, 'w', newline='')
    writer = csv.writer(f)
    writer.writerows(list)
    f.flush()
    f.close()

def get_soup(url):
    r = requests.get(url)
    html = r.text
    soup = BS(html, "html.parser")
    return soup

def get_table_as_list(table):
    headlines = table.find('thead').findAll('th')
    headline = [name.text for name in headlines]
    table_body = table.find('tbody')

    result = [headline]
    for table_row in table_body.findAll('tr'):
        columns = table_row.findAll('td')
        output_row = []
        for column in columns:
            try:
                output_row.append(column['data-value'])
            except KeyError:
                if column.find('div'):
                    output_row.append(column.find('div').text)
                else:
                    output_row.append(column.text)
        result.append(output_row)

    return result


def main(url, filename):
    today = date.today()
    day = today.strftime("%d.%m.%Y")
    url_with_date = url + '&f=01.01.2010&t=' + day
    soup = get_soup(url_with_date)
    table = soup.findAll('table')[1]
    output_list = get_table_as_list(table)

    list_to_csv(output_list, filename)

    count = 0
    # output
    for line in output_list[1:]:
        count += float(line[1])
    print('Written ', len(output_list), ' lines')
    print('Difference is : {:.2f}'.format(count))

main('https://ib.fio.cz/ib/transparent?a=2100048174','pirati')