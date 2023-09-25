from website import create_app
from website.root import close_db
app = create_app()
@app.teardown_appcontext
def app_teardown(exception):
    close_db(exception)
if __name__ =='__main__':
    app.run(debug=True)