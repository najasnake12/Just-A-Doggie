from flask import Flask, render_template, request
import logging

app = Flask(__name__)

# setup error logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('errorlogger.log')
file_handler.setLevel(logging.ERROR)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


# routes
@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/search', methods=['POST', 'GET'])
def search():
    
    try:
        Search_Input = request.form.get('Search_Input') 
    except Exception as e:
        logger.error(f'Error: {e}')
        return render_template('error.html')
    
    # soon starting on other stuff
    
     
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)