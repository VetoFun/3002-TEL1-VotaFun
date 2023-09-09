FROM node:18-slim

RUN apt-get update \
    && apt-get install default-jre -y \
    && apt-get install default-jdk -y

# Install the Firebase CLI
RUN npm install -g firebase-tools

# Create a directory for the Firebase project
WORKDIR /firebase

COPY . /firebase

EXPOSE 4000
EXPOSE 9000

CMD ["firebase", "emulators:start"]
