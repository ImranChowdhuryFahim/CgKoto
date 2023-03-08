from flask import Flask, render_template, request
import requests
import bs4
app = Flask(__name__)


def gradePointConverter(gradeLetter):
    if gradeLetter == "A+":
        return 4.00
    elif gradeLetter == "A":
        return 3.75
    elif gradeLetter == "A-":
        return 3.50
    elif gradeLetter == "B+":
        return 3.25
    elif gradeLetter == "B":
        return 3.00
    elif gradeLetter == "B-":
        return 2.75
    elif gradeLetter == "C+":
        return 2.50
    elif gradeLetter == "C":
        return 2.25
    elif gradeLetter == "D":
        return 2.00
    elif gradeLetter == "F":
        return 0.00


@app.route('/result')
def result():
    render_template('result.html')


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        studentID = request.form.get('uname')
        password = request.form.get('psw')
        tableData = ''
        resultData = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }
        login_data = {
            'user_email': studentID,
            'user_password': password,
            'loginuser': 'Sign In'
        }
        with requests.Session() as session:
            url = "https://course.cuet.ac.bd/index.php"
            response = session.get(url, headers=headers)
            response = session.post(url, data=login_data,
                       headers=headers)
            response = session.get(
                "https://course.cuet.ac.bd/result_published.php", headers=headers)
            processedResponse = bs4.BeautifulSoup(response.text, 'lxml')

            tableData = processedResponse.table
            if tableData is not None:
                row = tableData.find_all('tr')
                for tr in row:
                    td = tr.find_all('td')
                    row_data = [i.text for i in td]
                    resultData.append(row_data)
                resultData = resultData[1:]
                semester_wise_data = {}
                for i in resultData:
                    if i[2] not in semester_wise_data:
                        semester_wise_data[i[2]] = []
                        credit = float(i[1])
                        gradePoint = gradePointConverter(i[4])
                        weightedGrade = credit*gradePoint
                        fail_credit = 0.0
                        if i[4] == "F":
                            fail_credit = float(i[1])
                        semester_wise_data[i[2]].append(credit)
                        semester_wise_data[i[2]].append(weightedGrade)
                        semester_wise_data[i[2]].append(fail_credit)
                    else:
                        credit = float(i[1])
                        gradePoint = gradePointConverter(i[4])
                        weightedGrade = credit*gradePoint
                        fail_credit = 0.0
                        if i[4] == "F":
                            fail_credit = float(i[1])
                        semester_wise_data[i[2]
                                       ][0] = semester_wise_data[i[2]][0]+credit
                        semester_wise_data[i[2]][1] = semester_wise_data[i[2]][1]+weightedGrade
                        semester_wise_data[i[2]
                                       ][2] = semester_wise_data[i[2]][2]+fail_credit
                for i in semester_wise_data:
                    semester_wise_data[i].append(
                        round(semester_wise_data[i][1]/(semester_wise_data[i][0] - semester_wise_data[i][2]), 2))

                totalWeightedPassedCredit= 0
                totalFailedCredit = 0
                totalCredit = 0
                semester_wise_cgpa = []
                for i in semester_wise_data:
                    totalWeightedPassedCredit = totalWeightedPassedCredit + semester_wise_data[i][1]
                    totalFailedCredit = totalFailedCredit + semester_wise_data[i][2]
                    totalCredit = totalCredit + semester_wise_data[i][0]
                    d = []
                    d.append(i)
                    d.append(semester_wise_data[i][3])
                    semester_wise_cgpa.append(d)
                try:
                    cgpa = round(totalWeightedPassedCredit/(totalCredit - totalFailedCredit), 2)
                except:
                    cgpa = 0
                totalPassedCredit = (totalCredit - totalFailedCredit)
                return render_template('result.html', semester_wise_cgpa_data=semester_wise_cgpa, number_of_semesters=len(semester_wise_cgpa), totalPassedCredit=totalPassedCredit, CGPA=cgpa, resultData=resultData)
            else:
                return render_template('index.html', msg='Wrong Password!!!')

    else:
        return render_template('index.html', msg="")


@app.errorhandler(404)
def page_not_found(e):
    return '<h1>Page not Found<h1>'


if __name__ == "__main__":
    app.run(host='0.0.0.0')

