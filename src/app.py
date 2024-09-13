from flask import Flask, render_template, request
import logging
from collections import defaultdict, Counter

app = Flask(__name__)

# Setup error logger
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

# Routes
@app.route('/')
def index():
    return render_template('index.html')

def build_inverted_index(dataset):
    inverted_index = defaultdict(set)
    
    for doc_id, entry in enumerate(dataset):
        keywords_part, rest = entry.split(':', 1)
        keywords = keywords_part.strip().lower()
        
        words = rest.lower().split()
        for word in words:
            inverted_index[word].add(doc_id)
    
    return inverted_index

# inverse indexing search algorithm

def search_inverted_index(index, keywords):
    doc_scores = Counter()
    
    for keyword in keywords:
        keyword = keyword.lower()
        if keyword in index:
            for doc_id in index[keyword]:
                doc_scores[doc_id] += 1
    
    sorted_docs = sorted(doc_scores.items(), key=lambda item: item[1], reverse=True)
    
    return sorted_docs

@app.route('/search', methods=['POST', 'GET'])
def search():
    dataset = [ # for now this "database" is just for testing the search algorithm
        'Chicken Puppy: Dummy Title 1, image.jpg, The best chicken kibble for your puppy!',
        'Beef Adult: Dummy Title 2, image.jpg, Absolute best beef for your adult dog!',
        'Lamb Senior: Dummy Title 3, image.jpg, Lamb food for your senior dog.'
    ]
    
    if request.method == 'POST':
        
        # Fetch the options selected by the user
        try:
            product_type = request.form.get('ProductType')
            flavor = request.form.get('Flavor')
            dietary_needs = request.form.get('SpecialDietaryNeeds')
            age_range = request.form.get('AgeRange')
            breed_size = request.form.get('BreedSize')
            price_range = request.form.get('PriceRange')
            health_benefits = request.form.get('HealthBenefits')
        except Exception as e:
            logger.error(f'Error: {e}')
            return render_template('error.html')
        
        search_terms = [product_type, flavor, dietary_needs, age_range, breed_size, price_range, health_benefits]
        search_terms = [term for term in search_terms if term]  # Filter out empty terms
        
        inverted_index = build_inverted_index(dataset)
        sorted_docs = search_inverted_index(inverted_index, search_terms)
        
        if sorted_docs:
            best_doc_id = sorted_docs[0][0]  # Get the ID of the best matching document
            best_product = dataset[best_doc_id]
        else:
            best_product = "No matching product found." # When we actually get a real database we will remove this because it will be useless, but for now we use it because we have such a small database
        
        return render_template('search_results.html', best_product=best_product)

    return render_template('search.html')

@app.route('/search_products', methods=['POST', 'GET'])
def search_products():
    pass # haven't worked on this yet because this feature is not very important.

if __name__ == '__main__':
    app.run(debug=True)
