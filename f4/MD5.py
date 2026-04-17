import math
from flask import Flask, request, render_template_string

app = Flask(__name__)

def md5_manual_with_logs(message):
    logs = []
    S = [7, 12, 17, 22] * 4 + [5, 9, 14, 20] * 4 + [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4
    K = [int(abs(math.sin(i + 1)) * 2**32) & 0xFFFFFFFF for i in range(64)]

    a0, b0, c0, d0 = 0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476

    msg = bytearray(message.encode('utf-8'))
    orig_len_bits = (8 * len(msg)) & 0xFFFFFFFFFFFFFFFF
    msg.append(0x80)
    while len(msg) % 64 != 56:
        msg.append(0)
    msg += orig_len_bits.to_bytes(8, byteorder='little')
    
    logs.append(f"<b>Step 1: Padded Message (Hex):</b> {msg.hex().upper()}")

    for offset in range(0, len(msg), 64):
        a, b, c, d = a0, b0, c0, d0
        chunk = msg[offset:offset+64]
        X = [int.from_bytes(chunk[i:i+4], byteorder='little') for i in range(0, 64, 4)]

        for i in range(64):
            if 0 <= i <= 15:
                f = (b & c) | ((~b) & d)
                g = i
                label = "F"
            elif 16 <= i <= 31:
                f = (d & b) | ((~d) & c)
                g = (5 * i + 1) % 16
                label = "G"
            elif 32 <= i <= 47:
                f = b ^ c ^ d
                g = (3 * i + 5) % 16
                label = "H"
            elif 48 <= i <= 63:
                f = c ^ (b | (~d))
                g = (7 * i) % 16
                label = "I"
            
            temp_f = (f + a + K[i] + X[g]) & 0xFFFFFFFF
            rot = ((temp_f << S[i]) | (temp_f >> (32 - S[i]))) & 0xFFFFFFFF
            a, d, c, b = d, c, b, (b + rot) & 0xFFFFFFFF
            
            # Now logging ALL 64 rounds
            logs.append(f"Round {i:02d} ({label}): A={a:08x}, B={b:08x}, C={c:08x}, D={d:08x}")
            
        a0 = (a0 + a) & 0xFFFFFFFF
        b0 = (b0 + b) & 0xFFFFFFFF
        c0 = (c0 + c) & 0xFFFFFFFF
        d0 = (d0 + d) & 0xFFFFFFFF

    final_hex = (a0.to_bytes(4, 'little') + b0.to_bytes(4, 'little') + 
                 c0.to_bytes(4, 'little') + d0.to_bytes(4, 'little')).hex().upper()
    return final_hex, logs


HTML = """
<!DOCTYPE html><html><body style="font-family:sans-serif; padding:30px; line-height:1.6; max-width:900px; margin:auto; background:#f4f7f6;">
    <h2 style="color:#2c3e50;">MD5 Manual Implementation </h2>
    <form method="POST" style="background:white; padding:25px; border-radius:10px; box-shadow:0 4px 6px rgba(0,0,0,0.1);">
        <label><b>Plain Text Input:</b></label><br>
        <input type="text" name="msg" style="width:100%; padding:12px; margin:15px 0; border:1px solid #ddd; border-radius:4px;" placeholder="Enter message to hash..." value="{{ msg or '' }}" required><br>
        <button type="submit" style="background:#e74c3c; color:white; border:none; padding:12px 25px; cursor:pointer; font-weight:bold; border-radius:4px;">Generate MD5 Hash</button>
    </form>
    
    {% if res %}
    <div style="margin-top:30px;">
        <h3 style="color:#c0392b;">Final MD5 Hash:</h3>
        <code style="font-size:1.4em; font-weight:bold; background:#fff; border-left:6px solid #e74c3c; padding:15px; display:block;">{{ res }}</code>
        
        <h3>Intermediate Iteration Logs:</h3>
        <div style="background:#2c3e50; color:#bdc3c7; padding:20px; border-radius:8px; font-family:monospace; font-size:0.9em; max-height:400px; overflow-y:auto;">
            {% for s in logs %}
                <p style="border-bottom:1px solid #34495e; padding:5px 0; margin:0;">{{ s }}</p>
            {% endfor %}
        </div>
    </div>
    {% endif %}
</body></html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    res, logs, msg = None, [], None
    if request.method == "POST":
        msg = request.form.get("msg")
        res, logs = md5_manual_with_logs(msg)
    return render_template_string(HTML, res=res, logs=logs, msg=msg)

if __name__ == "__main__":
    app.run(debug=True)
