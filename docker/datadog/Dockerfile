FROM datadog/agent:7.23.1

COPY ./dd-entrypoint.sh /usr/local/bin
ENTRYPOINT ["/usr/local/bin/dd-entrypoint.sh"]
CMD ["/init"]
