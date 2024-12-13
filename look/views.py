from django.shortcuts import render
from django.http import JsonResponse
from .models import Product, ProductIndex
from nltk.stem import PorterStemmer, WordNetLemmatizer
from fuzzywuzzy import fuzz
from nltk.corpus import stopwords
import re
import json
import nltk
from nltk.tokenize import word_tokenize
import ssl


# Set up SSL context for downloading NLTK data
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download required NLTK data
#nltk.download('wordnet')
#nltk.download('punkt')
#nltk.download('punkt_tab')
#nltk.download('stopwords')
def normalize_text(text):
    return re.sub(r'[^a-z0-9\s]', '', text.lower())

def search_view(request):
    if request.method == 'GET':
        # Render the search page when the method is GET
        return render(request, 'look/search.html')

    elif request.method == 'POST':
        # Handle the AJAX request for search functionality
        data = json.loads(request.body)
        query = data.get('query', '').lower()  # Keep query as a string
        features = data.get('features', [])

        # Fetch all products from the database
        products = Product.objects.all()

        # Prepare product data for processing
        product_list = [{
            'id': product.product_id,
            'name': product.product_name.lower(),
            'category': product.category.lower(),
            'price': product.discounted_price,
            'rating': product.rating
        } for product in products]

        query = normalize_text(query) if "normalize" in features else query  # Normalize the query if needed
        query = word_tokenize(query) if "tokenize" in features else query
        print ("tokenize",query)

        if "lemmatization" in features:
            le = WordNetLemmatizer()
            query = [le.lemmatize(q) for q in query]
            print("lemmatize",query)
        results = []
        
        if "stopwords" in features:
            stop_words = set(stopwords.words('english'))
            query = [q for q in query if q.lower() not in stop_words]
            print("stopwords",query)

        # Single loop over product_list
        for product in product_list:
            if "tokenize" in features:
                # Tokenized matching
                name_tokens = product['name']
                category_tokens = product['category']
                
                #normalize if required
                if "normalize" in features:
                    name_tokens = normalize_text(name_tokens)
                    category_tokens = normalize_text(category_tokens)
                
                #mandatory tokenize for all usecase.
                name_tokens = word_tokenize(name_tokens)
                category_tokens = word_tokenize(category_tokens)

                name_matches = sum(1 for token in query if token in name_tokens)
                category_matches = sum(1 for token in query if token in category_tokens)
                total_matches = name_matches + category_matches

            else:
                # Simple string matching
                total_matches = (
                    (1 if query in product['name'] else 0) +
                    (1 if query in product['category'] else 0)
                )

            if total_matches > 0:
                results.append({
                    'product': product,
                    'matches': total_matches
                })

        # Sort results by match count
        sorted_results = sorted(results, key=lambda x: x['matches'], reverse=True)
        final_results = [result['product'] for result in sorted_results]

        return JsonResponse({
            'results':final_results,
            'query_tokens': query,
            }, safe=False)

    # Fallback for invalid request methods
    return JsonResponse({"error": "Invalid request method"}, status=400)

def save_index(request):
    if request.method == 'POST':
        try:
            products = Product.objects.all()
            for product in products:
                # Preprocess and create tokens
                category_tokens = product.category.split('|')
                category_tokens = [normalize_text(part) for part in category_tokens]
                category_tokens = [token for part in category_tokens for token in word_tokenize(part)]

                name_tokens = normalize_text(product.product_name)
                #category_tokens = normalize_text(product.category)

                name_tokens = word_tokenize(name_tokens)
                #category_tokens = word_tokenize(category_tokens)

                le = WordNetLemmatizer()
                name_tokens = [le.lemmatize(n) for n in name_tokens]
                category_tokens = [le.lemmatize(c) for c in category_tokens]
                
                ProductIndex.objects.update_or_create(
                    product_id=product.product_id,
                    defaults={
                        'name_tokens': " ".join(name_tokens),
                        'categories': " ".join(category_tokens),
                        'price': product.discounted_price,
                        'discount_percentage': product.discount_percentage,
                        'rating': product.rating,
                        'rating_count': product.rating_count,
                    }
                )

            return JsonResponse({'status': 'success', 'message': 'Index saved successfully.'}, status=200)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)
