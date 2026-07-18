FROM python:3.12-alpine AS prepare

WORKDIR /work
COPY public ./public
COPY scripts ./scripts
RUN python scripts/validate_public_content.py && python scripts/audit_contrast.py

FROM caddy:2-alpine
COPY Caddyfile /etc/caddy/Caddyfile
COPY --from=prepare /work/public /srv
EXPOSE 8080
CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile", "--adapter", "caddyfile"]
