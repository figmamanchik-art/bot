from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    
    # Получаем число воды из запроса
    number = req['queryResult']['parameters'].get('number', 0)
    
    # Достаём старый total из контекста (если есть)
    old_total = 0
    for context in req['queryResult'].get('outputContexts', []):
        if 'water-tracker' in context['name']:
            old_total = context['parameters'].get('total', 0)
            break
    
    # Считаем новое значение
    new_total = old_total + number
    
    # Формируем ответ
    response = {
        "fulfillmentText": f"Добавлено {number} мл. Всего выпито: {new_total} мл.",
        "outputContexts": [
            {
                "name": f"{req['session']}/contexts/water-tracker",
                "lifespanCount": 99,
                "parameters": {
                    "total": new_total
                }
            }
        ]
    }
    
    return jsonify(response)

@app.route('/')
def home():
    return "Water counter bot is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
