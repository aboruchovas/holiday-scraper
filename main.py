import requests, base64

property_links = [
    'https://www.airbnb.co.uk/rooms/20669368',
    'https://www.airbnb.co.uk/rooms/50633275',
    'https://www.airbnb.co.uk/rooms/33571268'
]

for link in property_links:
    # get the property id from the link and convert it to base64 for the API call
    property_id = link.split('rooms/')[1]
    property_idb64 = base64.b64encode(bytes(f'StayListing:{property_id}', 'utf-8'))
    property_idb64 = property_idb64.decode("utf-8") # to remove the b character

    # set some headers, including API key (found in their request)
    headers = {
        'authority': 'www.airbnb.co.uk',
        'accept': '*/*',
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36',
        'x-airbnb-api-key': 'd306zoyjsyarp7ifhu67rjxn52tv0t20',
    }

    # set params for our API query, including the property ID
    params = {
        'operationName': 'StaysPdpSections',
        'locale': 'en-GB',
        'currency': 'GBP',
        'variables': '{"id":"' + property_idb64 + '","pdpSectionsRequest":{"adults":"1","bypassTargetings":false,"categoryTag":null,"causeId":null,"children":null,"disasterId":null,"discountedGuestFeeVersion":null,"displayExtensions":null,"federatedSearchId":null,"forceBoostPriorityMessageType":null,"infants":null,"interactionType":null,"layouts":["SIDEBAR","SINGLE_COLUMN"],"pets":0,"pdpTypeOverride":null,"preview":false,"previousStateCheckIn":null,"previousStateCheckOut":null,"priceDropSource":null,"privateBooking":false,"promotionUuid":null,"relaxedAmenityIds":null,"searchId":null,"selectedCancellationPolicyId":null,"selectedRatePlanId":null,"splitStays":null,"staysBookingMigrationEnabled":false,"translateUgc":null,"useNewSectionWrapperApi":false,"sectionIds":null,"checkIn":null,"checkOut":null}}',
        'extensions': '{"persistedQuery":{"version":1,"sha256Hash":"7ef281634f2824262c9f7e56bd5afa278cf341da77a26ad204c444109951eaef"}}',
    }

    response = requests.get('https://www.airbnb.co.uk/api/v3/StaysPdpSections', params=params, headers=headers)
    response_data = response.json()

    if 'errors' not in response_data:
        # if there are no errors we parse the response data
        title = response_data['data']['presentation']['stayProductDetailPage']['sections']['metadata']['sharingConfig']['title']
        property_type = response_data['data']['presentation']['stayProductDetailPage']['sections']['metadata']['sharingConfig']['propertyType']
        details = response_data['data']['presentation']['stayProductDetailPage']['sections']['sections']

        print(f'Property name: {title}')
        print(f'Property type: {property_type}')
        print('=================================')
        
        # the index of detailItems and previewAmenitiesGroups seem to vary so we search for them inside a specific section
        for i in details: 
            if 'detailItems' in i['section']:
                print('Property details:')
                for j in i['section']['detailItems']:
                    print('\t', j['title'])

            if 'previewAmenitiesGroups' in i['section']:
                # there are multiple groups of amenities, however generally only 1 was found during testing
                # added support for multiple groups in case
                group = 1
                print('=================================')
                for j in i['section']['previewAmenitiesGroups']:
                    print(f'Property amenities [group {group}]:')
                    for k in j['amenities']:
                        # only print the available amenities
                        if k['available']:
                            print('\t', k['title'])

        print('==================================================================')
    else:
        # error fetching property, skip and print error message
        print(f'Error fetching data for property ID {property_id}:')
        print('\t', response_data['errors'][0]['message'])
        print('==================================================================')
