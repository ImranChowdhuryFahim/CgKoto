Table=g.table
            # if Table is not None:
            #     row=Table.find_all('tr')
            #     for tr in row:
            #         td=tr.find_all('td') 
            #         rw=[i.text for i in td]
            #         Result.append(rw)
            #     Result=Result[1:]
            #     term_wise_data={}
            #     for i in Result:
            #         if i[2] not in term_wise_data:
            #             term_wise_data[i[2]]=[]
            #             credit=float(i[1])
            #             grade=converter(i[4])
            #             prod=credit*grade
            #             fail_credit=0.0
            #             if i[4]=="F":
            #                 fail_credit=float(i[1])
            #             term_wise_data[i[2]].append(credit)
            #             term_wise_data[i[2]].append(prod)
            #             term_wise_data[i[2]].append(fail_credit)
            #         else:
            #             credit=float(i[1])
            #             grade=converter(i[4])
            #             prod=credit*grade
            #             fail_credit=0.0
            #             if i[4]=="F":
            #                 fail_credit=float(i[1])
            #             term_wise_data[i[2]][0]=term_wise_data[i[2]][0]+credit
            #             term_wise_data[i[2]][1]=term_wise_data[i[2]][1]+prod
            #             term_wise_data[i[2]][2]=term_wise_data[i[2]][2]+fail_credit
            #     for i in term_wise_data:
            #         term_wise_data[i].append(round(term_wise_data[i][1]/(term_wise_data[i][0] - term_wise_data[i][2]),2))
            #     sm=0
            #     fail=0
            #     totalcredit=0
            #     sd=0
            #     sgpa=[]
            #     level=[]
            #     for i in term_wise_data:
            #         sm= sm+ term_wise_data[i][1]
            #         fail= fail+ term_wise_data[i][2]
            #         totalcredit= totalcredit + term_wise_data[i][0]
            #         sd= sd+ term_wise_data[i][0]*term_wise_data[i][3]
            #         d=[]
            #         d.append(i)
            #         d.append(term_wise_data[i][3])
            #         sgpa.append(d)
            #     try:
            #        cgpa=round(sm/(totalcredit - fail),2)
            #     except:
            #         cgpa = 0
            #     tc=(totalcredit - fail)
            #     return render_template('result.html',tables=sgpa,a=len(sgpa),b=tc,c=cgpa,tables1=Result)
            # else:
            #     return render_template('index.html',msg='Wrong Password!!!')