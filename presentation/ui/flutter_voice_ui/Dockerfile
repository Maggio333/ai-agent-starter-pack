# Dockerfile for Flutter Voice UI Frontend
# Multi-stage build for optimized image size

# ============================================================================
# Stage 1: Build stage
# ============================================================================
FROM ghcr.io/cirruslabs/flutter:stable as builder

# Set working directory
WORKDIR /app

# Copy pubspec files first for better caching
# pubspec.lock is optional - will be generated if missing
COPY pubspec.yaml ./
COPY pubspec.lock* ./

# Get dependencies (this will generate pubspec.lock if missing)
RUN flutter pub get

# Copy application source
COPY . .

# Build Flutter web app
# Using release mode for optimized production build
# CanvasKit is now the default renderer in newer Flutter versions
RUN flutter build web --release

# ============================================================================
# Stage 2: Runtime stage
# ============================================================================
FROM nginx:alpine

# Copy built Flutter web app to nginx
COPY --from=builder /app/build/web /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]

