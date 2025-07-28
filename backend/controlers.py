from flask import current_app as app
from flask import Flask, render_template,request,redirect,url_for,session , flash
from backend.Models import *





@app.route("/",methods=["GET","POST"])#by default the method is get but if u want to post then u can write post
def login():
    if request.method == "POST":
        email = request.form.get("email")#it is same as username=request.form["username"] the only difference is it don't raise any error if value is missing,,means taking value from form and storing it in variable  name email
        password = request.form.get("password")

        #now i want to check whether username and password is present in database or not
        #second thing accordingly i want to redirect this to different html pages...
        usr=Admin_User_Details.query.filter_by(email=email,password=password).first()# iska matlab hai ki Admin_User_Details table me query karo/search karo,query karni hai ki filter by means search such that email=email and password=password(isme pehla vala variable table ka attribute hotta hai aur dusra vala variable ka naam hota hai jisme humne value store kiya hai),give me first record (row) if it is present in database
        if usr and usr.role==0:#saying only if user means if user is existed means it shouldn't be null then execute this code
            return redirect(url_for("admin_home"))#if admin exists then render admin home
        
        elif usr and usr.role==1:#saying only if user means if user is existed means it shouldn't be null then execute this code
            return redirect(url_for("user_home" , user_id=usr.id))#if user exists then render user home
        else:
            return render_template("login.html",error="Invalid Username or Password")
    return render_template("login.html" , error="")# If GET request  show login page,you can write it in the starting of the code also before if statement lekin fir apko if ya else ka use karke request.method ka use karna padega usme bolna padega if request.method == "GET" then do this .




@app.route("/register",methods=["GET","POST"])#listen i can give any name as a route in paranthesis it's not necessary to give name as of html page
def register():#here i want to submit the data given by user in form in my database also
    if request.method == "POST":
        usr_email = request.form.get("email")#in this variable usr_email i am storing the value of email and name of this variable can be anything
        usr_password = request.form.get("password")
        usr_fullname = request.form.get("fullname")
        usr_address = request.form.get("address")
        usr_pincode = request.form.get("pincode")
        mail=Admin_User_Details.query.filter_by(email=usr_email).first()#to check whether mail given in form by user is present in database or not,if it is present then we will say user already exists...
        if mail:
            return render_template("register.html",message="User Already Exists")
        else:
            usr=Admin_User_Details(email=usr_email,password=usr_password,full_name=usr_fullname,address=usr_address,pincode=usr_pincode)#idhar mai ek record/object banake usr naam ka usme batata huu konsa table hai aur konsa column me kya hai
            db.session.add(usr)#This adds a new object (usr) to the database session,It does not yet save the data to the actual database file,it only adds the object to the session.
            db.session.commit()#This saves all changes from the session into the database.It makes the changes permanent in the database.
            # return redirect(url_for("login" , success_msg="Registration Successfull , Login to Continue"))
            return render_template("login.html",success_msg="Registration Successfull , Login to Continue")

    return render_template("register.html")



@app.route("/admin_home")
def admin_home():
    parking_lots = Parking_Lots.query.all()
    lot_data = []

    for lot in parking_lots:
        spots = Parking_Spots.query.filter_by(lot_id=lot.id).all()
        lot_data.append({
            'lot': lot,
            'spots': spots,
            'occupied_count': sum(1 for s in spots if s.status == 'occupied'),
            'total_count': len(spots)
        })

    return render_template("a_admin_dashboard.html", lot_data=lot_data)

@app.route("/admin_users")
def admin_users():
    users=Admin_User_Details.query.filter_by(role=1).all()
    return render_template("a_registered_users.html" , user=users)

# @app.route("/admin_search_functionality")
# def admin_search_functionality():
#     return render_template("a_search_page.html")


@app.route("/admin_summary")
def admin_summary():
    lots = Parking_Lots.query.all()

    revenue_data = []
    occupancy_labels = []
    occupied_data = []
    available_data = []

    for lot in lots:
        lot_name = lot.prime_location_name
        price = lot.price_per_spot_per_hour

        total_revenue = sum(res.parking_price_per_hour for res in Reserved_parking_spots.query.filter_by(lot_id=lot.id).all())
        spots = Parking_Spots.query.filter_by(lot_id=lot.id).all()
        occupied = sum(1 for s in spots if s.status == 'occupied')
        available = sum(1 for s in spots if s.status == 'available')

        revenue_data.append({'lot_name': lot_name, 'revenue': total_revenue})
        occupancy_labels.append(lot_name)
        occupied_data.append(occupied)
        available_data.append(available)

    return render_template("a_admin_summary.html",
                           revenue_data=revenue_data,
                           occupancy_labels=occupancy_labels,
                           occupied_data=occupied_data,
                           available_data=available_data)


