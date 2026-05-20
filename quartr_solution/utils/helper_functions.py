import requests
from pathlib import Path
import json
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time



user_agent_name = "Tamas Torda"
user_agent_mail = "iam.tamas.torda@gmail.com"
tickers_data_folder_base = Path("utils/tickers_data")

def header_info():
    headers = {
        "User-Agent": f"{user_agent_name} [{user_agent_mail}]"
    }
    return headers

def read_json(file_base_path=tickers_data_folder_base):
    filepath = file_base_path / "company_tickers.json"
    with open(filepath, "r") as f:
        data = json.load(f)

    return(data)

def save_tickers(file_base_path=tickers_data_folder_base):
    url = "https://www.sec.gov/files/company_tickers.json"

    headers = header_info()
    data_folder = file_base_path
    data_folder.mkdir(exist_ok=True)

    filepath = data_folder / "company_tickers.json"

    response = requests.get(url, headers=headers)

    filepath.write_bytes(response.content)

    print(f"Saved to: {filepath.resolve()}")

def get_cik(company_name:str, data):
    return ([str(tick["cik_str"]).zfill(10) for tick in data.values()
               if get_formatted_name(company_name) == get_formatted_name(tick["title"])][0])

def get_formatted_name(name):

    elements = ["INC", ",", " ", "."]
    name = name.upper()
    for e in elements:
        name = name.replace(e, "")
    return name

def get_company_submissions(cik_number):
    headers = header_info()
    url = f"https://data.sec.gov/submissions/CIK{cik_number}.json"

    data = requests.get(url, headers=headers).json()
    return data

def get_forms(data, form_type="10-K"):
    filings = data["filings"]["recent"]
    res = list()
    for i in range(len(filings["form"])):
        if filings["form"][i] == form_type:
            accession = filings["accessionNumber"][i]
            filing_date = filings["filingDate"][i]

            res.append((accession, filing_date))
    if res:
        return res[0]
    else:
        return None

def get_10_k_form_url(cik_number, accession_number):
    base_cik = str(int(cik_number))
    if not accession_number:
        return None
    accession_no_dash = accession_number.replace("-", "")
    url = f"https://www.sec.gov/Archives/edgar/data/{base_cik}/{accession_no_dash}/{accession_number}-index.html"
    headers = header_info()
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")

    table = soup.find("table")

    for row in table.find_all("tr"):
        cols = row.find_all("td")

        if len(cols) < 3:
            continue

        col1 = cols[0].get_text(strip=True)
        col2 = cols[1].get_text(strip=True)

        if "10-K" in col1 or "10-K" in col2:
            link_tag = cols[2].find("a")

            if link_tag:
                href = link_tag["href"]
                full_url = "https://www.sec.gov" + href

                return full_url.replace('ix?doc=/', '')
        else:
            return None

def convert_sec_to_pdf(url_10_k_form, company_name, filling_date):
    base = Path.cwd()
    output_html_path = f"{base}/html_output/{company_name}_10_k_{filling_date}.html"
    output_pdf_path = f"{base}/pdf_outputs/{company_name}_10_k_{filling_date}.pdf"
    html = requests.get(url_10_k_form, headers=header_info()).text

    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html)

    html_file = Path(output_html_path).resolve()
    pdf_file = Path(output_pdf_path).resolve()

    if not html_file.exists():
        raise FileNotFoundError(f"HTML file not found: {html_file}")

    with sync_playwright() as p:
        browser = p.chromium.launch()

        context = browser.new_context()
        page = context.new_page()

        # Load local HTML file
        page.goto(f"file://{html_file}")

        # Give SEC pages time to fully render
        time.sleep(2)

        # Export to PDF
        page.pdf(
            path=str(pdf_file),
            format="A4",
            print_background=True
        )

        browser.close()

    print(f"PDF saved to: {pdf_file}")