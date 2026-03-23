DNS measurements
 with RIPE Atlas
              Stéphane Bortzmeyer
    bortzmeyer@nic.fr




                                    1 / 12
2 / 12
Domain Name System




                     3 / 12
Domain Name System



    A part of the Internet infrastructure,




                                             3 / 12
Domain Name System



    A part of the Internet infrastructure,
    As necessary as IP,




                                             3 / 12
Domain Name System



    A part of the Internet infrastructure,
    As necessary as IP,
    Often forgotten in studies about resilience or quality of service.




                                                                     3 / 12
RIPE Atlas and DNS




                     4 / 12
RIPE Atlas and DNS



     RIPE Atlas probes can do DNS measurements,




                                                  4 / 12
RIPE Atlas and DNS



     RIPE Atlas probes can do DNS measurements,
     Many options in
     https://atlas.ripe.net/docs/api/v2/reference/#/measurem




                                                      4 / 12
Web interface




                5 / 12
Result




         6 / 12
From the API


    {’definitions’: [{’protocol’: ’UDP’,
          ’description’: ’DNS resolution of ns.eu.org’, ’af’: 4,
          ’query_argument’: ’ns.eu.org’, ’query_type’: ’AAAA’,
          ’query_class’: ’IN’, ’set_rd_bit’: True, ’type’: ’dns’,
          ’use_probe_resolver’: True}], ’is_oneoff’: True, ’probes’:
      [{’requested’: 10, ’type’: ’area’, ’value’: ’WW’,
          ’tags’: {’include’: [’system-resolves-a-correctly’, ’system-re




                                                                7 / 12
Many options




               8 / 12
From Magellan
  Output similar to dig

  % ripe-atlas measure dns --query-argument=lqdn.net
  ...
  Probe #29198
  ========================================================================

    ; <<>> RIPE Atlas Tools <<>> lqdn.net.
    ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 47134
    ;; flags: qr ra rd; QUERY: 1, ANSWER: 1, AUTHORITY: 2, ADDITIONAL: 10

    ;; QUESTION SECTION:
    ;lqdn.net.                       IN      A

    ;; ANSWER SECTION:
    lqdn.net.               600      IN      A     204.12.240.154
  ...
    ;; Query time: 386.869 msec
    ;; SERVER: 172.20.7.1#53(172.20.7.1)                            9 / 12
    ;; WHEN: Mon Oct 02 17:43:55 CEST 2017
    ;; MSG SIZE rcvd: 253
From my tool



  % atlas-resolve --nsid --type AAAA --requested 10 \
      --country FR mamot.fr
  [2a00:99a0:0:1000::7] : 9 occurrences
  Test #9407903 done at 2017-10-02T15:47:28Z




                                                        10 / 12
Result in JSON

     "from": "89.142.236.92",
     "msm_id": 9668778,
     "msm_name": "Tdig",
     "prb_id": 16336,
     "resultset": [
       {
         "dst_addr": "192.168.1.1",
         "result": {
           "ANCOUNT": 3,
           "ARCOUNT": 1,
           "ID": 10350,
           "abuf": "KG6BgAABAAMA...




                                      11 / 12
Traps




        12 / 12
Traps



        Some probes use strange resolvers (alternative roots, lying
        resolvers. . . ),




                                                                      12 / 12
Traps



        Some probes use strange resolvers (alternative roots, lying
        resolvers. . . ),
        Some networks intercept and rewrite DNS traffic, some have
        transparent proxies.




                                                                      12 / 12
Examples of use
Examples of use



     Measuring censorship (selecting probes by country).
     Warning: may raise ethical issues.
Examples of use



     Measuring censorship (selecting probes by country).
     Warning: may raise ethical issues.
     Check the different instances of an anycast server.
Examples of use



     Measuring censorship (selecting probes by country).
     Warning: may raise ethical issues.
     Check the different instances of an anycast server.
     Test that your domain name resolves from everywhere. (Many
     zones have all eggs in the same basket.)
Merci !

       www.afnic.fr
    contact@afnic.fr
