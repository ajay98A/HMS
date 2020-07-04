from project import app,db
from flask import render_template,url_for,flash,redirect,request,abort,current_app
from flask_login import login_user,logout_user,login_required,current_user
from project.models import User,Patient,MedicineMaster,Medicines,DiagnosticsMaster,Diagnostics
from project.application.forms import (LoginForm,RegistrationForm,AddPatient,SearchForm,
                                       DeletePatient,UpdateForm,MedicineForm,medicineissue,billingForm,
                                       AddDiagForm,DiagnosticIssue,diag_bill,pharma_bill)
import wtforms
from functools import wraps
from datetime import datetime
def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.urole == permission:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome.html')
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You are logged out..!")
    return redirect(url_for('home'))

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is not None and user.check_password(form.password.data):

            login_user(user)
            flash("Logged in successfully.!")
            next = request.args.get('next')

            if next == None or next[0] == '/':
                next = url_for('home')
            return redirect(next)
        else:
            flash("Invalid Credentials")
            return redirect(url_for('login'))
    return render_template('login.html',form=form)


@app.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        uname = form.username.data
        if User.query.filter_by(username=uname).first():
            flash("Username exists !")
            return redirect(url_for('register'))
        user = User(username=form.username.data,password=form.password.data,urole=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash("Registered!")
        return redirect(url_for('welcome_user'))

    return render_template('register.html',form=form)

@app.route('/add-patient',methods=['GET','POST'])
@login_required
@permission_required("staff")
def addpatient():
    form = AddPatient()
    if form.validate_on_submit():
        if Patient.query.filter_by(ssn_id=form.ssn_id.data).first():
            flash("SSN Id Exists")
            return redirect(url_for('addpatient'))
        ssn_id_check = form.ssn_id.data
        if len(str(ssn_id_check)) < 9:
            flash("SSN Id must be 9 digits")
            return redirect(url_for('addpatient'))
        s = form.name.data
        if not all(x.isalpha() or x.isspace() for x in s):
            flash("Only alphabets are allowed in name, Enter details again")
            return redirect(url_for('addpatient'))
        s = form.Address.data
        if not all(x.isalnum() or x.isspace() for x in s):
            flash("Only Alphanumeric characters allowed in Address, no special characters")
            return redirect(url_for('addpatient'))
        age_check =form.age.data
        if len(str(age_check)) < 2 or len(str(age_check)) > 3:
            flash("Enter Age in 2 digits and no more than 3 digits")
            return redirect(url_for('addpatient'))
        patient_add = Patient(ssn_id=form.ssn_id.data,
                              name=form.name.data,
                              age=form.age.data,
                              address=form.Address.data,
                              bed_type=form.bed_type.data,
                              date = form.date.data,
                              city=form.city.data,
                              state=form.state.data,
                              status=form.status.data)
        db.session.add(patient_add)
        db.session.commit()
        flash('Patient Added')
        return redirect(url_for('viewpatient'))
    return render_template('add-patient.html',form=form)

@app.route('/view-patient',methods=['GET'])
@login_required
@permission_required("staff")
def viewpatient():
    data = Patient.query.all()
    return render_template("view-patient.html",data=data)

@app.route('/search-patient',methods=['GET','POST'])
@login_required
@permission_required("staff")
def searchpatient():
    form = SearchForm()
    if form.validate_on_submit():
        id = form.pid.data
        item = Patient.query.filter_by(id = id).first()
        if item:
            id = item.id
            ssn_id = item.ssn_id
            name = item.name
            age = item.age
            address = item.address
            city = item.city
            state = item.state
            return render_template("search-patient.html",form=form,id=id,ssn_id=ssn_id,name=name,age=age,
                                   address=address,city=city,state=state)
        else:
            flash("Not Found..!!")

    return render_template("search-patient.html",form=form)

@app.route('/delete-patient',methods=['GET','POST'])
@login_required
@permission_required("staff")
def deletepatient():
    form = DeletePatient()
    if form.validate_on_submit():
        id = form.pid.data
        item = Patient.query.get(id)
        if item:
            return render_template('delete-patient.html',form=form,item=item)
        else:
            flash("Patient Not Found")
    return render_template("delete-patient.html",form=form)
@app.route('/delete-patient2/<pid>',methods=['GET','POST'])
@login_required
@permission_required("staff")
def deletepatient2(pid):
    pat_det = Patient.query.get(pid)
    if pat_det:
        db.session.delete(pat_det)
        db.session.commit()
        flash('Record is deleted')
        return redirect(url_for('viewpatient'))
    if pat_det == None:
        flash('Patient Record Not Found, Please try again')
        return redirect(url_for('deletepatient'))

@app.route('/update-patient',methods=['GET','POST'])
@login_required
@permission_required("staff")
def UpdatePatient():
    form = UpdateForm()
    if form.validate_on_submit():
        id = form.pid.data
        item = Patient.query.get(id)
        s = form.Address.data
        if not all(x.isalnum() or x.isspace() for x in s):
            flash("Only Alphanumeric characters allowed in Address, no special characters")
            return redirect(url_for('UpdatePatient'))
        if item:
            if form.name.data != "" :
                item.name = form.name.data
            if form.age.data != "" :
                item.age = form.age.data
            if form.Address.data != "" :
                item.address = form.Address.data
            if form.city.data != "" :
                item.city = form.city.data
            if form.state.data != "" :
                item.state = form.state.data
            item.bed_type = form.bed_type.data
            item.status = form.status.data
            db.session.commit()
            flash('Patient Details Updated')
            return redirect(url_for('viewpatient'))

        else:
            flash("Patient Not Found")
    return render_template("update-patient.html",form=form)

@app.route('/patient-billing', methods=['GET', 'POST'])
@login_required
@permission_required("staff")
def Pbilling():
    #today = datetime.today().strftime('%Y-%m-%d')
    form = billingForm()
    today = datetime.now()
    if form.validate_on_submit():
        id = form.id.data
        delta = 0
        if id != "":
            patient = Patient.query.filter_by( id = id).first()
            print(type(patient))
            med1 = Medicines.query.filter_by(pid = id).all()
            print(type(med1))
            med2 = Diagnostics.query.filter_by(pid = id).all()
            print(type(med2))

            if patient == None:
                flash('No Patients with that this ID exists')
                return redirect( url_for('Pbilling') )
            elif patient.status != 'Active':
                flash('No Active Patients')

            else:
                flash('Patient Found')
                x = patient.date
                y = x.strftime("%d-%m-%Y, %H:%M:%S")
                # z = today.strftime("%d-%m-%Y")
                # print("Patient ",y)
                # print("today", z)
                delta = ( today - x ).days
                print(delta)
                dy = 0
                if delta == 0:
                    dy = 1
                else:
                    dy = delta
                roomtype = patient.bed_type
                bill = 0
                print(roomtype)
                if roomtype == 'SingleRoom':
                    bill = 8000 * dy
                elif roomtype == 'SemiSharing':
                    bill = 4000 * dy
                else:
                    bill = 2000 * dy
                if not med1 and not med2:
                    return render_template('billing.html', form=form,patient = patient, delta=delta, y=y, bill = bill)
                if med1:
                    price = []
                    for i in med1:
                        price.append(i.rate*i.qissued)
                    print(price)
                if med2:
                    price2 = []
                    for i in med2:
                        price2.append(i.charge)
                    print(price2)
                    if med1 and med2:
                        return render_template("billing.html",form=form,patient = patient,med1=med1,med2=med2,price=sum(price),price2=sum(price2),delta=delta, y=y, bill = bill)
                    else:
                        return render_template("billing.html",form=form,patient = patient,med2=med2,price2=sum(price2),delta=delta, y=y, bill = bill)
                else:
                    return render_template("billing.html",form=form,patient = patient,price=sum(price),med1=med1,delta=delta, y=y, bill = bill)
        if id == "":
            flash('Enter  id to search patient')
            return redirect( url_for('billing') )


    return render_template("billing.html",form=form)



@app.route('/pharma-view-patient',methods=['GET','POST'])
@login_required
@permission_required("pharma")
def ViewDetails():
    form = SearchForm()
    if form.validate_on_submit():
        id = form.pid.data
        item = Patient.query.get(id)
        if item:
            id = item.id
            ssn_id = item.ssn_id
            name = item.name
            age = item.age
            address = item.address
            city = item.city
            state = item.state
            med = Medicines.query.filter_by(pid = id).all()
            if med == None:
                flash('No Medicines issued to Patient till Now')
                return render_template('pharma-view-patient.html', item=item,form = form,id=id,ssn_id=ssn_id,name=name,age=age,
                                       address=address,city=city,state=state )
            else:
                return render_template('pharma-view-patient.html',item=item,form=form, id=id,ssn_id=ssn_id,name=name,age=age,
                                       address=address,city=city,state=state,med = med)

        else:
            flash("Not Found..!!")
    return render_template("pharma-view-patient.html",form=form)

@app.route('/pharma-search-patient',methods=['GET','POST'])
@login_required
@permission_required("pharma")
def Pharmaviewpatient():
    data = Patient.query.all()
    return render_template("pharma-current-patients.html",data=data)

@app.route('/View-Medicines',methods=['GET'])
@login_required
@permission_required("pharma")
def ViewMedicine():
    data = MedicineMaster.query.all()
    return render_template("Medicine-data.html",data=data)

@app.route('/add-medicine',methods=['GET','POST'])
@login_required
@permission_required("pharma")
def AddMedicine():
    form = MedicineForm()
    if form.validate_on_submit():
        mid = form.mid.data
        mname = form.mname.data
        qavailable = form.qavailable.data
        rate = form.rate.data
        pat = MedicineMaster.query.filter_by( mid = mid ).first()

        if pat == None:
            med = MedicineMaster(mid=mid, mname=mname, qavailable=qavailable, rate=rate)
            db.session.add(med)
            db.session.commit()
            flash('Medicine successfully Inserted to Database')
            return redirect( url_for('ViewMedicine') )

        else:
            flash('Medicine with this  ID already exists')
            return redirect( url_for('AddMedicine') )
    return render_template('add-medicine.html',form=form)

@app.route('/issue-medicine/<pid>',methods=['GET','POST'])
@login_required
@permission_required("pharma")
def IssueMedicine(pid):
    form = medicineissue()
    if form.validate_on_submit():
        patient_details = Patient.query.get(pid)
        mname = form.name.data
        if mname != "":
            patient = MedicineMaster.query.filter_by( mname = mname).first()
            if patient == None:
                flash('No Medicine with this Name exists')
                return render_template('issuemedicine.html',form=form,patient_details=patient_details)
            else:
                flash('Medicine found”')
                qissued = form.qissued.data
                qid = int(qissued)
                print( type(qid) )
                print((patient.qavailable) - qid)
                if(qid > patient.qavailable):
                    flash("Selected Medicine Quantity Unavailable")
                    return render_template('issuemedicine.html', form=form,patient = patient,patient_details=patient_details)
                else:
                    patient.qavailable = patient.qavailable - qid
                    db.session.commit()
                    mid = patient.mid
                    rate = patient.rate
                    rowup = Medicines( mid = mid, pid=pid, mname = mname, rate = rate , qissued=qissued)
                    db.session.add(rowup)
                    db.session.commit()
                    flash("Issued")
                    return render_template('issuemedicine.html', form=form,patient = patient,patient_details=patient_details)
        if mname == "":
            flash('Enter  Medicine Name to Search')
            return render_template('issuemedicine.html',form=form)

    return render_template('issuemedicine.html',form=form)
@app.route('/pharma-view-bill',methods=['GET','POST'])
@login_required
@permission_required("pharma")
def PharmaBill():
    form = pharma_bill()
    if form.validate_on_submit():
        id = form.pid.data
        item = Patient.query.get(id)
        if item:
            id = item.id
            ssn_id = item.ssn_id
            name = item.name
            age = item.age
            address = item.address
            city = item.city
            state = item.state
        else:
            flash('Not Found..!!')
            return render_template("pharma-view-bill.html",form=form)

        med = Medicines.query.filter_by(pid = id).all()
        patient_details = [id,ssn_id,name,age,address,city,state]
        if med:
            price = []
            for i in med:
                price.append(i.rate*i.qissued)
            print(price)
            return render_template("pharma-view-bill.html",form=form,med=med,price=sum(price),patient_details=patient_details)
        else:
            flash('Medicines Not found for this patient !')
            return render_template("pharma-view-bill.html",form=form,patient_details=patient_details)

    return render_template("pharma-view-bill.html",form=form)

@app.route('/view-diagnostic',methods=['GET','POST'])
@login_required
@permission_required("diag")
def ViewDiagnostics():
    data = DiagnosticsMaster.query.all()
    return render_template("Diagnostic-data.html",data=data)
@app.route('/add-diagnostic',methods=['GET','POST'])
@login_required
@permission_required("diag")
def AddDiag():
    form = AddDiagForm()
    if form.validate_on_submit():
        tid = form.tid.data
        tname = form.tname.data
        rate = form.rate.data
        pat = DiagnosticsMaster.query.filter_by( tid = tid ).first()

        if pat == None:
            d = DiagnosticsMaster(tid=tid, tname=tname, tcharge=rate)
            db.session.add(d)
            db.session.commit()
            flash('Diagnostics Service successfully Added')
            return redirect( url_for('ViewDiagnostics') )

        else:
            flash('Diagnostic Service with this  ID already exists')
            return redirect( url_for('AddDiag') )
    return render_template('add-diagnostic.html',form=form)

@app.route('/issue-diagnostic/<pid>',methods=['GET','POST'])
@login_required
@permission_required("diag")
def IssueDiag(pid):
    form = DiagnosticIssue()
    if form.validate_on_submit():
        patient_details = Patient.query.get(pid)
        tname = form.name.data
        if tname != "":
            patient = DiagnosticsMaster.query.filter_by( tname = tname).first()
            if patient == None:
                flash('No Diagnostic Service with this Name')
                return render_template('issuediagnostic.html',form=form,patient_details=patient_details)
            else:
                flash('Service Found”')
                tid = patient.tid
                rate = patient.tcharge
                rowup = Diagnostics( tid = tid, pid=pid, tname = tname, charge=rate)
                db.session.add(rowup)
                db.session.commit()
                flash("Issued")
                return render_template('issuediagnostic.html', form=form,patient = patient,patient_details=patient_details)
        if tname == "":
            flash('Enter  Diagnostic service name to Search')
            return render_template('issuediagnostic.html',form=form)

    return render_template('issuediagnostic.html',form=form)

@app.route('/diag-show-patient',methods=['GET','POST'])
@login_required
@permission_required("diag")
def Diagviewpatient():
    data = Patient.query.all()
    return render_template("diag-current-patients.html",data=data)


@app.route('/Diag-view-patient',methods=['GET','POST'])
@login_required
@permission_required("diag")
def ViewDetailsDiag():
    form = SearchForm()
    if form.validate_on_submit():
        id = form.pid.data
        item = Patient.query.get(id)
        if item:
            id = item.id
            ssn_id = item.ssn_id
            name = item.name
            age = item.age
            address = item.address
            city = item.city
            state = item.state
            med = Diagnostics.query.filter_by(pid = id).all()
            if med == None:
                flash('No Diagnostic Services issued to Patient till Now')
                return render_template('Diag-patients.html', item=item,form = form,id=id,ssn_id=ssn_id,name=name,age=age,
                                       address=address,city=city,state=state )
            else:
                return render_template('Diag-patients.html',item=item,form=form, id=id,ssn_id=ssn_id,name=name,age=age,
                                       address=address,city=city,state=state,med = med)

        else:
            flash("Not Found..!!")
    return render_template("Diag-patients.html",form=form)
@app.route('/Diag-view-bill',methods=['GET','POST'])
@login_required
@permission_required("diag")
def diagbill():
    form = diag_bill()
    if form.validate_on_submit():
        id = form.pid.data
        item = Patient.query.get(id)
        if item:
            id = item.id
            ssn_id = item.ssn_id
            name = item.name
            age = item.age
            address = item.address
            city = item.city
            state = item.state
        else:
            flash('Not Found..!!')
            return render_template("diag-view-bill.html",form=form)

        med = Diagnostics.query.filter_by(pid = id).all()
        patient_details = [id,ssn_id,name,age,address,city,state]
        if med:
            price = []
            for i in med:
                price.append(i.charge)
            print(price)
            return render_template("diag-view-bill.html",form=form,item=item,med=med,price=sum(price),patient_details=patient_details)
        else:
            flash('Diagnostic Not found for this patient !')
            return render_template("diag-view-bill.html",form=form,patient_details=patient_details)

    return render_template("diag-view-bill.html",form=form)

if __name__ == "__main__":
    app.run(debug=True)
