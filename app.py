
from flask import Flask, render_template, redirect, request
import requests
import bs4
app = Flask(__name__)


def converter(d):
    if d == "A+":
        return 4.00
    elif d == "A":
        return 3.75
    elif d == "A-":
        return 3.50
    elif d == "B+":
        return 3.25
    elif d == "B":
        return 3.00
    elif d == "B-":
        return 2.75
    elif d == "C+":
        return 2.50
    elif d == "C":
        return 2.25
    elif d == "D":
        return 2.00
    elif d == "F":
        return 0.00


@app.route('/result')
def result():
    render_template('result.html')


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        id = request.form.get('uname')
        ps = request.form.get('psw')
        Table = ''
        Result = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }
        login_data = {
            'user_email': id,
            'user_password': ps,
            'loginuser': 'Sign In'
        }
        with requests.Session() as s:
            url = "https://course.cuet.ac.bd/index.php"
            r = s.get(url, headers=headers)
            r = s.post(url, data=login_data,
                       headers=headers)
            r = s.get(
                "https://course.cuet.ac.bd/result_published.php", headers=headers)
            g = bs4.BeautifulSoup(r.text, 'lxml')

            Table = g.table
            if Table is not None:
                row = Table.find_all('tr')
                for tr in row:
                    td = tr.find_all('td')
                    rw = [i.text for i in td]
                    Result.append(rw)
                Result = Result[1:]
                term_wise_data = {}
                for i in Result:
                    if i[2] not in term_wise_data:
                        term_wise_data[i[2]] = []
                        credit = float(i[1])
                        grade = converter(i[4])
                        prod = credit*grade
                        fail_credit = 0.0
                        if i[4] == "F":
                            fail_credit = float(i[1])
                        term_wise_data[i[2]].append(credit)
                        term_wise_data[i[2]].append(prod)
                        term_wise_data[i[2]].append(fail_credit)
                    else:
                        credit = float(i[1])
                        grade = converter(i[4])
                        prod = credit*grade
                        fail_credit = 0.0
                        if i[4] == "F":
                            fail_credit = float(i[1])
                        term_wise_data[i[2]
                                       ][0] = term_wise_data[i[2]][0]+credit
                        term_wise_data[i[2]][1] = term_wise_data[i[2]][1]+prod
                        term_wise_data[i[2]
                                       ][2] = term_wise_data[i[2]][2]+fail_credit
                for i in term_wise_data:
                    term_wise_data[i].append(
                        round(term_wise_data[i][1]/(term_wise_data[i][0] - term_wise_data[i][2]), 2))
                sm = 0
                fail = 0
                totalcredit = 0
                sd = 0
                sgpa = []
                level = []
                for i in term_wise_data:
                    sm = sm + term_wise_data[i][1]
                    fail = fail + term_wise_data[i][2]
                    totalcredit = totalcredit + term_wise_data[i][0]
                    sd = sd + term_wise_data[i][0]*term_wise_data[i][3]
                    d = []
                    d.append(i)
                    d.append(term_wise_data[i][3])
                    sgpa.append(d)
                try:
                    cgpa = round(sm/(totalcredit - fail), 2)
                except:
                    cgpa = 0
                tc = (totalcredit - fail)
                return render_template('result.html', tables=sgpa, a=len(sgpa), b=tc, c=cgpa, tables1=Result)
            else:
                return render_template('index.html', msg='Wrong Password!!!')

    else:
        return render_template('index.html', msg="")


@app.errorhandler(404)
def page_not_found(e):
    return '<h1>Page not Found<h1>'


if __name__ == "__main__":
    app.run()

# arif
