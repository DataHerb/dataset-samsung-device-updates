import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
from functools import cached_property

uri = 'https://security.samsungmobile.com/workScope.smsb'


class SamsungUpdateList:
    """List of devices that are updated and their
    cadence

    :param uri: URL of the page
    """

    def __init__(self, uri):
        self.uri = uri

    @property
    def cadence_list(self) -> list[str]:
        return ["Monthly", "Quarterly", "Biannual"]

    @cached_property
    def content(self) -> BeautifulSoup:
        page = urlopen(uri)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        contents = soup.find_all("div", {"id": "contents"})

        return contents[0]

    @cached_property
    def raw_lists(self) -> list[BeautifulSoup]:
        lists = [
            i for i in self.content.find_all("div", {"class": "txt_section"})
            if i.find("strong") and "Updates" in i.find("strong").text
        ]

        return lists

    def get_cadence_from_title(self, title: str) -> str:

        update_cadence = "No Information"
        for cadence in self.cadence_list:
            if cadence.lower() in title.lower():
                update_cadence = cadence
                break

        return update_cadence

    def parse_update_group(self, data: BeautifulSoup) -> dict:
        title_raw = data.find("strong").text
        model_lists = sum([[j.strip() for j in i.text.split(", ")]
                           for i in data.find_all("li")], [])

        return {
            "title": title_raw,
            "cadence": self.get_cadence_from_title(title_raw),
            "devlices": model_lists
        }

    @cached_property
    def parsed_updates(self) -> list[dict]:
        return [self.parse_update_group(i) for i in self.raw_lists]

    @cached_property
    def table(self) -> list[dict]:
        models = []

        for i in self.parsed_updates:
            for j in i["devlices"]:
                models.append({"cadence": i["cadence"], "model": j})

        return models


if __name__ == "__main__":

    sul = SamsungUpdateList(uri=uri)

    df = pd.DataFrame(sul.table)

    print(df)

    df.to_csv("samsung_device_updates.csv")