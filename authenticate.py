import globus_sdk
import os.path as op
import wget
import globus_sdk.base as base
import json
from globus_sdk import LocalGlobusConnectPersonal

# LOCAL GLOBUS CONNECT PERSONAL
#  https://github.com/globus/globus-sdk-python


def get_endpoint_id():
    for ep in tc.endpoint_search(filter_fulltext='FRDR-Prod-2', num_results=None):
        print('{0} has ID {1}'.format(ep['display_name'], ep['id']))
        return ep['id']


def get_path_content(ep_id, path):
    for en in tc.operation_ls(ep_id, path=path, num_results=None):
        new_path = op.join(path, en['name'])
        if en['type'] == 'file':
            print(new_path)
        else:
            get_path_content(ep_id, new_path)


CLIENT_ID = '01589ab6-70d1-4e1c-b33d-14b6af4a16be'

client = globus_sdk.NativeAppAuthClient(CLIENT_ID)
client.oauth2_start_flow()

authorize_url = client.oauth2_get_authorize_url()
print('Please go to this URL and login: {0}'.format(authorize_url))

# this is to work on Python2 and Python3 -- you can just use raw_input() or
# input() for your specific version
get_input = getattr(__builtins__, 'raw_input', input)
auth_code = get_input(
    'Please enter the code you get after login here: ').strip()
token_response = client.oauth2_exchange_code_for_tokens(auth_code)

globus_auth_data = token_response.by_resource_server['auth.globus.org']
globus_transfer_data = token_response.by_resource_server['transfer.api.globus.org']

# most specifically, you want these tokens as strings
AUTH_TOKEN = globus_auth_data['access_token']
TRANSFER_TOKEN = globus_transfer_data['access_token']

print(AUTH_TOKEN)
print(TRANSFER_TOKEN)

# a GlobusAuthorizer is an auxiliary object we use to wrap the token. In
# more advanced scenarios, other types of GlobusAuthorizers give us
# expressive power
# An authorizer instance used for all calls to Globus Transfer
authorizer = globus_sdk.AccessTokenAuthorizer(TRANSFER_TOKEN)
tc = globus_sdk.TransferClient(authorizer=authorizer)

# GET THE FRDR-Prod-2 ID (This is what we need)

frdr_id = get_endpoint_id()

url1 = 'https://2a9f4.8443.dn.glob.us/5/published/publication_170/submitted_data/'
base_path = '/~/5/published/publication_170/submitted_data/'

get_path_content(frdr_id, base_path)

# # CREATE AN ENDPOINT
# ep_data = {
#     "DATA_TYPE": "endpoint",
#     "display_name": 'personal',
#     "DATA": [
#         {
#             "DATA_TYPE": "personal",
#         },
#     ],
# }
# create_result = tc.create_endpoint(ep_data)



# endpoint = tc.get_endpoint(frdr_id)

# DATA LOCATION LINK
# base: https://app.globus.org/file-manager?origin_id=8ca92f91-39fb-4176-bcb9-7fb1ed53114b&origin_path=%2F
# location: https://app.globus.org/file-manager?origin_id=8ca92f91-39fb-4176-bcb9-7fb1ed53114b&origin_path=%2F5%2Fpublished%2Fpublication_170%2Fsubmitted_data%2F

# https_server = endpoint['https_server']

# source_path = "/5/published/publication_170/submitted_data/2015_11_18_cortex/2015_11_18_cortex.json"



# wget.download(url=url)
# label = "My json transfer"
#
# # TransferData() automatically gets a submission_id for once-and-only-once submission
# tdata = globus_sdk.TransferData(tc, source_endpoint_id,
#                                 dest_endpoint_id,
#                                 label=label)
#
# # Recursively transfer source path contents
# tdata.add_item(source_path, dest_path, recursive=True)

# IMPORTANT PAGES: https://docs.globus.org/globus-connect-server-installation-guide/
# https://docs.globus.org/globus-connect-server-v5-installation-guide/#_creating_a_storage_gateway_using_the_posix_storage_connector


# TRY AND NAVIGATE IN THE ENDPOINT PATH AND RETRIVE DATA

# HOW TO TRANSFER DATA (GLOBUS PRINCIPLE)
# How can I transfer files to and from my laptop or desktop?
#
# Use Globus Connect Personal, which provides a point-and-click interface for configuring and operating a Globus endpoint
# on your local machine. After installing Globus Connect Personal, your computer looks just like any other Globus endpoint
# so all the standard Globus web and command line interface features will work. Globus Connect Personal runs behind NATs
# and firewalls, as long as it can make an outbound connection. Click the link for your operating system to get started
# with Globus Connect Personal: Mac OS X, Windows, Linux.
