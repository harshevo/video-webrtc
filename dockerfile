# -----------------
# Build Stage
# -----------------
FROM python:3.11-slim as builder

# Set the working directory
WORKDIR /app

# Copy the requirements file to the container
COPY ./requirements.txt /app/requirements.txt

# Install virtualenv
RUN pip install --upgrade pip \
	&& pip install virtualenv

# Create a virtual environment
RUN virtualenv venv

# Activate the virtual environment and install dependencies
RUN . venv/bin/activate && pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI application code to the container
COPY . /app

# -----------------
# Run Stage
# -----------------
FROM python:3.11-slim

# Set the working directory for the run stage
WORKDIR /app

# Copy the installed packages from the builder stage
COPY --from=builder /app/venv /app/venv
COPY --from=builder /app /app

# Ensure the virtual environment is in the PATH
ENV PATH="/app/venv/bin:${PATH}"

# Expose the port on which FastAPI will run
EXPOSE 8000

# Command to run FastAPI using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

