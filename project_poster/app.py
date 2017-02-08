from flask import Flask, redirect, url_for, request, make_response
from jinja2 import Environment, PackageLoader
from project_poster.logger import NullLogger
from project_poster.studentdb import CSVStudentDB
from project_poster.projectdb import DummyProjectDB
import sys, traceback


class ApplicationRoot:
    def __init__(self, app, env, var, logger=NullLogger()):
        self.var = var
        self.logger = logger
        self.global_template = env.get_template('global_template.html')
        self.index_template = env.get_template('index.html')

        @app.route('/')
        def index():
            return self.index()

    def log(self, msg):
        self.logger.log("ApplicationRoot: %s"%msg)

    def index(self):
        variables = dict(self.var)
        variables.update({'subtitle': "Welcome to Project Poster",\
                            'body': self.index_template.render()})
        return self.global_template.render(**variables)


class StudentBehaviour:
    def __init__(self, app, env, var, logger=NullLogger(),\
            studentdb=CSVStudentDB('project_poster/resources/csv/studentlist.csv'),\
            projectdb=DummyProjectDB()):
        self.var = dict(var)
        self.var['navigation'] += ('/', "Main Menu"),
        self.logger = logger
        self.global_template = env.get_template('global_template.html')
        self.login_template = env.get_template('student_login.html')
        self.view_template = env.get_template('student_view.html')
        self.confirmation_template = env.get_template('student_confirmation.html')
        self.banner_template = env.get_template('student_banner.html')
        self.studentdb = studentdb
        self.projectdb = projectdb

        @app.route('/students')
        def studentRoute():
            return self.route()

        @app.route('/students/login', methods=['GET', 'POST'])
        def studentLogin():
            return self.login()

        @app.route('/students/logout')
        def studentLogout():
            return self.logout()

        @app.route('/students/view')
        def studentView():
            return self.view()

        @app.route('/students/confirmation', methods=['POST'])
        def studentConfirmation():
            return self.confirmation()

    def log(self, msg):
        self.logger.log("StudentBehaviour: %s"%msg)

    def getStudent(self):
        return request.cookies.get('studenttoken').split(':')

    def loggedIn(self):
        try:
            return self.studentdb.studentExists(*self.getStudent())
        except:
            return False

    def route(self):
        return redirect(url_for(\
                'studentView' if self.loggedIn() else 'studentLogin'))

    def login(self):
        error = ''
        if request.method == 'POST':
            try:
                name = request.form['name']
                number = request.form['number']
                if self.studentdb.studentExists(name, number):
                    resp = make_response(redirect(url_for('studentView')))
                    resp.set_cookie('studenttoken', '%s:%s'%(name,number))
                    self.log("created cookie for %s (fcn login)"%name)
                    return resp
                else:
                    error = "Student name and number combonation "\
                                "was invalid"
            except:
                error = "There was an error with the request"
            self.log("student could not log in because %s (fcn login)"%error)
        if self.loggedIn():
            self.log("student redirected already logged in (fcn login)")
            return redirect(url_for('studentView'))
        variables = dict(self.var)
        variables.update({'subtitle': "Student Login",\
                'body': self.login_template.render({'error': error})})
        return self.global_template.render(variables)

    def logout(self):
        return self.redirectLogout()

    def redirectLogout(self, destination='/'):
        resp = make_response(redirect(destination))
        resp.set_cookie('studenttoken', "", expires=0)
        return resp

    def createBanner(self):
        name = self.getStudent()[0]
        return self.banner_template.render(name=name)

    def view(self):
        try:
            name,number = self.getStudent()
            assert self.studentdb.studentExists(name, number),\
                    "Student %s:%s does not exist"%(name,number)
            def make_proj(proj):
                projDict = proj.toDict()
                number = proj.getNumber()
                if not self.projectdb.projectAvailable(number):
                    projDict['name'] += ' AttributedTo '+self.projectdb.getStudent(number)[0]
                return projDict
            projects = [make_proj(proj) for proj in self.projectdb.getProjects()]
            view = self.view_template.render(projects=projects)
            banner = self.createBanner()
            variables = dict(self.var)
            variables['subtitle'] = "Student View"
            variables['body'] = view
            variables['banner'] = banner
            return self.global_template.render(**variables)
        except Exception as e:
            self.log("There was an exception at view (%r)"%e)
            traceback.print_exc(file=sys.stdout)
            return self.redirectLogout(url_for('studentLogin'))

    def confirmation(self):
        try:
            project = request.form['project_selection']
            accepted = self.projectdb.projectAvailable(project)
            probject =self.projectdb.getProjectByNumber(project)
            if accepted:
                self.projectdb.attributeProjectTo(probject.getNumber(), self.getStudent())
            name = probject.getName()
            cls,description = \
                ('accepted', "You have successfully selected the project '%s'"%name)\
                if accepted else\
                ('denied', "The project '%s' was already taken"%name)
            body = self.confirmation_template.render(confirmation=cls,\
                    description=description)
            banner = self.createBanner()
            variables = dict(self.var)
            variables['body'] = body
            variables['banner'] = banner
            return self.global_template.render(**variables)
        except Exception as e:
            self.log("There was an exception at confirmation (%r)"%e)
            traceback.print_exc(file=sys.stdout)
            return redirect(url_for('studentView'))

class Application:
    def __init__(self, behaviour=[ApplicationRoot, StudentBehaviour],\
            title='Project Poster', logger=NullLogger()):
        self.app = Flask(__name__)
        self.env = Environment(\
                        loader=PackageLoader('project_poster',\
                                                'templates'))
        self.var = {'title': title, 'scripts': (), 'navigation': ()}
        self.behaviour = [behave(self.app, self.env, self.var, logger)\
                            for behave in behaviour]
    def run(self):
        self.app.run()


