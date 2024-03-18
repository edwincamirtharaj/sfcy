from django.shortcuts import render

from django.http import JsonResponse
import spacy

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

def process_text(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        if text:
            # Process the text using spaCy
            doc = nlp(text)
            # Perform some processing on the doc if needed
            # For example, extract named entities or perform part-of-speech tagging
            # Then return the processed data as a JSON response
            return JsonResponse({'processed_text': doc.text})
        else:
            return JsonResponse({'error': 'No text provided'})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})

