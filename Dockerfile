FROM --platform=$BUILDPLATFORM node:18
ENV TZ=Asia/Ho_Chi_Minh
WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
CMD ["npm", "start"]
