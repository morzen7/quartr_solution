from pathlib import Path
import utils.helper_functions as f
#forms : forms 10-Q, 10-K,8-K, 20-F, 40-F, 6-K, and their variants


if __name__ == "__main__":
    if not Path("data/company_tickers.json").exists():
        print("saving tickers...")
        f.save_tickers()

    needed_companies = {
        "Apple": {"name":"Apple Inc."},
        "Meta": {"name":"Meta Platforms, Inc."},
        "Alphabet": {"name":"Alphabet Inc."},
        "Amazon": {"name":"Amazon com Inc."},
        "Netflix": {"name":"Netflix Inc."},
        "Goldman Sachs": {"name":"Goldman Sachs Group Inc."}}

    cik_base_data = f.read_json()
    for company_name, values in needed_companies.items():
        values["cik"] =  f.get_cik(values["name"], cik_base_data)
        data = f.get_company_submissions(cik_number=values["cik"])
        latest_form = f.get_forms(data)
        values["accession_number"] = latest_form[0]
        values['filling_time']=latest_form[1]
        values['url_10_k'] = f.get_10_k_form_url(cik_number=values["cik"], accession_number=values["accession_number"])
        f.convert_sec_to_pdf(values['url_10_k'], company_name, values['filling_time'])

    print(needed_companies)

    #print(get_cik(needed_companies[0]))

