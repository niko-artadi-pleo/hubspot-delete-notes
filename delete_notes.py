import hubspot
from hubspot.crm.objects.notes import PublicObjectSearchRequest, ApiException, BatchInputSimplePublicObjectId
import time
import pprint as pp

client = hubspot.Client.create(access_token="") # private key comes here use https://app.hubspot.com/private-apps/2694217/3184316
limit = 100 # maximum number that this API can process as per the documentation
after = '100' # for pagination
ticker = 0 # ticket for user
int_total = [] # total number of results to delete

# Filter criteria to find the total number of notes to be deleted.
public_object_search_request = PublicObjectSearchRequest(\
                                limit=1,\
                                filter_groups=[\
                                    {\
                                    "filters":[{"propertyName":"hs_object_source_id","value":"168764","operator":"EQ"},\
                                            {"propertyName":"hs_body_preview","value":"app.pleo.io","operator":"CONTAINS_TOKEN"},\
                                            {"propertyName":"hs_body_preview","value":"*/register/*","operator":"NOT_CONTAINS_TOKEN"}]\
                                                }\
                                            ]\
                                    )

# Fetch the total number of notes.
try:
    api_response = client.crm.objects.notes.search_api.do_search(public_object_search_request=public_object_search_request)
    pp.pprint(api_response)
    total = api_response.to_dict()
    int_total = total['total']
except ApiException as e:
    print("Exception when calling default_api->archive: %s\n" % e)

# Print the total number of notes to the user, can be commented out.
print(f'\nTotal number of notes to delete {int_total}.')

# List of notes deleted outside the list to stop While loop.
number_of_deleted_notes = []

# Start of loop to delete notes.
while int_total != len(number_of_deleted_notes):
    notes_to_be_deleted = [] # List of notes to be deleted.

    # Filter criteria paginating every 100 results.
    public_object_search_request = PublicObjectSearchRequest(\
                                    limit=100,after=after,\
                                    filter_groups=[\
                                        {\
                                        "filters":[{"propertyName":"hs_object_source_id","value":"168764","operator":"EQ"},\
                                                {"propertyName":"hs_body_preview","value":"app.pleo.io/*","operator":"CONTAINS_TOKEN"},\
                                                    {"propertyName":"hs_body_preview","value":"*/register/*","operator":"NOT_CONTAINS_TOKEN"}]\
                                                    }\
                                                ]\
                                        )
    try:
        api_response = client.crm.objects.notes.search_api.do_search(public_object_search_request=public_object_search_request)
        dic_api_response = api_response.to_dict()

        # Add notes to list outside and inside loop.
        [number_of_deleted_notes.append(i['id']) for i in dic_api_response['results']]
        [notes_to_be_deleted.append(i['id']) for i in dic_api_response['results']]

        # Start deleting notes inside the list notes_to_be_deleted.
        batch_input_simple_public_object_id = BatchInputSimplePublicObjectId(inputs=notes_to_be_deleted)
        try:
            api_response = client.crm.objects.notes.batch_api.archive(batch_input_simple_public_object_id=batch_input_simple_public_object_id)
            ticker += 1
            print('\nDeletion success ticker: ',ticker,'\nNotes deleted until now:',len(number_of_deleted_notes))
        except ApiException as e:
            print("Exception when calling default_api->archive: %s\n" % e)
            time.sleep(20)
            break

        time.sleep(10)
    except ApiException as e:
        print("Exception when calling default_api->do_search: %s\n" % e)
        break
    
    # Condition to check if the last page is reached, if not, move on to the next 100 notes to delete.
    if dic_api_response['paging']['next']['after'] == None:
        print('End of loop.')
        break
    else:
        after = dic_api_response['paging']['next']['after']
        stop_while_loop = int(after)