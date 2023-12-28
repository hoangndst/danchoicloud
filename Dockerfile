FROM --platform=${BUILDPLATFORM:-linux/amd64} node:18
WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
CMD ["npm run start"]
