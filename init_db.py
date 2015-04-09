__author__ = 'David'
#!/usr/bin/env python3

# initialize Django
import os
import sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'test_dmp.settings'
import django
django.setup()
from django.contrib.auth.models import Group, Permission
from django.db import connection
import subprocess

# regular imports
import homepage.models as hmod


##### DROP DATABASE, RECREATE IT, THEN MIGRATE IT #################

cursor = connection.cursor()
cursor.execute("DROP SCHEMA PUBLIC CASCADE")
cursor.execute("CREATE SCHEMA PUBLIC")
subprocess.call([sys.executable, "manage.py", "migrate"])

####################################    DUMMY DATA    ################################################
##########################       PHOTOS
for data in [
    #Products
    ["2000-12-25", "Bean Land", "Jack's Magic Beans", "/static/homepage/media/magicbeans.jpg"],
    ["2000-12-25", "Washington D.C.", "George Washington's Pipe", "/static/homepage/media/pipe.jpg"],
    ["2000-12-25", "My house", "A tattered old flag I found", "/static/homepage/media/tatteredflag.jpg"],
    ["2000-12-25", "blah blah", "yippeehiay", "/static/homepage/media/flag2.jpg"],
    ["2000-12-25", "The Death Star", "Darth Vader's Helmet", "/static/homepage/media/darth.jpg"],
    ["2000-12-25", "George's House", "George Washington's Breeches", "/static/homepage/media/georgesbreeches.jpg"],
    ["2000-12-25", "On some dude's head", "Raccoon Fur Hat", "/static/homepage/media/raccoonhat.jpg"],
    ["2002-12-25", "The shop", "A fancy wig styling kit", "/static/homepage/media/wigstyling.png"],
    #Areas
    ["2002-12-25", "Gove's Bakery", "Bread in a brick oven", "/static/homepage/media/bakery.jpg"],
    ["2002-12-25", "Cooperage", "A barrel", "/static/homepage/media/cooperage.jpg"],
    ["2002-12-25", "Stole it from the internet", "Information Booth", "/static/homepage/media/informationbooth.jpg"],
    ["2002-12-25", "Jamestown", "Jamestown", "/static/homepage/media/jamestown.jpg"],
    ["2002-12-25", "Old South Church ", "Old South Church", "/static/homepage/media/oldsouthchurch.jpg"],
    ["2002-12-25", "Stole it from the internet", "Security Booth", "/static/homepage/media/securitybooth.jpg"],
    #Events
    ["2003-12-25", "Red Butte Garden", "Gorgeous gardens", "/static/homepage/media/red_butte.jpg"],
    ["2004-12-25", "Thanksgiving Point", "Museums and cool stuff", "/static/homepage/media/thanksgiving_point.jpg"],
    ["2005-12-25", "BYU Campus", "The Lord's University", "/static/homepage/media/byu_campus.jpg"],
    ["2006-12-25", "Bryce Canyon", "Desert and more desert", "/static/homepage/media/bryce_canyon.jpg"],
    #Made-to-order Items (ID starts at 19)
    ["1991-11-05", "Cooperage", "Hand-crafted hatchet of handliness", "/static/homepage/media/hatchet.jpg"],
    ["1995-11-05", "Cooperage", "Carry some nice water in this bad boy", "/static/homepage/media/beaver_bucket.jpg"],
    ["1999-11-05", "Bakery", "Corn + bread = cornbread", "/static/homepage/media/cornbread.jpg"],
]:
    p = hmod.Photograph()
    p.date_taken = data[0]
    p.place_taken = data[1]
    p.description = data[2]
    p.image = data[3]
    p.save()

