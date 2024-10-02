# deploy_metabase.py
import modal
import subprocess

app = modal.App("metabase-server")
IMAGE_VERSION = "v0.50.27"
PORT=3000

image = (
    modal.Image.from_registry(f"metabase/metabase:{IMAGE_VERSION}", add_python="3.12", setup_dockerfile_commands=[
        "RUN apk add --no-cache curl",
        "RUN curl -Lo /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub",
        "RUN curl -Lo glibc-2.34-r0.apk https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.34-r0/glibc-2.34-r0.apk",
        "RUN apk add --force-overwrite glibc-2.34-r0.apk",
        "RUN rm glibc-*.apk",
        "RUN /usr/local/bin/python3 -m pip install --upgrade pip",
    ])
    .pip_install("protobuf==4.25.3")
    .dockerfile_commands("ENTRYPOINT []")
)

@app.function(image=image, concurrency_limit=1, allow_concurrent_inputs=100, enable_memory_snapshot=True)
@modal.web_server(PORT, startup_timeout=300)
def metabase_webserver():
    subprocess.Popen("/app/run_metabase.sh", shell=True)
