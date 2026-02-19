FROM python:3.11-slim

# Install Java for Spark
RUN apt-get update && apt-get install -y openjdk-21-jre-headless && rm -rf /var/lib/apt/lists/*
ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64

# Install uv
RUN pip install uv

# Copy requirements and install dependencies
COPY docker/jupyter/requirements.txt /
RUN uv pip install --system -r /requirements.txt

# Set up Jupyter
RUN useradd -ms /bin/bash jupyter
USER jupyter
WORKDIR /home/jupyter

# Expose port and start JupyterLab
EXPOSE 8888
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--NotebookApp.token=sparkling", "--NotebookApp.notebook_dir=/opt/notebooks"]