@app.route("/admin_profile" , methods=["GET","POST"])
def admin_profile():
    if request.method == "POST":
        admin_email=request.form.get("email")
        admin_full_name=request.form.get("full_name")
        admin_password=request.form.get("password")
        admin_pincode=request.form.get("pincode")
        admin_address=request.form.get("address")
        admin=Admin_User_Details.query.filter_by(role=0).first()
        admin.email=admin_email
        admin.full_name=admin_full_name
        admin.password=admin_password
        admin.pincode=admin_pincode
        admin.address=admin_address
        db.session.commit()
        return redirect(url_for("admin_home"))
    admin=Admin_User_Details.query.filter_by(role=0).first()
    return render_template("a_profile.html" , admin=admin)



@app.route("/add_lot" , methods=["GET","POST"])
def add_lot():
    if request.method == "POST":
        prime_location=request.form.get("location")
        address=request.form.get("address")
        pincode=request.form.get("pincode")
        price=request.form.get("price")
        max_spots=request.form.get("max_spots")
        parking_lot=Parking_Lots.query.filter_by(prime_location_name=prime_location).first()#case sensitive
        if (parking_lot==""):
            return render_template("a_add_parking_lot.html",message="Bhai koi Parking Lot to fill kar lo")
        elif parking_lot:
            return render_template("a_add_parking_lot.html",message="Parking Lot Already Exists")
        else:
            lot=Parking_Lots(prime_location_name=prime_location,address=address,pincode=pincode,price_per_spot_per_hour=price,max_spots=max_spots)
            db.session.add(lot)
            db.session.commit()
            # Create empty parking spots
            # Jab tu naya lot add karega (e.g. Palwal, 10 spots), to backend me 10 Parking_Spots rows banengi — status = available.
            # Admin dashboard me har spot dikhega (Spot 1, 2, 3...).
            # Jo occupied honge wo red background se dikhenge.
            for i in range(int(max_spots)):
                spot = Parking_Spots(lot_id=lot.id, status="available")
                db.session.add(spot)
            db.session.commit()
            return redirect(url_for("admin_home"))

    return render_template("a_add_parking_lot.html")


@app.route("/edit_lot/<int:lot_id>" , methods=["GET","POST"])
def edit_lot(lot_id):
    parking_lot=Parking_Lots.query.filter_by(id=lot_id).first()
    if request.method == "POST":
        location=request.form.get("location")
        address=request.form.get("address")
        pincode=request.form.get("pincode")
        price=request.form.get("price")
        new_max_spots=int(request.form.get("max_spots"))

        old_max_spots=parking_lot.max_spots
         # Update the parking lot        
        parking_lot.prime_location_name=location
        parking_lot.address=address
        parking_lot.pincode=pincode
        parking_lot.price_per_spot_per_hour=price
        parking_lot.max_spots=new_max_spots
        db.session.commit()

         # Get all spots
        all_spots = Parking_Spots.query.filter_by(lot_id=lot_id).order_by(Parking_Spots.id.desc()).all()
        occupied_count = sum(1 for spot in all_spots if spot.status == "occupied")
        available_spots = [s for s in all_spots if s.status == "available"]
        
         #  Safe Check Before Reducing
        if new_max_spots < occupied_count:
            return render_template("a_edit_parking_lot.html", lot=parking_lot,
                                   message=f"Cannot reduce to {new_max_spots} spots. {occupied_count} spots are currently occupied.")

        # #  Safe Check Before Reducing
        # if new_max_spots < len(available_spots):
        #     return render_template("a_edit_parking_lot.html", lot=parking_lot,
        #                            message=f"Cannot reduce to {new_max_spots} spots. There are {len(available_spots)} available spots.")
         #  Now save the new max value
        parking_lot.max_spots = new_max_spots
        db.session.commit()



        # If max_spots increased, add new spots
        if new_max_spots > old_max_spots:
            for _ in range(new_max_spots - old_max_spots):
                new_spot = Parking_Spots(lot_id=parking_lot.id, status="available")
                db.session.add(new_spot)
            db.session.commit()


         #  Remove extra available spots if decreased
        elif new_max_spots < old_max_spots:
            # Get all spots of this lot ordered by latest created (highest id)
            all_spots = Parking_Spots.query.filter_by(lot_id=lot_id).order_by(Parking_Spots.id.desc()).all()
            # Count how many to delete
            spots_to_remove = old_max_spots - new_max_spots
            deleted_count = 0

            for spot in all_spots:
                if spot.status == "available":
                    db.session.delete(spot)
                    deleted_count += 1
                if deleted_count >= spots_to_remove:
                    break

            db.session.commit()

        return redirect(url_for("admin_home"))
    
        
    return render_template("a_edit_parking_lot.html" , lot=parking_lot)


@app.route("/delete_lot/<int:lot_id>")#mere bhai abhi delete incomplete hai ,kyoki abki baar aap parking lot ko jabhi delete kar sako jab sarre parking spot khali honge....
def delete_lot(lot_id):
    lot=Parking_Lots.query.filter_by(id=lot_id).first()
    db.session.delete(lot)
    db.session.commit()
    return redirect(url_for("admin_home"))




