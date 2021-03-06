import sys
import datetime
import json
import re

def parse_date(date):
    try:
        date_time_obj = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')
        return str(date_time_obj)
    except Exception as e:
        print('Could not parse date ' + date)
        return sys.exit()

def parse_type(raw_type):
    type_dict = {
        r"^Investicija į kreditą „[A-Z0-9]+“$": 'Investment',
        r"^Sąskaitos \"[A-Z0-9]+\" papildymas$": 'Deposit',
        r"^Investicijos [A-Z0-9]+ kredito dalies grąžinimas$": 'Loan return',
        r"^Investicijos [A-Z0-9]+ palūkanų grąžinimas$": 'Interest',
        r"^Investicijos [A-Z0-9]+ grąžinimas atsisakius vartojimo paskolos$": 'Loan decline',
        r"^Gautas pavedimas \"[A-Z0-9]+\" iš vartotojo \"\"NEO Finance\", AB\"$": 'Affiliate earnings',
        r"^Užtikrinimo fondo mokestis už investiciją į kreditą „[A-Z0-9]+“$": 'Buyback guarantee',
        r"^Tarpininkavimo mokestis už investicijos [A-Z0-9]+ gautą įmoką$": 'Broker fee',
        r"^Investicijos [A-Z0-9]+ kredito dalies grąžinimas iš užtikrinimo fondo$": 'Loan return', # Could change type to Buyback loan return
        r"^Investicijos [A-Z0-9]+ palūkanų grąžinimas iš užtikrinimo fondo$": 'Interest' # Could change type to Buyback interest
    }

    for regex in type_dict:
        p = re.compile(regex)
        m = p.match(raw_type)
        if (m != None):
            return type_dict[regex]

    print('Could not map type for ' + raw_type)
    return sys.exit()

def parse_amount(raw_debit, raw_credit):
    if (raw_debit == ''):
        return raw_credit
    elif (raw_credit == ''):
        return "-" + raw_debit
    else:
        print("Could not parse amount (debit: " + raw_debit + "credit: " + raw_credit + ")")
        sys.exit()

def process_event(event):
    delim = ';'

    raw_date = event['date']
    raw_name = event['name']
    raw_debit = event['debit']
    raw_credit = event['credit']

    inv_date = parse_date(raw_date)
    inv_type = parse_type(raw_name)
    inv_name = raw_name
    inv_amount = parse_amount(raw_debit, raw_credit)
    inv_currency = 'EUR'
    inv_platform = 'Paskolų klubas'

    inv_details = [
        inv_date,
        inv_name,
        inv_amount,
        inv_currency,
        inv_type,
        inv_platform
    ]
    return delim.join(inv_details)

def get_events():
    print("Paste your PK events and hit Ctrl-D:")
    events_raw = sys.stdin.read()
    events = json.loads(events_raw)
    return events

events = get_events()
processed_events = list(map(process_event, events))

for event in processed_events:
    print(event)
