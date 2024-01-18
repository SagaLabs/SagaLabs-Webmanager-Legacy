# Use a Python base image
FROM python:bullseye as backend

WORKDIR /app

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy all files
COPY . .

# Use Node.js to build the frontend
FROM node:lts-bullseye as frontend

WORKDIR /app/sagalabs/firecms

# Copy frontend files
COPY sagalabs/firecms .

# Install dependencies
RUN yarn install

# Build the project
RUN yarn build

# Copy build artifacts from frontend stage and set the CMD for backend
FROM backend as final

# Copy React build output to be served by Flask
COPY --from=frontend /app/sagalabs/firecms/dist /app/sagalabs/firecms/dist

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5001" ]
