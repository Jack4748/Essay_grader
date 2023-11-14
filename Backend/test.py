from flask import Flask, jsonify
import asyncio

app = Flask(__name__)

async def mlfunc():
    await asyncio.sleep(5)
    return "HELLO"

async def updatefunc(result):
    data = await mlfunc()
    result = data + "   " + "ABC"
    print(result)

async def handle():
    a = "HELLO"
    update_task = asyncio.ensure_future(updatefunc(a))  # Run updatefunc in the background
    return a

@app.route('/')
async def main():
    a = await handle()
    return jsonify({'result': a})

if __name__ == '__main__':
    app.run(debug=True)



