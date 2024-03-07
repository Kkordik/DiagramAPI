from fastapi import FastAPI, HTTPException
from starlette.responses import Response
from graphviz import Source
import urllib.parse
import tempfile

app = FastAPI()

@app.get("/gen")
async def render_graph(dot: str):
    # Decode the DOT code from the URL parameter
    decoded_dot_code = urllib.parse.unquote(dot)

    try:
        # Create a temporary file for the output
        with tempfile.NamedTemporaryFile(suffix='.png') as tmpfile:
            output_file = tmpfile.name
            src = Source(decoded_dot_code)
            src.render(outfile=output_file, format='png', cleanup=True)

            with open(output_file, "rb") as file:
                content = file.read()
            return Response(content=content, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
