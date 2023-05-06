from bs4 import BeautifulSoup
from google.cloud import storage
from google.oauth2 import service_account
import requests

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

credentials_dict = {
    "type": "service_account",
    "project_id": "projeto-espm-dataops",
    "private_key_id": "833d1340e13193a4ecc950a10eaa460b62a66c7f",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCnNw2uFYIEfLyo\naUg9DxcVxI+zzcvB3ZmaLc7PYMm7TBmjSEJfW1l/+DkznVXC0VqJQq7zPZzXypwv\naxogY/01BAQuUupTfRHU9wUFWh9nMYukemBz79rAcW9Q4AX5EbqzpuKK5902x0jA\nB/6X8l9Lyj0/9mPamzFKKtFrZg3s7EiYsfplRtPj0MK3iDycsI0AhyjT/3jLYDXC\nLembg07rReLvntfHBLOLT5dkaARjhOnPX/G0lbfdwIWIJfe6VaOkF7yPWpMfWwqT\nwCillRezVR0K7Zyb4+Ug7KNrX9tDP3tAb2+76r8Ul0gIuorsILFdCd2sj8Y6NJdT\nG2FkiYFxAgMBAAECggEAEoFOd4NEVARM6ZNbLfyvSJar85FVGROR1eT3Y+5ZbOun\nU7FhvQVSQo4BIJPrI4gBLbsOOveI1b3DqqC+77I5Gaaj4s+ExLAM6uVabiTy4Dv0\nsQNlDLeQ3SbAk7HzH0UFxS91FzvBOLh1teC8nWqyfqP3Qs6c7tqpagSSkADnjh5K\n+YUeKLCyy6HgwnIN6GwFD+WKX48CcxkZSTPjwMyCsKvwNGHv1SnMOx/sw+WG42Xf\nCWme2Qqc2vTFijg/OMEfFSds3eUkkEVCqtRw3T2DQargy/eMl3ELuHAze7zxJN60\n/czdQUKZ0flof+c/9WnKsa2InFFAzkhuUDTPEn239QKBgQDm4vf6jQGUyNCazvqw\ndGraix2rBGSF+kK1NOSDewkq+Q2ncvvJ78ZFXK5Lgx/gjPFiGMNVfETAmTlEnd8w\nbbLwPXT+aAL/q3Pn0KOdmv/L+dgCjPYATtOrDmO9FFP0CYA4UEL/RzS15jJoCIOz\nfalPTfJXd4ypWPyx89P4aik35QKBgQC5Zyb7M4Jj4c357DZ1GbS7qk9M501vpAfO\ntNSsZ8AAlv+8Mdi06BWxT5VF2bxPU6IQ4orGrS+WYkm7KpzaKmBmtWRK/G3yZ5Tl\nZSx0iHuikP1P5t3MLoJPSVPFk+jv2n6lfu/t9WruD8rXCsSd2z4i7C8Z69isNeny\ntae1PoGynQKBgQDfkNjzyEPGsOilblP6NtAcy+YvabJ4tMqRMiUvVxyaesyI3uMG\nN2GyWjr/LXnZckBtb3L9PLZKFFQKqB+sghxpWekGSurUbE1wI2u6uZKFDWjnl1zB\nEZMOKIHVXXCpdeWtIbKuA2H73GnkqJH2ZHBkNSK7JSyT8nHFUkdnXEyLLQKBgBd/\nXU9k/deO3L4aE+TPdzp5oUdL4WKO1XZ7MKERHSJ2AL9nSeHTsDwiq/aIW/dp0BZ3\nv8LiXC+hEVspUWvNBx69SpK+X2jje9l+8x1p1tGJsrEXv3CLTHSkBHv7/P+5H2f2\nKI5uFjlJwxlyAe1Hxh5C9M1CONnKk3XxU+oCnAl5AoGBANKjZ17RIn8hgma2elUN\nlVWPpExXEUD1A/h4jZ9csQQzCy+kaun92bNu7S+nKmSkK9eCvaLE502MtdQkYEn0\nPxYXqx6zUNIZxJCAcgDHD+bvJR5Xi6LidSW3sFakzJN5EdG+/o1ZlL7xWyFpoOCY\n58PGAdLwcjMcamlwyVewrOC1\n-----END PRIVATE KEY-----\n",
    "client_email": "gitactions@projeto-espm-dataops.iam.gserviceaccount.com",
    "client_id": "102652982804899103739",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/gitactions%40projeto-espm-dataops.iam.gserviceaccount.com"
}

try:

    """Uploads a file to the bucket."""
    credentials = service_account.Credentials.from_service_account_info(credentials_dict)
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.get_bucket('gitactions') 
    blob = bucket.blob('artist-names.csv')

    pages = []
    names = "Name \n"

    for i in range(1, 5):
        url = 'https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ' + str(i) + '.htm'
        pages.append(url)

    for item in pages:
        page = requests.get(item)
        soup = BeautifulSoup(page.text, 'html.parser')

        last_links = soup.find(class_='AlphaNav')
        last_links.decompose()

        artist_name_list = soup.find(class_='BodyText')
        artist_name_list_items = artist_name_list.find_all('a')

        for artist_name in artist_name_list_items:
        names = names + artist_name.contents[0] + "\n"

        blob.upload_from_string(names, content_type="text/csv")

except Exception as ex:
  print(ex) 