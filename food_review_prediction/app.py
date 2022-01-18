from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from datetime import datetime
import pickle


client = MongoClient('mongodb+srv://pavan:Pavan$ai@cluster0.ymwrn.mongodb.net/test')
db = client.get_database('aravind')
login = db.login
reviews = db.review

app = Flask(__name__)
app.secret_key = 'any randon key'


@app.route("/")
def imfint():
    session['seq'] = 'one'

    return render_template("welcome.html")


@app.route("/sign")
def imfint2():
    return render_template("signup.html")


@app.route("/admin", methods=["POST", "GET"])
def logins():
    if request.method == 'POST':
        if request.form.get('uname') == 'admin' or request.form.get('uname') == 'admin2' or request.form.get(
                'perks') == 'admin':
            ver = reviews.find({}, {"_id": 0, "Name": 1, "Item": 1, "Review": 1, "Entry_time": 1, "Entry_date": 1,
                                    "Status": 1}).sort("_id", -1)

            ver2 = reviews.find({}, {"_id": 0, "Name": 1, "Item": 1, "Review": 1, "Entry_time": 1, "Entry_date": 1,
                                     "Status": 1, "Mail": 1, "Phone": 1}).sort("_id", -1)
            ver3 = reviews.find({}, {"_id": 0, "Name": 1, "Item": 1, "Review": 1, "Entry_time": 1, "Entry_date": 1,
                                     "Status": 1}).sort("_id", -1)

            # Items reviews
            ver4 = reviews.find({"Item": "Veggie -paradise"},
                                {"_id": 0, "Name": 1, "Item": 1, "Review": 1, "Entry_time": 1, "Entry_date": 1,
                                 "Status": 1}).sort("_id", -1)
            ver5 = reviews.find({"Item": "Margherita"},
                                {"_id": 0, "Name": 1, "Item": 1, "Review": 1, "Entry_time": 1, "Entry_date": 1,
                                 "Status": 1}).sort("_id", -1)
            ver6 = reviews.find({"Item": "Capricciosa"},
                                {"_id": 0, "Name": 1, "Item": 1, "Review": 1, "Entry_time": 1, "Entry_date": 1,
                                 "Status": 1}).sort("_id", -1)
            ver7 = reviews.find({"Item": "Cheesy-Delight"},
                                {"_id": 0, "Name": 1, "Item": 1, "Review": 1, "Entry_time": 1, "Entry_date": 1,
                                 "Status": 1}).sort("_id", -1)
            ver8 = reviews.find({"Item": "Hawaiian"},
                                {"_id": 0, "Name": 1, "Item": 1, "Review": 1, "Entry_time": 1, "Entry_date": 1,
                                 "Status": 1}).sort("_id", -1)
            ver9 = reviews.find({"Item": "Caeasars pizza"},
                                {"_id": 0, "Name": 1, "Item": 1, "Review": 1, "Entry_time": 1, "Entry_date": 1,
                                 "Status": 1}).sort("_id", -1)

            bb = db.review.count()
            bc = db.review.distinct('Name')
            bc = len(bc)
            counts = countz(ver)
            counts = round(counts, 2)

            it1, it11 = countzz(ver4)
            it2, it22 = countzz(ver5)
            it3, it33 = countzz(ver6)
            it4, it44 = countzz(ver7)
            it5, it55 = countzz(ver8)
            it6, it66 = countzz(ver9)

            if request.form.get('uname') == 'admin':
                pv = 0
            elif request.form.get('uname') == 'admin2':
                pv = 1

            return render_template('dashboardbase.html', pv=pv, vers=ver2, versi=ver3, visit=bb, rati=counts, unq=bc,
                                   it1=it1, it2=it2, it3=it3, it4=it4, it5=it5, it6=it6, it11=it11, it22=it22,
                                   it33=it33, it44=it44, it55=it55, it66=it66)
        else:
            user = request.form.get('uname')
            phone = request.form.get('uphone')
            mail = request.form.get('umail')
            session['sequence1'] = user
            session['sequence3'] = phone
            session['sequence4'] = mail

            login.insert_many([{"Name": user, "Phone": phone, "Email": mail}])
            return render_template('flipcard.html')


def countz(ver):
    count = 0
    n = 0
    for x in ver:
        b = int(x["Status"])
        count = count + b
        n = n + 1
    try:
        count = count * 5 / n
        return count
    except:
        count = 0
        return count


def countzz(ver2):
    count = 0
    count2 = 0
    for x in ver2:
        if x["Status"] == 0:
            count = count + 1
        else:
            count2 = count2 + 1
    return count, count2


@app.route("/item", methods=["POST"])
def items():
    if request.method == 'POST':

        item = request.form.get('item')
        session['sequence2'] = item
        bver12 = reviews.find({}).sort("_id", -1).limit(15)
        verr = reviews.find({}, {"_id": 0, "Name": 1, "Item": 1, "Review": 1, "Entry_time": 1, "Entry_date": 1,
                                 "Status": 1}).sort("_id", -1)

        count = 0
        n = 0
        for x in verr:
            b = int(x["Status"])
            count = count + b
            n = n + 1
        try:
            count = count * 5 / n
            mn = int(count)
        except:
            count = 0
        mn = int(count)
        mm = 5 - mn

        return render_template('input.html', speec=bver12, cnts=mn, cnty=mm)


@app.route("/review", methods=["POST"])
def comment():
    if request.method == 'POST' and 'review' in request.form and session['seq'] == 'one':
        review = request.form.get('review')
        timing = datetime.now()
        timingdate = timing.strftime("%x")
        timingtime = timing.strftime("%X")
        user = session['sequence1']
        item = session['sequence2']
        phone = session['sequence3']
        mail = session['sequence4']
        session['seq'] = 'two'
        vectorizer = pickle.load(open("D://education//projects//minor 1//food_review_prediction//output//vector.pkl", "rb"))
        ve = pickle.load(open("D://education//projects//minor 1//food_review_prediction//output//model.pkl", "rb"))
        gg = vectorizer.transform([review])
        fg = ve.predict(gg)
        fg = str(fg[0])
        fg = int(fg)

        reviews.insert_many([{"Name": user, "Item": item, "Review": review, "Status": fg, "Mail": mail, "Phone": phone,
                              "Entry_time": timingtime, "Entry_date": timingdate}])
        return render_template('thank.html')
    else:
        return '<h1>Please return to home page</h1>'


@app.route("/profile")
def toprofile():
    return render_template('profile.html')


@app.route("/homed")
def tohome():
    return render_template('signup.html')


if __name__ == "__main__":
    app.run(debug=True)
