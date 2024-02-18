from selenium import webdriver
import time
import csv

from selenium.webdriver.common.by import By

website = "https://dhcbkp.nic.in/FreeText/"

driver = webdriver.Chrome()
driver.get(website)

# Find the search input field and enter the value
search_input = driver.find_element(by="id", value="search1")
search_input.send_keys("Reliance Industries")

button = driver.find_element(by="id", value="search_button")
button.click()

# Find the table containing search results
table = driver.find_element(By.TAG_NAME, "table")

records_text = table.find_elements(By.XPATH, "//table/tbody/tr/td/h3/em/strong")
records_text_list = records_text[0].text.split(" ")
records_text_index = (records_text_list.index("total")+1)
record_range = int(int(records_text_list[records_text_index])/10)+1

# Extract headers
header_cells = table.find_elements(By.XPATH, "//table/tbody/tr/td[@class='bluebg']/strong")

headers = [cell.text.strip() for cell in header_cells if not cell.text.strip() == "No."]

data = []
for i in range(record_range):
    table = driver.find_element(By.TAG_NAME, "table")
   

    # Extract data rows
    data_rows = table.find_elements(By.XPATH, "//tr[@bgcolor='#C8E9F9' or @bgcolor='#FFFFFF']")
    for row in data_rows:
        row_cells = row.find_elements(By.TAG_NAME, "td")
        row_data = [cell.text.strip() for i, cell in enumerate(row_cells) if cell.text.strip() and i != 0]

        # print(row_data,'>>row data')
        data.append(row_data)

    next_button = table.find_elements(By.XPATH, "//table/tbody/tr/td/div/span/a")
    main_next_button = [button for button in next_button if button.text == "Next"]
    if main_next_button:
        main_next_button[0].click()


# Write data to a CSV file
with open('court_cases.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)  
    writer.writerows(data)



time.sleep(20)