##########################       ADDRESSES
for data in [
    ["1432 Wallaby Way", "Sydney", "SydneyState", "49830", "Australia"],
    ["1782 S. Ashland Ridge dr.", "Herriman", "UT", "47483", "USA"],
    ["4484 W. 344 S.", "Salt Lake", "UT", "84848", "USA"],
    ["4555 W. 566 S.", "hahaha", "NY", "44555", "USA"],
    ["34343 W. 884444 S.", "Provo", "UT", "84333", "USA"],
]:
    a = hmod.Address()
    a.street1 = data[0]
    a.city = data[1]
    a.state = data[2]
    a.zip_code = data[3]
    a.country = data[4]
    a.save()


###################################      CREATE PERMISSIONS/GROUPS
g1 = Group()
g1.name = "Admin"
g1.save()

g2 = Group()
g2.name = 'Manager'
g2.save()

g3 = Group()
g3.name = 'Agent'
g3.save()

g4 = Group()
g4.name = 'Customer'
g4.save()

############################       ADD Permissions to Groups

admin = Group.objects.get(name="Admin")
admin.permissions = Permission.objects.all()
admin.save()

countPermissions = Permission.objects.count()
y = 3
managerList = []
while y<=countPermissions:
    managerList.append(y)
    y = y + 3
print(managerList)
manager = Group.objects.get(name="Manager")
manager.permissions = Permission.objects.all().exclude(id__in=managerList) #Just can't delete Users
manager.save()

agent = Group.objects.get(name="Agent")
x = 1
agentList = []
while x<countPermissions-1:
    agentList.append(x)
    x = x + 3
print(agentList)
agent.permissions = Permission.objects.filter(id__in=agentList) ##I want this to exclude all id's of the multiple 3 so the Agent can't delete anything.  
agent.save()

###################################    USERS

id_counter = 0

for data in [

    ["Jayson", "Jensen", "jayson", "jayson", "jensenjb21@gmail.com", False, "Am I cool?", "yes", "801-324-4233", 1, 5, 1],
    ["Macey", "Vogt", "macey", "macey", "davidericvogt@gmail.com", False, "Whos my daddy?", "Gerald", "801-624-4433", 2, 5, 4],
    ["David", "Vogt", "david", "david", "davidericvogt@gmail.com", False, "How old am I?", "43", "801-324-4433",2, 5, 3],
    ["Steven", "Dewey", "steven", "steven", "s.dewey1@gmail.com", False, "Whats my favorite color?", "pink", "801-384-4433", 3, 5, 2],
    ["Bucky", "LeStarge", "kevin", "kevin", "kblestarge@gmail.com", True, "Am I cool?", "Heck yes", "801-324-4733", 4, 5, 1],
    ["Gove", "Allen", "gove", "gove", "fake.gove@byu.edu", False, "I am the...", "Gove", "801-422-1206", 5, 5, 3],
]:

    u = hmod.User()
    u.first_name = data[0]
    u.last_name = data[1]
    u.set_password(data[2])
    u.username = data[3]
    u.email = data[4]
    u.is_superuser = data[5]
    u.security_question = data[6]
    u.security_answer = data[7]
    u.phone = data[8]
    u.address_id = data[9]
    u.photo_id = data[10]
    u.save()

    u.groups.add(data[11])
    u.save()


##########################       EVENTS
for data in [
    ["Spring Festival", "Beautiful gardens near the U of U", "2000-12-25", "2012-12-25", "http://www.redbuttegarden.org/sites/default/files/ParkingMap__Print.pdf", "Red Butte Garden", 1, 15],
    ["Summer Festival", "Museums and open landscape", "2000-12-25", "2012-12-25", "http://www.thanksgivingpoint.org/document.doc?id=424", "Thanksgiving Point", 1, 16],
    ["Winter Festival", "Different events in different BYU buildings", "2000-12-25", "2012-12-25", "http://map.byu.edu/campusmap.pdf", "BYU Campus", 2, 17],
    ["Fall Festival", "A great big desert with canyons", "2000-12-25", "2012-12-25", "https://www.utah.com/nationalparks/bryce_canyon/bryce-map.pdf", "Bryce Canyon", 4, 18],
]:
    e = hmod.Event()
    e.name = data[0]
    e.description= data[1]
    e.start_date = data[2]
    e.end_date = data[3]
    e.map_file_name = data[4]
    e.venue_name = data[5]
    e.address_id = data[6]
    e.photo_id = data[7]
    e.save()

