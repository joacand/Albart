#! py -3

from bs4 import BeautifulSoup
import urllib.request
import os
import json


class GoogleImageDownloader:
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                          'Chrome/43.0.2357.134 Safari/537.36'

    def download_image(self, image_query, output_path, file_name):
        image_query = '+'.join(image_query.split())
        url = "https://www.google.com/search?q=" + image_query + "&source=lnms&tbm=isch"
        soup = self._get_soup(url, {'User-Agent': self.user_agent})

        soup_finding = soup.find("div", {"class": "rg_meta"})
        try:
            img_url, file_type = json.loads(soup_finding.text)["ou"], json.loads(soup_finding.text)["ity"]
        except AttributeError as e:
            print('Could not find result for %s. Error: %s' % (image_query, e))
            return False

        try:
            req = urllib.request.Request(img_url)
            req.add_header('User-Agent', self.user_agent)
            raw_img = urllib.request.urlopen(req).read()

            if len(file_type) == 0:
                file_to_open = os.path.join(output_path, file_name + ".jpg")
            else:
                file_to_open = os.path.join(output_path, file_name + "." + file_type)

            with open(file_to_open, 'wb') as f:
                f.write(raw_img)

        except urllib.request.URLError as e:
            print('Could not load (URLError) %s. Error: %s' % (img_url, e))
            return False
        except (OSError, IOError) as e:
            print('Could not write image (OSError or IOError) %s. Error: %s' % (img_url, e))
            return False

        return True

    @staticmethod
    def _get_soup(url, header):
        return BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url, headers=header)), 'html.parser')
