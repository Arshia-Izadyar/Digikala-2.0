# digikala-clone

Digikala is an E-commerce platform like Amazone.

this is an online shop / digikala-clone with python django 4.2  🛒

## authentication 🔐

users can login with google or github


when a new user signup a wellcome email is sent using signals

user email verifucation is optional

users can reset-password, change email and etc.

2 step verification is optional

## how does it work 🤔

users can add/remove item to cart

products can be wishlisted

comments and rating system is avalibe for products

every user can only rate and comment once 

some pages are cached with **Redis**

### User profile 🧑‍💻 

users have profile page

every user can change address list for the account

CDRUD is possible on user Addresses 

Users can access to liked iitems (wish List)

every comment and rate by user is displayed in profile page

users can reset or change password in profile


### Products 💎 
every product has uuid

in home page onle top rated products will be displayed (products with rates higher than 3)

product category view is avalible

category view is reachable with slug field


you can **Filter** products with provider or brand

products can be **Searched** with thair name

product detail view will have functions like: product Rating / product Review / Product wishlist (Like) / product Add to cart

ofcorse product detail are shown 

### Shopping Cart 🛒 

every user can have only one shopping cart

items in cart can be added or removed 

if a product quantity is 0 the product will be removed from basket entirely

shopping cart will show total amount and you can cheakout from there

### Address 🧾 

every user can add up to 3 address 

in shipping page users can choose what address they want to use

### Shipping 📬 
every basket has a method called add to shipping

if a transaction is paid the items in basket will clear and move to shipping list

transaction invoice has uuid

in shipping view user will choose **when** to send **where** to send and the **sending method for shipping**