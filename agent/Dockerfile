FROM golang:alpine AS builder

WORKDIR /app

COPY src/ ./

# Build
ARG TARGETOS TARGETARCH
RUN CGO_ENABLED=0 GOGC=75 GOOS=linux GOARCH=amd64 go build -ldflags "-w -s" -o /agent

FROM scratch

COPY --from=builder /agent /agent
EXPOSE 8080
ENTRYPOINT ["/agent"]