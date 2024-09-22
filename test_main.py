from colorama import Fore, Style, init
import logging
from urllib.parse import quote
from fastapi.testclient import TestClient
from main import app

init(autoreset=True)

client = TestClient(app)

URL_VARIANTS = {
    # Expecting proxy to return PDF content
    "Direct Download": [
        "http://www.mdpi.com/2072-6643/6/6/2131/pdf",
        "https://brill.com/downloadpdf/book/edcoll/9789004391192/BP000009.pdf",
        "https://www.mdpi.com/2076-2615/6/6/35/pdf",
        "https://www.mdpi.com/2075-4698/4/4/623/pdf?version=1415182629",
        "https://revistes.uab.cat/da/article/download/v9-n4-wookey/381-pdf-en",
        "https://www.mdpi.com/2072-6643/13/3/842/pdf",
        "https://res.mdpi.com/d_attachment/animals/animals-08-00088/article_deploy/animals-08-00088-v3.pdf",
        "https://www.mdpi.com/2072-6643/11/1/43/pdf",
        "https://www.frontiersin.org/articles/10.3389/fnut.2019.00047/pdf",
        "https://figshare.com/articles/chapter/Robert_Nozick_on_nonhuman_animals_Rights_value_and_the_meaning_of_life/19434521/1/files/34682617.pdf",
    ],
    # Expecting proxy to return PDF content
    "PDF Viewer": [
        "https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/jsfa.10663",
        "https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0227046&type=printable",
        "https://link.springer.com/content/pdf/10.1007/s40572-023-00400-z.pdf",
        "https://link.springer.com/content/pdf/10.1007/s10806-020-09821-4.pdf",
        "https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0189029&type=printable",
        "https://www.cambridge.org/core/services/aop-cambridge-core/content/view/78D1F5E6B65AE7157B7AA85FF3F06017/S0963180115000079a.pdf/div-class-title-the-flaws-and-human-harms-of-animal-experimentation-div.pdf",
        "https://www.wellbeingintlstudiesrepository.org/cgi/viewcontent.cgi?article=1076&context=animsent",
        "https://www.tandfonline.com/doi/pdf/10.1080/17524032.2020.1805344?needAccess=true",
    ],
    # Expecting proxy to return PDF content
    "Redirect to PDF": [
        "https://academic.oup.com/tas/article-pdf/2/4/337/33233604/txy016.pdf"
    ],
    # Expecting proxy to redirect to original URL
    "Redirect to Non-PDF": [
        "http://www.davidpublisher.org/Public/uploads/Contribute/569c3de64e6c2.pdf",
        "https://doi.org/10.1016/j.appet.2021.105206",
        "https://www.semanticscholar.org/paper/1ec49ddcbff2cc7878749bc9e71370e60a9ac3d8",
        "https://www.semanticscholar.org/paper/ee490e7ca7f4496751fc9752be6d20c70e898e28",
        "https://doi.org/10.1093/phe/phu001",
        "https://doi.org/10.1186/s40694-018-0050-9",
        "https://doi.org/10.1093/advances/nmab063",
        "https://www.semanticscholar.org/paper/b7d4d42a3a60c6b218917a635cdb7a17ee363c7d",
        "https://doi.org/10.7554/elife.27438",
        "https://academic.oup.com/cdn/advance-article-pdf/doi/10.1093/cdn/nzac144/45948582/nzac144.pdf",
    ],
    # Expecting proxy to return PDF content or redirect to original URL
    "Redirect to Unusual PDF Viewer": [
        "https://downloads.hindawi.com/journals/cric/2015/978906.pdf"
    ],
    # Expecting proxy to redirect to original URL
    "Domain Not Found": [
        "https://www.ejast.org/download/download_pdf?pid=jast-62-1-64"
    ],
}


def add_proxy(url, index):
    # Update this to match your actual proxy server address and port
    try:
        proxy_base_url = "http://localhost:8000/pdf"
        proxy_url = f"{proxy_base_url}?url={quote(url)}"
        return proxy_url
    except Exception as e:
        logging.error(
            f"Error adding proxy: {str(e)} | url: {url} | index: {Fore.RED}{index}{Style.RESET_ALL}"
        )
        return url


def test_add_proxy():
    url = "https://example.com/test.pdf"
    proxied_url = add_proxy(url, 0)
    assert (
        proxied_url
        == "http://localhost:8000/pdf?url=https%3A%2F%2Fexample.com%2Ftest.pdf"
    )


def basic_test():
    for category, urls in URL_VARIANTS.items():
        print(f"\n{Fore.CYAN}Testing category: {category}{Style.RESET_ALL}")
        for index, url in enumerate(urls):
            proxied_url = add_proxy(url, index)
            try:
                response = client.get(f"/pdf?url={quote(url)}", allow_redirects=False)
                # Create a clickable link using ANSI escape sequences
                proxy_link = f"\033]8;;{proxied_url}\033\\Proxy URL\033]8;;\033\\"
                if response.status_code == 200:
                    content_type = response.headers.get("Content-Type", "")
                    if "application/pdf" in content_type:
                        print(
                            f"{proxy_link} {Fore.GREEN}✓ Streaming PDF: {url}{Style.RESET_ALL}"
                        )
                    else:
                        print(
                            f"{proxy_link} {Fore.YELLOW}? Unexpected content type: {content_type} for {url}{Style.RESET_ALL}"
                        )
                elif response.status_code == 307:  # Temporary Redirect
                    print(f"{proxy_link} {Fore.BLUE}→ Redirect: {url}{Style.RESET_ALL}")
                else:
                    print(
                        f"{proxy_link} {Fore.RED}✗ Unexpected status code {response.status_code}: {url}{Style.RESET_ALL}"
                    )
            except Exception as e:
                print(
                    f"{proxy_link} {Fore.RED}✗ Error: {str(e)} for {url}{Style.RESET_ALL}"
                )


if __name__ == "__main__":
    basic_test()
