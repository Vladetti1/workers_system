import sqlite3
from flask import Flask, redirect, url_for, render_template, request, session
import wwb

wwb.start()

app = Flask(__name__)
app.secret_key = "r@ndrer0mSk_1"


@app.route("/")
def index():
    return render_template('login.html')


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        wwb.register(username, password, email)
        return redirect(url_for('index'))

    else:
        return render_template('register.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if wwb.login(username, password):
            session['username'] = username

        return redirect(url_for('home'))
    else:
        return redirect(url_for('index'))


@app.route('/home', methods=['POST', "GET"])
def home():
    if 'username' in session:

        email, role, date_reg = wwb.login_info(session['username'])
        session['role'] = role

        if role == "worker":
            return render_template('home_work.html', username=session['username'], email=email, role=role,
                                   date_reg=date_reg)
        elif role == "admin":
            return render_template('home_admin.html', username=session['username'], email=email, role=role,
                                   date_reg=date_reg)
        elif role == "user":
            return render_template('home_user.html', username=session['username'], email=email, role=role,
                                   date_reg=date_reg)
        else:
            return redirect(url_for('index'))


    else:
        return "Username or Password is wrong!"


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# функции пользователя ---------------
@app.route('/create_task', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        #
        price = request.form['price']
        adres = request.form['adres']
        data_deadline = request.form['data_deadline']
        information = request.form['information']

        wwb.create_task(session['username'], price, adres, data_deadline, information)
        return redirect(url_for('home', username=session['username']))
    return render_template('create_task.html')


@app.route('/show_user_case_archive')
def show_user_case_archive():
    # Получить данные пользователя из базы данных
    username = session['username']
    tasks = wwb.get_tasks_by_username_archive(username)
    ss = ''
    for i in tasks:
        ss += """
			<tr>
			  <td>id заявки {}</td>
			  <td>дата {}</td>
			  <td> <a href="/show_user_case_for_user/{}"><button>Show Details</button></a></td>
			</tr>
				""".format(i[0], i[7], i[0])

    return render_template('show_user_keys.html', t=ss, name="архивные задания")


@app.route('/show_user_case_active')
def show_user_case_active():
    # Получить данные пользователя из базы данных
    username = session['username']
    tasks = wwb.get_tasks_by_username_active(username)
    ss = ''
    for i in tasks:
        ss += """
			<tr>
			  <td>id заявки {}</td>
			  <td>дата {}</td>
			  <td> <a href="/show_user_case_for_user/{}"><button>Show Details</button></a></td>
			</tr>
				""".format(i[0], i[7], i[0])

    return render_template('show_user_keys.html', t=ss, name="активные задания")


@app.route('/create_comm/<username>/<idd>', methods=['GET', 'POST'])
def create_comm(username, idd):
    if request.method == 'POST':
        text = request.form['comment']

        wwb.create_comment(username, idd, text)

        return redirect(url_for('show_user_case_for_user', username=username, idd=idd))

    return render_template('comment.html')


@app.route('/show_user_case_for_user/<idd>')
def show_user_case_for_user(idd):
    task_data = wwb.show_user_case_for_user(idd)
    username = session['username']
    ss = "<table>"
    comment = wwb.show_comment(idd)
    if len(comment) > 0:

        for i in comment:
            ss += """

				  <td>{}</td>
				  <td>{}</td>
				  <td>дата {}</td>
				</tr>
			""".format(i[2], i[1], i[4])
        ss += "</table>"
    else:
        ss = ''

    return render_template('task.html', task0=task_data[0], task1=task_data[1],
                           task2=task_data[2],
                           task3=task_data[3],
                           task4=task_data[4],
                           task5=task_data[5],
                           task6=task_data[6],
                           task7=task_data[7],
                           task8=task_data[8],
                           task11="{}/{}".format(username, idd),
                           task9=ss)


@app.route('/open_case')
def open_case():
    username = session['username']
    tasks = wwb.open_case(username)
    ss = ''

    for i in tasks:
        ss += """
			<tr>
			  <td>id заявки {}</td>
			  <td>дата {}</td>
			  <td> <a href="/show_user_case_for_user/{}"><button>Show Details</button></a></td>
			  <td> <a href="/case_end/{}"><button>выполнил</button></a></td>

			</tr>
		""".format(i[0], i[7], i[0], i[0])
    return render_template('show_user_keys.html', t=ss, name="")


@app.route('/close_case')
def close_case():
    username = session['username']
    tasks = wwb.close_case(username)
    ss = ''

    for i in tasks:
        ss += """
			<tr>
			  <td>id заявки {}</td>
			  <td>дата {}</td>
			  <td> <a href="/show_user_case_for_user/{}"><button>Show Details</button></a></td>


			</tr>
		""".format(i[0], i[7], i[0])
    return render_template('show_user_keys.html', t=ss, name="закрытые задания")


@app.route('/choise_new_case')
def choise_new_case():
    username = session['username']
    tasks = wwb.choise_new_case(username)
    ss = ''

    for i in tasks:
        ss += """
			<tr>
			  <td>id заявки {}</td>
			  <td>дата {}</td>
			  <td> <a href="/show_user_case_for_user/{}"><button>Show Details</button></a></td>
			  <td> <a href="/choise_case/{}"><button>choise</button></a></td>
			</tr>
		""".format(i[0], i[7], i[0], i[0])
    return render_template('show_user_keys.html', t=ss, name="выбор нового задания")


@app.route('/choise_case/<idd>', methods=['GET', 'POST'])
def choise_case(idd):
    username = session['username']
    wwb.update_task_worker(username, idd)
    return redirect(url_for('choise_new_case', username=username))


@app.route('/delete_case/<username>/<idd>', methods=['GET', 'POST'])
def delete_case(username, idd):
    wwb.delete_case(username, idd)
    return redirect(url_for('all_case', username=username))


@app.route('/case_end/<idd>', methods=['GET', 'POST'])
def case_end(idd):
    username = session['username']
    wwb.case_end(username, idd)
    return redirect(url_for('home'))


@app.route('/all_case')
def all_case():
    username = session['username']
    tasks = wwb.case_all(username)
    ss = ''

    for i in tasks:
        ss += """
			<tr>
			  <td>id заявки {}</td>
			  <td>дата {}</td>
			  <td> <a href="/show_user_case_for_user/{}"><button>Show Details</button></a></td>
			  <td> <a href="/delete_case/{}/{}"><button>delete</button></a></td>
			  <td> <a href="/case_end/{}"><button>завершить задание</button></a></td>


			</tr>
		""".format(i[0], i[7], i[0], username, i[0], i[0])
    return render_template('show_user_keys.html', t=ss)


@app.route('/users')
def get_users():
    username = session['username']
    users = wwb.get_users()
    ss = ''
    for i in users:
        ss += """
			<tr>
			  <td>id пользователя {}</td>
			  <td>имя {}</td>
			  <td>{}</td>

			  <td> <a href="/set_worker/{}"><button>назначить рабочим</button></a></td>
			  <td> <a href="/set_admin/{}"><button>назначить админом</button></a></td>
			  <td> <a href="/delete_user/{}"><button>удалить</button></a></td>
			</tr>
		""".format(i[0], i[1], i[4], i[0], i[0], i[0])

    return render_template('show_user_keys.html', t=ss, name="база пользователей")


@app.route('/set_worker/<idd>', methods=['GET', 'POST'])
def set_worker(idd):
    wwb.set_worker(idd)
    return redirect(url_for('get_users'))


@app.route('/set_admin/<idd>', methods=['GET', 'POST'])
def set_admin(idd):
    wwb.set_admin(idd)
    return redirect(url_for('get_users'))


@app.route('/delete_user/<idd>', methods=['GET', 'POST'])
def delete_user(idd):
    wwb.delete_user(idd)
    return redirect(url_for('get_users'))


if __name__ == '__main__':
    app.run(debug=True)