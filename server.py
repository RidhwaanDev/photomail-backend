from flask import Flask, jsonify, request
import google
from google.cloud import vision

import io

app = Flask(__name__)

@app.route('/', methods=["POST"])
def handle_image_cv():
    if request.method == 'POST':
        file = request.files['file']
        file.save(file.filename)
        print("doing " + file.filename)
        res = detect_document(file.filename)
        return jsonify({"status":"ok",
                        "response": res,
                        })
    return "hello"

def detect_document(path):
    """Detects document features in an image."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)

    result = ''
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            # print('\nBlock confidence: {}\n'.format(block.confidence))

            for paragraph in block.paragraphs:
                # print('Paragraph confidence: {}'.format(
                #paragraph.confidence))

                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    result += '\n' if word_text == 'm' else word_text
                    # print('Word text: {} (confidence: {})'.format(
                    #word_text, word.confidence))
                    #for symbol in word.symbols:
                    # print('\tSymbol: {} (confidence: {})'.format(
                    #symbol.text, symbol.confidence))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return result

#print(detect_document('fe'))
