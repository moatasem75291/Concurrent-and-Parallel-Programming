import requests
from bs4 import BeautifulSoup


class WikipediaReader:
    def __init__(self):
        self._url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    @staticmethod
    def _extract_company_symbols(html_bage):
        soup = BeautifulSoup(html_bage, "html.parser")
        table = soup.find(id="constituents")
        table_rows = table.find_all("tr")

        for row in table_rows[1:]:
            symbol = row.find("td").text.strip()
            yield symbol

    def get_sp_500_companies(self):
        respones = requests.get(self._url)
        if respones.status_code != 200:
            print("Couldn't get data")
        else:
            print("Data was successfully downloaded")
            yield from self._extract_company_symbols(respones.text)


if __name__ == "__main__":
    reader = WikipediaReader()
    generator = reader.get_sp_500_companies()
    for i, symbol in enumerate(generator):
        print(symbol)
        if i == 7:
            break
