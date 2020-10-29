FROM datadog/agent:latest

COPY ./dd-entrypoint.sh /usr/local/bin
ENTRYPOINT ["/usr/local/bin/dd-entrypoint.sh"]
CMD ["/init"]
