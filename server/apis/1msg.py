'''
## https://github.com/1msg/1sdk/tree/main/python

import one_msg_waba_sdk
from one_msg_waba_sdk.rest import ApiException
from pprint import pprint
from one_msg_waba_sdk.models.send_message_request import SendMessageRequest
from one_msg_waba_sdk.models.send_message_status import SendMessageStatus


# Defining the host is optional and defaults to https://api.1msg.io/YOUR_INSTANCE_NUMBER
# See configuration.py for a list of all supported configuration parameters.
configuration = one_msg_waba_sdk.Configuration(
    host = "https://sandbox.1msg.io/VID187188187/"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: token
configuration.api_key['token'] = 'link_lk5ARiUcukOwqDFHVZBVeu3tgDieQopb'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['token'] = 'Bearer'

# Enter a context with an instance of the API client
with one_msg_waba_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = one_msg_waba_sdk.MessagingApi(api_client)
    send_message_request = one_msg_waba_sdk.SendMessageRequest(chatId='VID187188187',body="msg from vs code") # SendMessageRequest | 

    try:
        # Send a Message
        api_response = api_instance.send_message(send_message_request,async_req=True)
        print("The response of MessagingApi->send_message:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MessagingApi->send_message: %s\n" % e)
'''
