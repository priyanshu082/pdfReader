import PyPDF2
import re

def extract_data_by_status(pdf_path, status_filter="usdt"):
    print(f"Status Filter: {status_filter}")
    print(f"PDF File: {pdf_path}")
    
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        extracted_data = []

        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()

            # print(f"\n--- Page {page_num + 1} ---\n")
            
            lines = text.split("\n")
            
            column_counter = 1
            current_amount = None
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                # print(f"Line {line_num} Column {column_counter}: {line}")
                
                if column_counter == 2 and re.match(r'^-?\d+(\.\d+)?$', line):
                    current_amount = float(line)
                    # print(f"Found amount: {current_amount}")
                
                elif column_counter == 3 and line in ['usdt', 'Failed', 'Pending']:
                    if current_amount is not None:
                        transaction = {'amount': current_amount, 'status': line}
                        # print(f"Found complete transaction: {transaction}")
                        if line == status_filter:
                            extracted_data.append(transaction)
                            # print(f"Added transaction to extracted data")
                   
                
                column_counter += 1
                
                if column_counter > 5:
                    column_counter = 1
                    current_amount = None  # Reset for the next row

    # print(f"\nExtracted Data: {extracted_data}\n")
    return extracted_data

# Example usage
pdf_file = 'AnilCryptoWidh.pdf'
successful_transactions = extract_data_by_status(pdf_file, status_filter="usdt")

# Print the extracted data
print("Extracted Transactions of Crypto:")
sum=0
for transaction in successful_transactions:
    sum+=transaction['amount']

# for transaction in successful_transactions:
#     print(transaction )

print(sum)