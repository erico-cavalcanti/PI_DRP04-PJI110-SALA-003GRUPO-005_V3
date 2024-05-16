from app import app, db
#from flask_migrate import MigrateCommand
#from flask_script import Manager

if __name__ == '__main__':
    app.run(debug=True)

#manager = Manager(app)
#manager.add_command('db', MigrateCommand)

#if __name__ == '__main__':
#    manager.run()
