# 构建前端
FROM node:18-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# 构建后端
FROM maven:3.9-eclipse-temurin-17-alpine AS backend-build
WORKDIR /app
COPY backend/pom.xml ./backend/
RUN cd backend && mvn dependency:resolve -q
COPY backend/ ./backend/
COPY --from=frontend-build /app/frontend/dist ./backend/src/main/resources/static/frontend/
RUN cd backend && mvn clean package -DskipTests -q

# 运行
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY --from=backend-build /app/backend/target/yunshop-1.0.0.jar ./
EXPOSE 8080
CMD ["java", "-jar", "yunshop-1.0.0.jar"]
