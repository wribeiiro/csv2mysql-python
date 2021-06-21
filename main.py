from reader import Reader

columns = ["company_id", "record_date", "due_date", "pay_date", "department_id", "accounting_code_id", "provider_id", "payment_type_id", "value", "note", "sequence", "created_at"]

read_csv = Reader('test.csv', columns)
read_csv.execute()
