We decided to build a mobile application for our customers. Your goal is to build the backend for this application. We would like the app to show the history of customer's operations and the available balance. Also we'd like customers to be able to request withdrawals in the app. There're 3 types of customer operations (with their affects on customer balance):

1. Transaction:Purchase (positive)
2. Transaction:Refund (negative)
3. Withdrawal (negative)

Transactions data is provided by a 3rd party service via webhooks. Each transaction is delivered to us by a single request (no batching). Incoming transactions may be represented as objects `{"user_id": int, "transaction_id": int, "amount" Decimal, "created": datetime}` ("amount" will contain a negative value in case of refunds).
Withdrawals are initialized by our customers.

Requirements:
* Django 3.x (any modules, any data structures)
* API only, no need for UI
* Repository is hosted on github/bitbucket/gitlab. Please either make it public or provide access to "ogurtsov" for review.
* Customers may exchange their username and password for an authentication token
* Customers may see a paginated list of their operations
* Customers may see the available balance
* Customers may request a withdrawal
* Backend is ready to accept webhooks with transaction data (no need to implement authentication, just match the user_id from the transaction object with a user from our system)

Bonus points:
* Provide deployment instructions for one of the major providers (GCP, AWS, Azure, Heroku, etc). No need for actual configuration scripts: 2-3 sentences is enough.
* We expect that the assignment takes around 4 hours. Do as much as you can within this timeframe and provide a description of what else you'd like to do but was unable to due to limited time.