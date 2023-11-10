# Gradle 빌드 단계
FROM gradle:8.4.0-jdk17-alpine AS builder
WORKDIR /app
COPY /backend/build.gradle /backend/settings.gradle /app/
COPY /backend/src /app/src/
RUN gradle build --no-daemon -x test

# 실행 이미지 빌드 단계
FROM openjdk:17-jdk
WORKDIR /app
COPY --from=builder /app/build/libs/backend-0.0.1-SNAPSHOT.jar /app/backend-springboot.jar
ENTRYPOINT [ "nohup", "java", "-Dspring.profiles.active=production", "-jar", "backend-springboot.jar" ]
