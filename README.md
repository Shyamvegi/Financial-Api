## Financial App Using Django,Rest Framework

## clone the repository using

```sh
$ git clone "git-url"
```


### set path to projet folder

## Make and enter a virtaul env  

```sh
py -m venv nameOfenvfolder
```
```sh
.\envFOlder\Scripts\activate
```  
## install Redis Message Broker For celery(for Async Message Queue)
### Run ping command to get pong and redis is running in your machine
```sh
c:\\redis\\redis-cli ping
```

## Now run requirements file to install all dependencies 

```sh
(env)\pip install -r requirements.txt
```

## Replace your Plaid Client details in keys.py file in PlaidApp      

```sh
(env)\ python manage.py makemigrations 
```
```sh
(env)\ python manage.py migrate 
```
```sh
(env)\ python manage.py runserver 
```
  
## Start Celery worker  

```sh
(env) celery -A BankingApp worker -loglevel=info
(env) celery -A BankingApp Beat -loglevel=info
```
![](/Images/celery.png.png)

![](/Images/Screenshot.png)
  
## API END-PONTS  
  
@http://localhost:8000/  
  
### ClientApp API (Using Postman make sure to include Authorization Token in Headers)  

-  signup/ -- User-Signup-API  
![](/Images/signup.png.png)
-  login/  -- User-Login-API    
![](/Images/login.png.png)
  
### PlaidApp API (make sure to use authorization token in postman)
## oauth using authentication to plaid
## Refer to @https://plaid/docs

-  plaidApp/ 
![](/Images/plaid.png.png)
![](/Images/1.png.png)
![](/Images/2.png.png)
![](/Images/3.png.png)

-  plaidApp/get-link-token/ ------- (get public token using link token) 
![](/Images/plaid.png.png)  

-  plaidApp/get-access-token/ - (exchange public token to access_token)  
![](/Images/public.png.png)
![](/Images/access.png.png)
![](/Images/tokens.png.png)
   
-  plaidApp/get-transactions/ ------- (fetch transactions using access token)  
![](/Images/transactions.png.png)

## Model Details:
![](/Images/x.png.png)
![](/Images/y.png.png)
![](/Images/z.png.png)
