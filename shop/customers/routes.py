from flask import redirect,render_template,url_for,flash,request,session,current_app,make_response
from flask_login import login_required,current_user,login_user,logout_user
from shop import db,app,photos,search,bcrypt,login_manager
from .forms import CustomerRegistration,CustomerLoginFrom
from .model import Register,CustomerOrder

import secrets,os
import json
import pdfkit
path_to_wkhtmltopdf = 'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'  # Adjust the path as necessary
config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)


import stripe
publishable_key ='pk_test_51PhSlGSEMl2j1m5C6DFOBqQUgd3hWgHV7BcoOyaGNcWWWRXQ0r1UQKGajRbNqwQhFEHA6Ec3xX1HNXoEzbV6wUEB00WLzelE4W'
stripe.api_key ='sk_test_51PhSlGSEMl2j1m5C2WuIjO5lDrTNEELmMMwRSHxQ88T8DfdW5Dh0a0EqwlPlZLTNGyJwDj2YBRn1ntxzwjXIZR1q00X7VpMYH2'

@app.route('/payment',methods=['POST'])
def payment():
    invoice = request.form.get('invoice')
    amount = request.form.get('amount')
    customer = stripe.Customer.create(
      email=request.form['stripeEmail'],
      source=request.form['stripeToken'],
    )
    charge = stripe.Charge.create(
      customer=customer.id,
      description='shop',
      amount=amount,
      currency='inr',
    )
    orders =  CustomerOrder.query.filter_by(customer_id = current_user.id,invoice=invoice).order_by(CustomerOrder.id.desc()).first()
    orders.status = 'Paid'
    db.session.commit()
    return redirect(url_for('thanks'))

@app.route('/thanks')
def thanks():
    return render_template('customer/thank.html')



@app.route('/customer/register',methods=['GET','POST'])
def customer_register():
  form = CustomerRegistration()
  if form.validate_on_submit():
    hash_password = bcrypt.generate_password_hash(form.password.data)
    register = Register(name=form.name.data,username=form.username.data,email=form.email.data,password = hash_password ,
                        country=form.country.data,state = form.state.data,city = form.city.data,address=form.address.data,
                        zipcode=form.zipcode.data)
    
    db.session.add(register)
    flash(f'Welcome {form.name.data}, Thank you for registering','success')
    db.session.commit()
    return redirect(url_for('login'))
  return render_template('customer/register.html',form=form)


@app.route('/customer/login', methods=['GET','POST'])
def customerLogin():
    form = CustomerLoginFrom()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You are login now!', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash('Incorrect email and password','danger')
        return redirect(url_for('customerLogin'))
            
    return render_template('customer/login.html', form=form)



@app.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('home'))

#remove unwanted details from shoping cart
def updateshoppingcart():
    for key, shopping in session['Shoppingcart'].items():
        session.modified = True
        del shopping['image']
        del shopping['colors']
    return updateshoppingcart


@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        updateshoppingcart()
        try:
            order = CustomerOrder(invoice=invoice,customer_id=customer_id,orders=session['Shoppingcart'])
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash('Your order has been sent successfully','success')
            return redirect(url_for('orders',invoice=invoice))
        except Exception as e:
            print(e)
            flash('Some thing went wrong while get order', 'danger')
            return redirect(url_for('getCart'))
        

@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id
        customer = Register.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()
        for _key, product in orders.orders.items():
            discount = (product['discount']/100) * float(product['price'])
            subTotal += float(product['price']) * int(product['quantity'])
            subTotal -= discount
            tax = ("%.2f" % (.06 * float(subTotal)))
            grandTotal = ("%.2f" % (1.06 * float(subTotal)))

    else:
        return redirect(url_for('customerLogin'))
    return render_template('customer/order.html', tax=tax,subTotal=subTotal,grandTotal=grandTotal,customer=customer,orders=orders)




@app.route('/get_pdf/<invoice>', methods=['POST'])
@login_required
def get_pdf(invoice):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id
        if request.method =="POST":
            customer = Register.query.filter_by(id=customer_id).first()
            orders = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()
            for _key, product in orders.orders.items():
                discount = (product['discount']/100) * float(product['price'])
                subTotal += float(product['price']) * int(product['quantity'])
                subTotal -= discount
                tax = ("%.2f" % (.06 * float(subTotal)))
                grandTotal = float("%.2f" % (1.06 * subTotal))

            rendered =  render_template('customer/pdf.html', invoice=invoice, tax=tax,grandTotal=grandTotal,customer=customer,orders=orders)
            pdf = pdfkit.from_string(rendered, False, configuration=config)
            response = make_response(pdf)
            response.headers['content-Type'] ='application/pdf'
            response.headers['content-Disposition'] ='inline; filename='+invoice+'.pdf'
            return response
    return request(url_for('orders'))