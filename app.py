from flask import Flask, render_template, request, jsonify
import plotly.graph_objects as go
import plotly.utils
import json

app = Flask(__name__)


def calculate_rf(layers):
    n = 1  # Initial receptive field
    jump = 1  # Initial jump
    rf_sizes = [1]

    for layer in layers:
        if layer["type"] == "conv":
            kernel = layer["kernel"]
            n = n + (kernel - 1) * jump
        elif layer["type"] == "maxpool":
            kernel = layer["kernel"]
            n = n + (kernel - 1) * jump
            jump = jump * kernel
        rf_sizes.append(n)

    return rf_sizes


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    layers = data["layers"]
    rf_sizes = calculate_rf(layers)

    # Create visualization
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=list(range(len(rf_sizes))),
            y=rf_sizes,
            mode="lines+markers",
            name="Receptive Field Size",
        )
    )

    fig.update_layout(
        title="Receptive Field Growth",
        xaxis_title="Layer Number",
        yaxis_title="Receptive Field Size",
        template="plotly_white",
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return jsonify({"rf_sizes": rf_sizes, "graph": graphJSON})


if __name__ == "__main__":
    app.run(debug=True)
