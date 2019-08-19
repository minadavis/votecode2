import pandas
import re

dataFrame = pandas.read_csv(
    'part_one_dirty_addresses.csv'
    )

dataFrame['address'] = dataFrame[dataFrame.columns[0:]].apply(
    lambda x: ' '.join(x.dropna().astype(str)),
    axis=1
)

Number = '^[0-9]{2,9}'
Street = '[a-zA-Z\s]{1,20}'
Address = '(?:street|st|avenue|ave|road|rd|highway|hwy|square|sq|trail|trl|drive|dr|court|ct|park|parkway|pkwy|circle|cir|boulevard|blvd|way|freeway|pass|lane|ln|pl|bend|crossing|cross|place)'
AddressClosing = '\W?\s|$'
UnitName = '(?:apt|apartment|unit|#)'
Unit = '\W?\s?\d{0,5}\w{0,1}'
Zip = '\d{5}(?:[-\s]\d{4})?$'
City = '(?:(?:' + Address + AddressClosing + ')\s?(?:' + UnitName + Unit + ')?)(.*?)(?:' + Zip + ')?$'

dataFrame['Number'] = dataFrame['address'].str.extract(
    '(' + Number + ')', 
    expand=True)
dataFrame['Street'] = dataFrame['address'].str.extract(
    '(' + Street + Address + AddressClosing + ')',
    flags=re.IGNORECASE,
    expand=True)
dataFrame['Unit Number'] = dataFrame['address'].str.extract(
    '(' + UnitName + Unit + ')', 
    flags=re.IGNORECASE,
    expand=True)
dataFrame['City'] = dataFrame['address'].str.extract(
    City,
    flags=re.IGNORECASE,
    expand=True)
dataFrame['Zip'] = dataFrame['address'].str.extract(
    '(' + Zip + ')',
    expand=True)

dataFrame.drop(columns=["address"], inplace=True)

dataFrame = dataFrame.loc[:, ~dataFrame.columns.str.contains('^Unnamed')]

dataFrame_str = dataFrame.select_dtypes(['object'])

dataFrame[dataFrame_str.columns] = dataFrame_str.select_dtypes(
    ['object']).apply(lambda x: x.str.strip()
)

dataFrame.dropna(axis=0, how='all', thresh=None, subset=None, inplace=False)

dataFrame.to_csv('part_one_modify_addresses.csv')
