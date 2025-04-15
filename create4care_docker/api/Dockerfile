# Use official python image
FROM python:3.10

# Install netcat if not present (optional, if you need nc for waiting)
RUN apt-get update && apt-get install -y \ 
netcat-openbsd \
&& apt-get clean

# Set working directory
WORKDIR /app

# Copy the entire project into the container
COPY api .

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Start the FastAPI app with Uvicorn
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]

# Start the run the seed
# RUN python db/seed.py
# RUN python -m db.seed