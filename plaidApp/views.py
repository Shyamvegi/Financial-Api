#imports

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import LogsModel,ItemModel,TransactionsModel
from .tasks import get_accounts
from plaid import Client
from datetime import datetime,timedelta
from .keys import *

#plaid Configurations

client = Client(client_id=PLAID_CLIENT_ID,secret=PLAID_SECRET, environment=PLAID_ENV)

#link to plaid connect frontend

def PlaidConnect(request):
    return render(request, 'index.html',{})

"""
API to get link token using plaid
Refered to plaid docs on getting public token and linktoken
Use exception handlers for debugging in every view
"""
class GetLinkToken(APIView):
    #permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            #create plaidConfigurations

            plaidConfigurations = {
                'user': {
                    'client_user_id': PLAID_CLIENT_ID ,
                },
                'products': ['auth', 'transactions'],
                'client_name': "shyamvegi",
                'country_codes': ['US'],
                'language': 'en',
                'webhook': 'http://localost:8000/webhook',
                'link_customization_name': 'default',
                'account_filters': {
                    'depository': {
                        'account_subtypes': ['checking', 'savings'],
                    },
                },
            }
            tokendata = client.LinkToken.create(plaidConfigurations)
            link_token = tokendata['link_token']

            print("link_token = "+ link_token)

            senddata = {'link_token': link_token}
            return Response(senddata, status=200)

        except Exception as e:
            errdata = {"message": str(e)}
            return Response(errdata, status=400)

"""
API to get access_token using public_token
Refered to plaid docs on getting access_token
Use print statements and exception handlers for debugging in every view
"""

class GetAccessToken(APIView):

    #permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            public_token = request.data['public_token']
            print("public_token = "+public_token)

            itemdata = client.Item.public_token.exchange(public_token)
            print("itemdate =",itemdata)

            access_token = itemdata['access_token']
            print("access_token = "+access_token)
            
            item_id = itemdata['item_id']
            request_id =itemdata['request_id']

            req = {'public_token': public_token}
            res = {'access_token': access_token,'item_id': item_id, "request_id": request_id}
            
            LogsModel.objects.create(request=req, response=res)
            ItemModel.objects.create(access_token=access_token,item_id=item_id, user=request.user)
            
            data = {'message': "access_token saved into db"}

            #shared task
            get_accounts.delay(res)
            return Response(data, status=200)

        except Exception as e:
            errmsg = {'message': str(e)}
            LogsModel.objects.create(request=request.data, response=errmsg)
            return Response(errmsg, status=400)

"""
API to get transactions using accesstoken in itemmodel
Refered to plaid docs on getting link token
Use exception handlers for debugging in every view
"""

class GetTransactions(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            start_date = request.data['start_date']
            end_date = request.data['end_date']
            tokenitem = ItemModel.objects.get(user=self.request.user)
            access_token = tokenitem.access_token
            response = client.Transactions.get(access_token,
                                               start_date=start_date,
                                               end_date=end_date)
            transactions = response['transactions']
            while len(transactions) < response['total_transactions']:
                response = client.Transactions.get(access_token,
                                                   start_date=start_date,
                                                   end_date=end_date,
                                                   offset=len(transactions)
                                                   )
                transactions.extend(response['transactions'])
            data = {"transactions": transactions}
            TransactionsModel.objects.create(data=data)
            status_code = 200
        except Exception as e:
            data = {"message": str(e)}
            status_code = 400
        LogsModel.objects.create(request=request.data, response=data)
        return Response(data, status=status_code)


class Webhook(APIView):
    #permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            item_id = request.data['item_id']
            tokenitem = ItemModel.objects.get(item_id=item_id)
            access_token = tokenitem.access_token
            response = client.Transactions.get(access_token,
                                               start_date=datetime.now -
                                               timedelta(days=30),
                                               end_date=datetime.now)
            transactions = response['transactions']
            data = {"transactions": transactions}
            TransactionsModel.objects.create(data=data)
            status_code = 200
        except Exception as e:
            data = {"message": str(e)}
            status_code = 400
        LogsModel.objects.create(request=request.data, response=data)
        return Response(status_code=status_code)
