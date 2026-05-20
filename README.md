This is an assignment for quartr.
You can find the task description in here:
**quartr_solution/documentation/task.txt**

you can find my ai prompts here:
**quartr_solution/documentation/ai_prompts_log.txt**
(it is not a full log, but these were my inputs, when it is not some copy-paste debugging conversation)

*quartr_solution/requirements.txt* 
    contains the dependencies. 

after that main entry point is here:

*quartr_solution/main.py*

it should work out of the box. 

The logic is , that i have a base dictionary called: needed_companies

it contains the name of the company and nickname which has to be added initially.
After that the program uses helper functions for gets the information(downloads) for identification for the form accesses here:
*quartr_solution/utils/tickers_data/company_tickers.json*

After that if searches the k-10 form. 
Downlads it into *quartr_solution/html_outputs*

After is converts it into pdf:
*quartr_solution/pdf_outputs/*

Example of the pdf name:
company nick name_form name_date of the upload:
**Alphabet_10_k_2026-02-05.pdf**

(I was able to make a container in my computer, but was not able to make a git workflow to work, 
I spent around 4 hours to make it )