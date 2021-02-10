import PySimpleGUI as sg
import json
from GUI import gui_functions as gf
import main


# on submit: First read all the stuff from the inputs, then validate it, then write the whole thing to a json config file
def store_data(data):
    with open('ConfigFile.json', 'w') as outfile:
        json.dump(data, outfile)


def data_converter(data):
    data = gf.convert_csv_dict_items_to_lists(data, [
        'repositories',
        'required_labels',
        'type_labels',
        'blacklist_words_issue',
        'blacklist_words_pr',
        'issue_headers',
        'issue_table_content',
        'pr_headers',
        'pr_table_content'
        'updated_after'
        'updated_before'
    ])
    return data


status = ""

sg.theme('DarkAmber')  # No gray windows please!

# STEP 1 define the layout
layout = [
    [sg.Text('Settings for ReleaseDesigner')],
    [sg.Text('In lists, items should be separated by commas')],
    [sg.Text('Token'), sg.InputText(key='token')],
    [sg.Text('Username (If you don\'t wanna use token)'), sg.InputText(key='username')],
    [sg.Text('Password (If you don\'t wanna use token)'), sg.InputText(key='password')],
    [sg.Text('Owner of repository'), sg.InputText(key='rep_owner')],
    [sg.Text('Repositories ( separated by commas)'), sg.InputText(key='repositories')],
    [sg.Text('From date ( year-month-day)'), sg.InputText(key='from_date')],
    [sg.Text('To date ( year-month-day)'), sg.InputText(key='to_date')],
    [sg.Text('Updated after ( year-month-day)'), sg.InputText(key='updated_after')],
    [sg.Text('Updated before ( year-month-day)'), sg.InputText(key='updated_before')],
    [sg.Text('State (open,closed,all)'), sg.Combo(['open', 'closed', 'all'], default_value='all', key='state')],
    [sg.Text('Language'), sg.Combo(['markdown', 'latex'], default_value='markdown', key='language')],
    [sg.Text('Results per page'), sg.InputText(key='per_page')],
    [sg.Text('Required labels'), sg.InputText(key='required_labels')],
    [sg.Text('Type labels'), sg.InputText(key='type_labels')],
    [sg.Text('Word blacklist (issues)'), sg.InputText(key='blacklist_words_issue')],
    [sg.Text('Word blacklist (pull requests)'), sg.InputText(key='blacklist_words_pr')],
    [sg.Text('Milestone'), sg.InputText(key='milestone')],
    [sg.Text('Pr Headers'), sg.InputText(key='pr_headers')],
    [sg.Text('Pr table content'), sg.InputText(key='pr_table_content')],
    [sg.Text('Issue Headers'), sg.InputText(key='issue_headers')],
    [sg.Text('Issue table content'), sg.InputText(key='issue_table_content')],
    [sg.Text('Issue/Pr filter'),
     sg.Combo(['Pull requests', 'Issues', 'Both'], key="issues_or_pr", default_value="Both")],
    [sg.Button('Ok'), sg.Button('Execute'), sg.Button('Exit')]
]

# STEP 2 - create the window
window = sg.Window('Release Designer', layout, grab_anywhere=True, finalize=True)

# Read initial values if there already is a ConfigFile
try:
    initial_values = {}
    # Read the initial config values, and format lists correctly
    with open("ConfigFile.json", "r") as json_file:
        initial_values = gf.convert_lists_to_csv(json.load(json_file))

    # Update the actual GUI
    for key in initial_values:
        window[key].update(initial_values[key])

except:
    print('ConfigFile.json does not exist. Could not read initial values')

# STEP3 - the event loop
while True:
    event, values = window.read()  # Read the event that happened and the values dictionary
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':  # If user closed window with X or if user clicked "Exit" button then exit
        break
    if event == 'Ok':
        print('Creating configuration file')
        store_data(data_converter(values))
        break
    if event == 'Execute':
        print('Creating configuration file')
        if main.main(data_converter(values)):
            print(values)
            store_data(values)
            print('Succes')
window.close()