@app.route("/user_home/<int:user_id>", methods=["GET"])
def user_home(user_id):
    # User's recent reservations (latest 5)
    parking_history = Reserved_parking_spots.query \
        .filter_by(user_id=user_id) \
        .order_by(Reserved_parking_spots.parking_timestamp.desc()) \
        .limit(5).all()

    # Search logic
    search_query = request.args.get("search", "")
    if search_query:
        lots = Parking_Lots.query.filter(
            (Parking_Lots.prime_location_name.ilike(f"%{search_query}%")) |
            (Parking_Lots.pincode.ilike(f"%{search_query}%"))
        ).all()
    else:
        lots = Parking_Lots.query.all()

    # This block should be outside of if-else
    available_lots = []
    for lot in lots:
        available_spot = Parking_Spots.query.filter_by(lot_id=lot.id, status="available").first()
        if available_spot:
            lot.available_count = Parking_Spots.query.filter_by(lot_id=lot.id, status="available").count()
            lot.available_spot_id = available_spot.id
            available_lots.append(lot)

    return render_template(
        "u_user_dashboard.html",
        user_id=user_id,
        parking_history=parking_history,
        available_lots=available_lots,
        search_query=search_query
    )



@app.route("/user_summary/<int:user_id>")
def user_summary(user_id):
    from sqlalchemy import func

    # Query to get count of reservations grouped by lot
    usage_stats = (
        db.session.query(Parking_Lots.prime_location_name, func.count().label("count"))
        .join(Reserved_parking_spots, Reserved_parking_spots.lot_id == Parking_Lots.id)
        .filter(Reserved_parking_spots.user_id == user_id)
        .group_by(Parking_Lots.prime_location_name)
        .all()
    )

    lot_names = [lot for lot, _ in usage_stats]
    usage_counts = [count for _, count in usage_stats]

    return render_template(
        "u_user_summary.html",
        user_id=user_id,
        lot_names=lot_names,
        usage_counts=usage_counts
    )

@app.route("/user_profile/<int:user_id>" , methods=["GET","POST"])
def user_profile(user_id):
    if request.method == "POST":
        email=request.form.get("email")
        full_name=request.form.get("full_name")
        password=request.form.get("password")
        address=request.form.get("address")
        pincode=request.form.get("pincode")
        usr=Admin_User_Details.query.filter_by(id=user_id).first()
        usr.email=email
        usr.full_name=full_name
        usr.password=password
        usr.address=address
        usr.pincode=pincode
        db.session.commit()
        return redirect(url_for("user_home" , user_id=user_id))
    usr=Admin_User_Details.query.filter_by(id=user_id).first()
    return render_template("u_profile.html", user_id=user_id , user=usr)

@app.route("/book_spot", methods=["POST"])
def book_parking_spot():
    spot_id = int(request.form.get("spot_id"))
    lot_id = int(request.form.get("lot_id"))
    user_id = request.form.get("user_id")
    vehicle_number = request.form.get("vehicle_number")

    # Spot ko occupied karo
    spot = Parking_Spots.query.get(spot_id)
    if not spot or spot.status == "occupied":
        return "Spot already occupied or not found", 400

    spot.status = "occupied"

    # Lot se price le lo
    lot = Parking_Lots.query.get(lot_id)
    price = lot.price_per_spot_per_hour

    # New reservation
    reservation = Reserved_parking_spots(
        spot_id=spot_id,
        lot_id=lot_id,
        user_id=user_id,
        vehicle_number=vehicle_number,
        parking_timestamp=datetime.now(),
        parking_price_per_hour=price
    )

    db.session.add(reservation)
    db.session.commit()

    return redirect(url_for('user_home', user_id=user_id))


@app.route("/book/<int:spot_id>/<int:lot_id>/<user_id>", methods=["GET"])
def render_booking_form(spot_id, lot_id, user_id):
    return render_template("u_book_the_parking_spot.html", spot_id=spot_id, lot_id=lot_id, user_id=user_id)


@app.route("/release_spot/<int:reservation_id>", methods=["POST"])
def release_spot(reservation_id):
    reservation = Reserved_parking_spots.query.get(reservation_id)

    if not reservation or reservation.leaving_timestamp:
        flash("Reservation not found or already released.")
        return redirect(url_for("user_home", user_id=reservation.user_id))

    # Update leaving timestamp
    reservation.leaving_timestamp = datetime.now()

    # Mark the spot as available again
    spot = Parking_Spots.query.get(reservation.spot_id)
    if spot:
        spot.status = "available"

    db.session.commit()

    flash("Spot released successfully!")
    return redirect(url_for("user_home", user_id=reservation.user_id))

@app.route("/admin_search_functionality", methods=["GET"])
def admin_search_functionality():
    filter_type = request.args.get("filter")
    query = request.args.get("query")

    results = []

    if filter_type == "user_id":
        results = Reserved_parking_spots.query.filter_by(user_id=query).all()

    elif filter_type == "spot_id":
        results = Reserved_parking_spots.query.filter_by(spot_id=query).all()

    elif filter_type == "location":
        lots = Parking_Lots.query.filter(Parking_Lots.prime_location_name.ilike(f"%{query}%")).all()
        results = []
        for lot in lots:
            spots = Parking_Spots.query.filter_by(lot_id=lot.id).all()
            results.append({'lot': lot, 'spots': spots})

    return render_template("a_search_page.html", filter_type=filter_type, query=query, results=results)

