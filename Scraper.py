from bs4 import BeautifulSoup
import requests

def scrap():
    url = 'https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/submit-profile/rounds-invitations/results-previous.html'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    rounds_of_invitations = soup.find(class_='mwsgeneric-base-html parbase section')

    data = []
    score_list = []
    number_of_invitations_issued = []

    for tag in rounds_of_invitations.findAll('p'):
        if 'CRS score of lowest-ranked candidate invited:' in tag.getText():
            score = tag.getText().split(': ')[1]
            score_list.append(int(score))
        if 'Number of invitations issued:' in tag.getText():
            invitations = tag.getText().split(': ')[1].split('F')[0]
            number_of_invitations_issued.append(int(invitations.replace(',', '')))

    for tag in soup.findAll('table'):
        for td in tag.findAll('td'):
            if 'points' in td.getText():
                score = td.getText().split()[0]
                score_list.append(int(score))
            else:
                invitations = td.getText()
                number_of_invitations_issued.append(int(invitations.replace(',', '')))

    for index, (date, score, no_of_invitations) in enumerate(zip(rounds_of_invitations.findAll('h3'), score_list, number_of_invitations_issued)):
        extracted_date = date.getText().split(' – ')[1]
        temp_date = extracted_date.split()
        month = temp_date[0]
        day = int(temp_date[1].replace(',', ''))
        year = int(temp_date[2])

        item = Entry(index)
        cloud_id = view.add_data_to_database(month, date, year, score, invitations)
        item.add_entry(
            cloud_id = cloud_id, 
            month = month, 
            date = day,
            year = year,
            crs = score, 
            invitations = no_of_invitations
        )

        data.append({
            'month': month,
            'date': day,
            'year': year,
            'score': score,
            'no_of_invitations_issued' : no_of_invitations
        })
        
    return data
        
scraped_data = scrap()
print("Data Scraped - ", scraped_data)
