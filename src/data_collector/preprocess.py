def preprocess(items):
    cleaned_data = []
    for item in items:
        cleaned_item = {
            'license_no': item.get('LCNS_NO'),
            'permission_date': item.get('PRMS_DT'),
            'organization': item.get('PRMS_ORG_NM'),
            'business_name': item.get('BSSH_NM'),
            'address': item.get('SITE_ADDR'),
            'ceo_name': item.get('CEO_NM'),
            'tel_no': item.get('TELNO').replace("-", "") if item.get('TELNO') else None
        }
        cleaned_data.append(cleaned_item)
    return cleaned_data