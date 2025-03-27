from flask import Flask

from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app, config={'swagger_ui': True})

@app.route('/example', methods=['GET'])
def example_endpoint():
    """
    Example endpoint returning a simple message.
    ---
    responses:
      200:
        description: A successful response
        schema:
          type: object
          properties:
            message:
              type: string
              example: Hello, World!
    """
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    app.run(debug=True)