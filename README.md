# HMS
Hospital Management System Where Registration Desk Executive/Pharmacy/Diagnostic Executive can perform their respective operations.

#Registration Desk Executive :

Can Add, Delete or Updte Patient Record
Can Generate Entire Bill for the Sevices Taken by Patient like (Pharmacy, Diagnostic Test, Room Bill (Edit Room Bill price in views.py file and room type in forms.py file)


#Pharmacy :
can Add Medicine
Can Issue Medicines for Active Patients
Can generate Pharmacy Bill

#Diagnostic Executive:
Can Add Diagnotic tests
Can Issue Diagnostic Test to Patients
Can generate Diagnostic test bill

#Usage:
Install requirements. text by running
pip install -r requirements.txt

Run powershell or Command prompt as administrator and run :

flask db init

flask db migrate

flask db upgrade

Above lines are important for code to run

Now run python app.py (Note that debug is set to True)

Go to 127.0.0.1:5000 (Unless you specified a default Port number)

Register new User

Based on the role you will be logged in to that particular screens (Different for every role)
