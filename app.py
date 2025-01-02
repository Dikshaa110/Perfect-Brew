# import threading
# from flask import Flask, jsonify, request, render_template
# import virtual_mouse  # Import virtual_mouse.py functions

# app = Flask(__name__)

# # Initialize global thread variable
# virtual_mouse_thread = None

# @app.route('/')
# def index():
#     return render_template('index.html')  # Rendering the index.html file

# @app.route('/start_virtual_mouse', methods=['POST'])
# def start_virtual_mouse():
#     global virtual_mouse_thread
#     try:
#         if virtual_mouse_thread is None or not virtual_mouse_thread.is_alive():
#             # Start the virtual mouse in a new thread
#             virtual_mouse_thread = threading.Thread(target=virtual_mouse.run_virtual_mouse, daemon=True)
#             virtual_mouse_thread.start()
#             return jsonify({'status': 'Virtual Mouse Started'}), 200
#         else:
#             return jsonify({'status': 'Virtual Mouse already running'}), 400
#     except Exception as e:
#         return jsonify({'status': f'Error: {str(e)}'}), 500

# @app.route('/stop_virtual_mouse', methods=['POST'])
# def stop_virtual_mouse():
#     try:
#         virtual_mouse.stop_virtual_mouse()
#         return jsonify({'status': 'Virtual Mouse Stopped'}), 200
#     except Exception as e:
#         return jsonify({'status': f'Error: {str(e)}'}), 500

# if __name__ == '__main__':
#     app.run(debug=True)
import threading
from flask import Flask, jsonify, request, render_template
import virtual_mouse  # Import virtual_mouse.py functions

app = Flask(__name__)

# Initialize global thread variable
virtual_mouse_thread = None

@app.route('/')
def index():
    return render_template('index.html')  # Rendering the index.html file

@app.route('/start_virtual_mouse', methods=['POST'])
def start_virtual_mouse():
    global virtual_mouse_thread
    try:
        if virtual_mouse_thread is None or not virtual_mouse_thread.is_alive():
            # Start the virtual mouse in a new thread
            virtual_mouse_thread = threading.Thread(target=virtual_mouse.start_virtual_mouse, daemon=True)
            virtual_mouse_thread.start()
            return jsonify({'status': 'Virtual Mouse Started'}), 200
        else:
            return jsonify({'status': 'Virtual Mouse already running'}), 400
    except Exception as e:
        return jsonify({'status': f'Error: {str(e)}'}), 500

@app.route('/stop_virtual_mouse', methods=['POST'])
def stop_virtual_mouse():
    try:
        virtual_mouse.stop_virtual_mouse()
        return jsonify({'status': 'Virtual Mouse Stopped'}), 200
    except Exception as e:
        return jsonify({'status': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)

