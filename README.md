# DuFarms

DuFarms is a Flask application for keeping track of products, locations, and the product movements between the locations.
It was written as a test project for [Frappe.io](https://frappe.io).

## The Challenge
Below is the test:  

The goal is to create a web application using Flask framework to manage inventory of a list of products in respective warehouses. Imaging this application will be used in a shop or a warehouse that needs to keep track of various products and various locations

The application should cover following functionalities:
Database Tables:

    Product (product_id)
    Location (location_id)
    ProductMovement (movement_id, timestamp, from_location, to_location, product_id, qty)

Note: Any one, or both of from_location and to_location can be filled. If you want to move things into a location, from_location will be blank, if you want to move things out, then to_location will be blank.
Views:

    Add/Edit/View Product
    Add/Edit/View Location
    Add/Edit/View ProductMovement

Report:

    Balance quantity in each location

Use Cases:

    Create 3/4 Products
    Create 3/4 Locations
    Make ProductMovements
        Move Product A to Location X
        Move Product B to Location X
        Move Product A from Location X to Location Y
        (make 20 such movements)
    Get product balance in each Location in a grid view, with 3 columns: Product, Warehouse, Qty


## Getting Started

To get this application on your local machine, you either clone this repository:  

`git clone git@github.com:HAKSOAT/DuFarms.git`

### Prerequisites

To install the prerequisites for this application, simply run the command below.
Strictly for Python 3, Python 2 may not behave as expected.

```
pip install -r requirements.txt
```

### Running Application

To run this application, navigate to the root folder and run the command below:

```
python run.py
```

You can then view and use the application by opening `localhost:5000` on your browser.

### Screenshots
![](https://github.com/HAKSOAT/Timely/blob/master/screenshots/0.png)
![](https://github.com/HAKSOAT/Timely/blob/master/screenshots/1.png)
![](https://github.com/HAKSOAT/Timely/blob/master/screenshots/2.png)
![](https://github.com/HAKSOAT/Timely/blob/master/screenshots/3.png)
![](https://github.com/HAKSOAT/Timely/blob/master/screenshots/4.png)
![](https://github.com/HAKSOAT/Timely/blob/master/screenshots/5.png)
![](https://github.com/HAKSOAT/Timely/blob/master/screenshots/6.png)
![](https://github.com/HAKSOAT/Timely/blob/master/screenshots/7.png)
![](https://github.com/HAKSOAT/Timely/blob/master/screenshots/8.png)
![](https://github.com/HAKSOAT/Timely/blob/master/screenshots/9.png)
![](https://github.com/HAKSOAT/Timely/blob/master/screenshots/10.png)
![](https://github.com/HAKSOAT/Timely/blob/master/screenshots/11.png)
![](https://github.com/HAKSOAT/Timely/blob/master/screenshots/12.png)
![](https://github.com/HAKSOAT/Timely/blob/master/screenshots/13.png)
![](https://github.com/HAKSOAT/Timely/blob/master/screenshots/14.png)
![](https://github.com/HAKSOAT/Timely/blob/master/screenshots/15.png)
![](https://github.com/HAKSOAT/Timely/blob/master/screenshots/16.png)
![](https://github.com/HAKSOAT/Timely/blob/master/screenshots/17.png)
![](https://github.com/HAKSOAT/Timely/blob/master/screenshots/18.png)
![](https://github.com/HAKSOAT/Timely/blob/master/screenshots/19.png)
![](https://github.com/HAKSOAT/Timely/blob/master/screenshots/20.png)


## Author

* **Habeeb Kehinde Shopeju** - [HAKSOAT](https://haksoat.github.io)


## Contributions

Contributions are welcome. Especially if you could help compile into an executable file, as I am having issues doing that.

