import plaid
from celery import shared_task
from .keys import *
from .models import *

# Create your views here.

client = plaid.Client(client_id=PLAID_CLIENT_ID,
                secret=PLAID_SECRET, environment=PLAID_ENV)


@shared_task
def get_accounts(request_data):
    access_token = request_data['access_token']
    try:
        response1 = client.Accounts.get(access_token)
        accounts = response1['accounts']

        response2 = client.Item.get(access_token)
        item = response2['item']
        status = response2['status']
        data = {"account_get_response": response1,
                "item_get_response": response2}
        Account.objects.create(data=response1)
        Item.objects.create(data=response2)
    except Exception as e:
        data = {"message": str(e)}
    LogsModel.objects.create(request=request_data, response=data)