#################################      AREA

for data in [
    ["Security", "Security station", "6", 1, 2, 4, None, 14],
    ["Information Booth", "Maps and helpers", "5", 1, 2, 4, None, 11],
    ["Bakehouse", "Bread making demonstrations", "4", 1, 2, 4, None, 9],
    ["Cooperage", "Items made of copper", "2", 1, 2, 4, None, 10],
    ["Jamestowne", "Visit old Jamestowne", "3", 1, 2, 4, None, 12],
    ["Old South Church", "Worship respectfully", "8", 1, 2, 4, None, 13],
]:

    a = hmod.Area()
    a.name = data[0]
    a.description = data[1]
    a.place_number = data[2]
    a.coordinator_id = data[3]
    a.supervisor_id = data[4]
    a.event_id = data[5]
    #a.participants = data[6]
    a.photo_id = data[7]
    a.save()

##########################       CATEGORY
e1 = hmod.Category()
e1.description = "Cool Category"
e1.save()

e2 = hmod.Category()
e2.description = "Rad Category"
e2.save()

e3 = hmod.Category()
e3.description = "Too-cool-for-school Category"
e3.save()

##########################       PRODUCT SPECIFICATION
for data in [
    #Mass-Produced Items
    ["Magic Beans", "39.95", "These beans make you smarter and taller", "Jack", "0.01", "hhhhh", "sdf", "five", 1, 5, 1, "product", None],
    ["George Washington's Pipe", "1300", "Seriously, he smoked this", "His Mom", "1000", "hhhhh", "sdf", "five", 2, 5, 2, "product", None],
    ["Tattered 19th Century Flag", "369.95", "This flag was waved by President Obama at his inauguration", "China", "4.50", "hhhhh", "sdf", "five", 3, 5, 3, "product", None],
    #Rental Items
    ["George Washington's Breeches", "8000", "You can wear these to parties, on Halloween, or just when you're feeling lazy but presidential", "His Mom", "8000", "sku", "an order_form_name", "a production_time", 3, 5, 6, "product", None],
    ["Raccoon Fur Hat", "75", "Daveeeeeee, Davy Crocket! Born on the wild frontier", "The boy from Where the Red Fern Grows", "75", "sku", "an order_form_name", "a production_time", 3, 5, 7, "product", None],
    ["Wig Styling Kit", "244.53", "Display a full head of hair", "Vietnam", "5.60", "sku", "an order_form_name", "a production_time", 3, 2, 8, "product", None],
    #Made-to-order Items
    ["Beaver Bucket", "40.00", "It's called a Beaver Bucket because the way it is", "Beavers", "20.00", "sku", "an order_form", "a production_time", 3, 2, 19, "mto", 4],
    ["Corn Bread in a Cast Iron Skillet", "100.00", "We've literally tasted every recipe of cornbread in the world, and Gove's is the best.", "Gove Allen", "1.00", "sku", "an order_form", "a production_time", 3, 6, 20, "mto", 3],
    ["Hatchet", "654.51", "Handy tool for hunting small beasts", "Cooperage", "122.74", "sku", "an order_form_name", "a production_time", 3, 2, 21, "mto", 4],
]:

    e = hmod.ProductSpecification()
    e.name = data[0]
    e.price = data[1]
    e.description = data[2]
    e.manufacturer = data[3]
    e.average_cost = data[4]
    e.sku = data[5]
    e.order_form_name = data[6]
    e.production_time = data[7]
    e.category_id = data[8]
    e.vendor_id = data[9]
    e.photo_id = data[10]
    e.type = data[11]
    e.area_id = data[12]
    e.save()

