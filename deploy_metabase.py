import modal
import subprocess


app = modal.App("metabase-server")
IMAGE_VERSION = "v0.50.27"
PORT=3000 # MB_JETTY_PORT

image = (
    modal.Image.from_registry(f"metabase/metabase:{IMAGE_VERSION}", add_python="3.12")
    .dockerfile_commands("ENTRYPOINT []")
)

@app.function(image=image)
@modal.web_server(PORT)
def metabase_webserver():
    subprocess.Popen("/app/run_metabase.sh", shell=True)
