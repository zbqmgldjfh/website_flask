from main import app

@app.route("/")
def home():
    return "Hello Wordl!"

if __name__ == "__main__":
    app.run(debug=True)