#########################       STOCKED PRODUCT
for data in [
    ["5", "Behind the fridge", "I don't know", 1, 3],
    ["445", "Shed", "I don't know", 2, 1],
    ["100", "sdfs", "I don't know", 2, 3],
    ["42", "house", "I don't know", 1, 2],
    ["7", "Under the bed", "I don't know", 2, 3],
]:
    s = hmod.StockedProduct()
    s.quantity_on_hand = data[0]
    s.shelf_location= data[1]
    s.order_file= data[2]
    s.photo_id= data[3]
    s.product_specification_id= data[4]
    s.save()

##########################       SERIALIZED PRODUCT
for data in [
    ["1", "product", "2012-12-12", "50.55", True, False, "this is a good product", 1, "Huge", "well, kinda huge", "Male", "Green", "stripes", "1776", "1889", "1", "Barn", "I don't know", 2, 2],
    ["2", "product", "2012-12-12", "50.55", True, False, "this is a good product", 1, "Huge", "well, kinda huge", "Male", "Green", "stripes", "1776", "1889", "45", "Barn", "I don't know", 3, 3],
    ["5", "product", "2012-12-12", "50.55", True, False, "this is a good product", 1, "Huge", "well, kinda huge", "Male", "Green", "stripes", "1776", "1889", "5", "Barn", "I don't know", 1, 1],
]:

    sp = hmod.SerializedProduct()
    sp.serial_number = data[0]
    sp.type = data[1]
    sp.date_acquired = data[2]
    sp.cost = data[3]
    sp.for_sale = data[4]
    sp.condition_new = data[5]
    sp.notes = data[6]
    sp.owner_id = data[7]
    sp.size = data[8]
    sp.size_modifier = data[9]
    sp.gender = data[10]
    sp.color = data[11]
    sp.pattern = data[12]
    sp.start_year = data[13]
    sp.end_year = data[14]
    sp.quantity_on_hand = data[15]
    sp.shelf_location= data[16]
    sp.order_file= data[17]
    sp.photo_id= data[18]
    sp.product_specification_id= data[19]

    sp.save()

#########################       RENTAL PRODUCT
for data in [
    ["45", "20.00", "8000.00", "34", "rental", "2012-12-12", "8000", False, False, "this is a good rental product", 1, "34 waste, 32 length", "button crotch", "Male", "Yellow", "lad", "1733", "1999", "400", "behind fridge", "dsfd", 6, 4],
    ["234", "5.00", "75.00", "66", "rental", "2012-12-12", "75.00", False, False, "this is a good rental product", 4, "Huge", "well, kinda huge", "Male", "Yellow", "lad", "1733", "1999", "400", "behind fridge", "dsfd", 7, 5],
    ["2", "55.43", "99.99", "90", "rental", "2012-12-12", "50.55", False, False, "this is a good rental product", 5, "Huge", "well, kinda huge", "Male", "Yellow", "lad", "1733", "1999", "400", "behind fridge", "dsfd", 8, 6],
]:

    r = hmod.RentalProduct()
    r.times_rented = data[0]
    r.price_per_day= data[1]
    r.replacement_price= data[2]
    r.serial_number = data[3]
    r.type = data[4]
    r.date_acquired = data[5]
    r.cost = data[6]
    r.for_sale = data[7]
    r.condition_new = data[8]
    r.notes = data[9]
    r.owner_id = data[10]
    r.size = data[11]
    r.size_modifier = data[12]
    r.gender = data[13]
    r.color = data[14]
    r.pattern = data[15]
    r.start_year = data[16]
    r.end_year = data[17]
    r.quantity_on_hand = data[18]
    r.shelf_location= data[19]
    r.order_file= data[20]
    r.photo_id= data[21]
    r.product_specification_id= data[22]

    r.save()
#################################      ORDER

