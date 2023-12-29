import configparser
import sqlglot
import os
import sqlparse
import re

current_file_path = os.path.abspath("sql_transpile_v01.py")
current_dir_path = os.path.dirname(current_file_path)
os.chdir(current_dir_path)

config = configparser.ConfigParser()
config.optionxform = str  # preserves uppercase keywords from config

config.read('config.ini')
with open(config['Input']['file_path'], "r", encoding="utf-8") as f:
    input_text = f.read()

# Replacements
replacements = dict(config.items('Keywords to replace'))

# replace strings if needed
if config.getboolean('Replacement', 'replace'):
    # Define the list of replacements

    # Replace the strings with their corresponding replacements
    for old_str, new_str in replacements.items():
        input_text = input_text.replace(old_str, new_str)

# Transpile into target dialect
input_dialect = config['Transpiling']['input_dialect']
output_dialect = config['Transpiling']['output_dialect']

output = sqlglot.transpile(input_text,
                          read=input_dialect, write=output_dialect)[0]


# Check if remove_whitespace_from_identifier is set to True in the config file
if config.getboolean('Output Formatting', 'remove_whitespace_from_identifier'):
    # Define a regular expression to find column names enclosed in single quotes
    pattern = re.compile(r"`([^`]*)`")

    # Find all column names enclosed in single quotes and replace whitespaces with underscores
    for match in pattern.finditer(output):
        column_name = match.group(1)
        if ' ' in column_name:
            new_column_name = column_name.replace(' ', '_')
            output = output.replace(column_name, new_column_name)

# Format the output
keyword_case = config['Output Formatting']['keyword_case']
identifier_case = config['Output Formatting']['identifier_case']


# Parse and format the SQL code
formatted_sql = sqlparse.format(output, reindent=True, keyword_case=keyword_case, identifier_case=identifier_case)

# Save the formatted SQL code
with open(config['Output']['file_path'], "w", encoding="utf-8") as f:
    f.write(formatted_sql)