for data in [
   ["1990-08-15", "801-898-6764", "2000-12-12", "2000-11-11", "2000-11-11", "453", 2, 1, 3, 2, 3, 4],
   ["1990-08-15", "801-898-6764", "2000-12-12", "2000-11-11", "2000-11-11", "453", 2, 5, 3, 2, 4, 2],
    ["1990-08-15", "801-898-6764", "2000-12-12", "2000-11-11", "2000-11-11", "453", 1, 1, 1, 2, 1, 4],
    ["1990-08-15", "801-898-6764", "2000-12-12", "2000-11-11", "2000-11-11", "453", 2, 3, 2, 2, 3, 4],
]:

    sp = hmod.Order()
    sp.order_date = data[0]
    sp.phone = data[1]
    sp.date_packed = data[2]
    sp.date_paid = data[3]
    sp.date_shipped = data[4]
    sp.tracking_number = data[5]
    sp.ships_to_id = data[6]
    sp.packed_by_id = data[7]
    sp.payment_processed_by_id = data[8]
    sp.shipped_by_id = data[9]
    sp.handled_by_id = data[10]
    sp.customer_id = data[11]
    sp.save()

#################################      CART LINE ITEM

for data in [
   ["51", 2, 3],
    ["83", 1, 1],
    ["74", 3, 2],
]:

    cli = hmod.CartLineItem()
    cli.quantity = data[0]
    cli.stocked_product_id = data[1]
    cli.user_id = data[2]
    cli.save()

#################################      SALE ITEM

for data in [
   ["989", 5, "499.99", 2],
   ["912", 3, "499.99", 1],
    ["89", 9, "499.99", 3],
    ["20", 1, "499.99", 4],
]:

    si = hmod.SaleItem()
    si.quantity = data[0]
    si.product_id = data[1]

    si.amount = data[2]
    si.order_id = data[3]

    si.save()

#################################      Rental Item

for data in [
   ["1998-12-12", "1990-08-15", "1995-03-01", ".50", 9, "99.99", 1],
    ["1988-12-12", "1990-08-15", "2015-03-06", ".50", 10, "99.99", 2],
    ["1978-12-12", "1990-08-15", "2016-03-08", ".50", 11, "99.99", 3],
]:

    ri = hmod.RentalItem()
    ri.date_out = data[0]
    # ri.date_in = data[1]
    ri.date_due = data[2]
    ri.discount_percent = data[3]
    ri.rental_product_id = data[4]

    ri.amount = data[5]
    ri.order_id = data[6]
    ri.save()

#################################      Damage Fee

for data in [
   ["dents and scrapes", False, 3, "50.43", 1],
   ["paint spilled", True, 1, "43", 2],
    ["grass stains", False, 2, "10.00", 3],
]:

    df = hmod.DamageFee()
    df.description = data[0]

    df.waived = data[1]
    df.rental_item_id = data[2]

    df.amount = data[3]
    df.order_id = data[4]

    df.save()

#################################      Late Fee

for data in [
   ["5", False, 1, "10.43", 3],
   ["3", True, 2, "4.50", 2],
    ["25", False, 3, "50.00", 1],
]:

    lf = hmod.LateFee()
    lf.days_late = data[0]

    lf.waived = data[1]
    lf.rental_item_id = data[2]

    lf.amount = data[3]
    lf.order_id = data[4]

    lf.save()

################################      Configuration Parameters

for data in [
   [".23"],
   [".20"],
    [".13"],
]:

    cp = hmod.ConfigurationParameters()
    cp.sales_tax_rate = data[0]
    cp.save()

#################################       Participant Role

for data in [
   [1, 1, "Colonial Tea Party Guy", "Cool"],
   [3, 2, "Bootlegger", "kinda lame"],
    [2, 3, "Cook in the kitchen", "funny"],
]:

    pr = hmod.ParticipantRole()
    pr.participant_id = data[0]
    pr.area_id = data[1]
    pr.name = data[2]
    pr.type = data[3]

    pr.save()

print("Script ran successfully!          Group Lucky #7 is in the house!")